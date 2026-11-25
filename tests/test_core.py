"""Tests for Semantic Response Memoizer."""
import unittest
from semantic_response_memoizer.core import SemanticMemoizer


class TestSemanticMemoizer(unittest.TestCase):
    def test_hits_rephrased_query_and_isolates_models(self):
        memo = SemanticMemoizer(similarity_threshold=0.75, ttl_seconds=100)
        memo.put("model-a", "Summarize Kubernetes pod crash logs", "OOMKilled", now=10.0)
        self.assertEqual(memo.get("model-a", "Please summarize Kubernetes pod crash logs", now=20.0), "OOMKilled")
        self.assertIsNone(memo.get("model-b", "Summarize Kubernetes pod crash logs", now=20.0))

    def test_ttl_expiration_evicts_entry(self):
        memo = SemanticMemoizer(ttl_seconds=10)
        memo.put("m1", "Check status", "ok", now=0.0)
        self.assertIsNone(memo.get("m1", "Check status", now=15.0))
