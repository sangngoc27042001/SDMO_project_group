from src.mine_and_dedupe import mine_commits, apply_bird, filter_pairs, hash_repo_url, shuffle_list
import os
from itertools import combinations
from joblib import Parallel, delayed
from tqdm import tqdm
import pandas as pd
from .compare_str_vector import compare_texts

def handle_two_pairs_proposed(p1, p2):
    name1, email1 = p1["name"], p1["email"]
    name2, email2 = p2["name"], p2["email"]

    prefix1 = email1.split("@")[0]
    prefix2 = email2.split("@")[0]

    c1 = compare_texts(name1, name2)
    c2 = compare_texts(prefix1, prefix2)
    c3 = compare_texts(name1, prefix2)
    c4 = compare_texts(prefix1, name2)

    return {
        'name_1': name1,
        'email_1': email1,
        'name_2': name2,
        'email_2': email2,
        'c1': c1,
        'c2': c2,
        'c3': c3,
        'c4': c4,
    }

def apply_proposed_method(repo_url, pairs, limit_no_pair=None):
    """
    Apply Bird heuristic to all pairs and return potential duplicates.
    """
    # Check cache
    repo_hash = hash_repo_url(repo_url)
    run_dir = os.path.join("runs", repo_hash)
    pairs_path = os.path.join(run_dir, "devs_similarity_proposed_method.csv")
    if limit_no_pair is not None:
        pairs_path += "_limit="+str(limit_no_pair)+".csv"

    if os.path.exists(pairs_path):
        try:
            df = pd.read_csv(pairs_path)
            return df.to_dict(orient='records')
        except:
            pass
    
    # Apply Bird heuristic
    pairs = [
        (
            {
                "name": p["name_1"],
                "email": p["email_1"],
            },
            {
                "name": p["name_2"],
                "email": p["email_2"],
            }
        )
        for p in pairs
    ]
    bird_results = Parallel(n_jobs=-1)(
        delayed(handle_two_pairs_proposed)(p1, p2) for p1, p2 in tqdm(pairs)
    )

    pd.DataFrame(bird_results).to_csv(pairs_path, index=False)
    
    return pd.DataFrame(bird_results).to_dict(orient="records")

def filter_pairs_proposed(repo_url, devs_similarity, thresh_hold=0.6):
    # Check cache
    repo_hash = hash_repo_url(repo_url)
    run_dir = os.path.join("runs", repo_hash)
    pairs_path = os.path.join(run_dir, f"devs_similarity_proposed_method_t={thresh_hold}.csv")

    filtered_devs_similarity = [
        two_pairs for two_pairs in devs_similarity
        if any([
            two_pairs['c1'] >= thresh_hold,
            two_pairs['c2'] >= thresh_hold,
            two_pairs['c3'] >= thresh_hold,
            two_pairs['c4'] >= thresh_hold,
    ])
    ]

    pd.DataFrame(filtered_devs_similarity).to_csv(pairs_path, index=False)
    
    return pd.DataFrame(filtered_devs_similarity).to_dict(orient="records")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Bird heuristic duplicate detection on a repository")
    parser.add_argument("--repo_url", default="https://github.com/keras-team/keras",
                        help="Repository URL to analyze (default: eShopOnContainers)")
    parser.add_argument("--threshold", type=float, default=1,
                        help="Threshold for duplicate detection (default: 0.7)")
    parser.add_argument("--threshold_2", type=float, default=0.6,
                        help="Threshold for duplicate detection (default: 0.7)")
    parser.add_argument("--limit_no_pair", type=int, default=None,
                        help="Limit the number of pairs to be processed (default: None)")
    args = parser.parse_args()

    repo_url = args.repo_url
    thresh_hold = args.threshold
    thresh_hold_2 = args.threshold_2
    limit_no_pair = args.limit_no_pair

    print("Mining commits...")
    pairs = mine_commits(repo_url)
    print(f"Collected {len(pairs)} unique (name, email) pairs")

    print("Applying Bird heuristic...")
    devs_similarity = apply_bird(repo_url, pairs, limit_no_pair)
    print(f"Found {len(devs_similarity)} potential duplicate pairs")

    print("Filtering pairs...")
    filtered_pairs = filter_pairs(repo_url, devs_similarity, thresh_hold=thresh_hold)
    print(f"Found {len(filtered_pairs)} potential duplicate pairs")

    print("Level-2 vector calculation")
    applied_pairs_2 = apply_proposed_method(repo_url, filtered_pairs)
    print(f"Apply level-2 vector calculation to {len(applied_pairs_2)} pairs")

    print("Filtering pairs...")
    filtered_pairs_2 = filter_pairs_proposed(repo_url, applied_pairs_2, thresh_hold=thresh_hold_2)
    print(f"Found {len(filtered_pairs_2)} potential duplicate pairs")
