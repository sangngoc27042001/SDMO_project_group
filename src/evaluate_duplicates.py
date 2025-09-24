import json
import sys
import os
from mine_and_dedupe import hash_repo_url


def evaluate_duplicates(repo_url, max_commits=None, show_samples=10):
    """
    Evaluate duplicate pairs and classify them as True Positives (TP) or False Positives (FP).
    A TP is when the emails are exactly the same.
    Results are saved in the same run directory as duplicates.json.
    """
    run_dir = os.path.join("runs", hash_repo_url(repo_url, max_commits))
    duplicates_path = os.path.join(run_dir, "duplicates.json")
    results_path = os.path.join(run_dir, "evaluation.json")

    if not os.path.exists(duplicates_path):
        raise FileNotFoundError(f"duplicates.json not found at {duplicates_path}")

    with open(duplicates_path, "r") as f:
        duplicates = json.load(f)

    tp = 0
    fp = 0
    false_positive_examples = []
    true_positive_examples = []

    for pair in duplicates:
        if len(pair) != 2:
            continue
        p1, p2 = pair
        if len(p1) < 2 or len(p2) < 2:
            continue

        email1 = p1[1].strip().lower()
        email2 = p2[1].strip().lower()

        if email1 == email2:
            tp += 1
            if len(true_positive_examples) < show_samples:
                true_positive_examples.append((p1, p2))
        else:
            fp += 1
            if len(false_positive_examples) < show_samples:
                false_positive_examples.append((p1, p2))

    total = tp + fp
    results = {
        "total_pairs": total,
        "true_positives": tp,
        "false_positives": fp,
        "sample_false_positives": false_positive_examples,
        "sample_true_positives": true_positive_examples,
    }

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    repo_url = "https://github.com/tensorflow/tensorflow.git"
    max_commits = 1000

    evaluate_duplicates(repo_url, max_commits)
