"""CLI for Semantic Response Memoizer."""
import argparse
import json
from .core import SemanticMemoizer


def main():
    parser = argparse.ArgumentParser(description="Semantic Response Memoizer CLI")
    parser.add_argument("--threshold", type=float, default=0.75, help="Jaccard cache hit threshold")
    args = parser.parse_args()

    memo = SemanticMemoizer(similarity_threshold=args.threshold)
    memo.put("gemini-flash", "Extract invoice total and vendor name", {"vendor": "Acme", "total": 420})
    hit = memo.get("gemini-flash", "Extract vendor name and invoice total please")
    print(json.dumps({"hit": hit, "hits": memo.hits, "misses": memo.misses}, indent=2))


if __name__ == "__main__":
    main()
