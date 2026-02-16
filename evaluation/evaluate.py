import sys
import os

sys.path.append(os.path.abspath("src"))

import json
from retrieval import retrieve_relevant_chunks

def evaluate_retrieval(test_file="evaluation/test_queries.json"):
    with open(test_file, "r") as f:
        test_cases = json.load(f)

    total = len(test_cases)
    passed = 0
    total_coverage = 0

    for case in test_cases:
        
        question = case["question"]
        keywords = case["expected_keywords"]

        results = retrieve_relevant_chunks(question)

        combined_text = ""
        for doc, score in results:
            combined_text += doc.page_content.lower()

        keyword_hits = sum(1 for kw in keywords if kw in combined_text)

        print(f"\nQuestion: {question}")
        print(f"Keyword hits: {keyword_hits}/{len(keywords)}")

        coverage_ratio = keyword_hits / len(keywords)
        total_coverage += coverage_ratio
        print(f"Coverage ratio: {coverage_ratio:.2f}")

        if coverage_ratio >= 0.5:
            passed += 1


    print("\n--- Evaluation Summary ---")
    print(f"Passed: {passed}/{total}")
    print(f"Accuracy (rough): {passed/total:.2f}")
    print(f"Average coverage: {total_coverage/total:.2f}")

if __name__ == "__main__":
    evaluate_retrieval()
