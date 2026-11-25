"""Core TTL-aware lexical semantic cache for deterministic LLM subqueries."""
import re
import time
from typing import Any, Dict, List, Optional, Set


STOPWORDS = {"the", "a", "an", "please", "could", "you", "of", "for", "to", "in", "is"}


class SemanticMemoizer:
    """Caches LLM subquery responses keyed by model version and normalized token overlap."""

    def __init__(self, similarity_threshold: float = 0.8, ttl_seconds: float = 3600.0):
        self.similarity_threshold = similarity_threshold
        self.ttl_seconds = ttl_seconds
        self._entries: List[Dict[str, Any]] = []
        self.hits = 0
        self.misses = 0

    @staticmethod
    def _tokens(text: str) -> Set[str]:
        words = re.findall(r"[a-z0-9]+", text.lower())
        return {w for w in words if w not in STOPWORDS}

    def put(self, model_id: str, prompt: str, response: Any, now: Optional[float] = None):
        ts = time.time() if now is None else now
        self._entries.append({
            "model_id": model_id,
            "prompt": prompt,
            "tokens": self._tokens(prompt),
            "response": response,
            "expires_at": ts + self.ttl_seconds,
        })

    def get(self, model_id: str, prompt: str, now: Optional[float] = None) -> Optional[Any]:
        ts = time.time() if now is None else now
        q_tokens = self._tokens(prompt)
        best_score = 0.0
        best_resp = None

        active: List[Dict[str, Any]] = []
        for entry in self._entries:
            if entry["expires_at"] < ts:
                continue
            active.append(entry)
            if entry["model_id"] != model_id:
                continue
            if entry["prompt"] == prompt:
                self.hits += 1
                self._entries = active + self._entries[len(active):]
                return entry["response"]
            union = q_tokens | entry["tokens"]
            if union:
                score = len(q_tokens & entry["tokens"]) / len(union)
                if score >= self.similarity_threshold and score > best_score:
                    best_score = score
                    best_resp = entry["response"]

        self._entries = active
        if best_resp is not None:
            self.hits += 1
            return best_resp
        self.misses += 1
        return None
