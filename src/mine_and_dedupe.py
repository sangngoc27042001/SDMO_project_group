import subprocess
import json
from src.bird_heuristic import bird_heuristic
from itertools import combinations
from joblib import Parallel, delayed
from tqdm import tqdm

import hashlib
import os
import pandas as pd
import random

def shuffle_list(items, seed=0):
    items_copy = items[:]  # avoid modifying original list
    rng = random.Random(seed)  # create a local RNG with fixed seed
    rng.shuffle(items_copy)
    return items_copy

def hash_repo_url(repo_url, max_commits=None):
    key_str = f"{repo_url}::{max_commits}"
    repo_hash = hashlib.sha1(key_str.encode("utf-8")).hexdigest()[:12]
    return repo_hash

from pydriller import Repository

def mine_commits(repo_url):
    """
    Use PyDriller to traverse commits and extract (name, email) pairs.
    Uses caching based on hash(repo_url + max_commits).
    """
    repo_hash = hash_repo_url(repo_url)
    run_dir = os.path.join("runs", repo_hash)
    pairs_path = os.path.join(run_dir, "devs.csv")

    # Check cache
    if os.path.exists(pairs_path):
        try:
            df = pd.read_csv(pairs_path)
            return df.to_dict(orient='records')
        except:
            pass

    devs = set()
    print("Beginning to read the commits ...")
    for commit in Repository(repo_url, num_workers=20).traverse_commits():
        devs.add((commit.author.name, commit.author.email))
        devs.add((commit.committer.name, commit.committer.email))

    devs = sorted(devs)
    pairs = [list(d) for d in devs]
    pairs = [{
        "name": p[0],
        "email": p[1],
    } for p in pairs]

    # Save to cache
    os.makedirs(run_dir, exist_ok=True)
    pd.DataFrame(pairs).to_csv(pairs_path, index=False)

    return pd.DataFrame(pairs).to_dict(orient="records")

def handle_two_pairs(p1, p2):
    return bird_heuristic(p1, p2)

def apply_bird(repo_url, pairs, limit_no_pair=None):
    """
    Apply Bird heuristic to all pairs and return potential duplicates.
    """
    # Check cache
    repo_hash = hash_repo_url(repo_url)
    run_dir = os.path.join("runs", repo_hash)
    pairs_path = os.path.join(run_dir, "devs_similarity.csv")
    if limit_no_pair is not None:
        pairs_path += "_limit="+str(limit_no_pair)+".csv"

    if os.path.exists(pairs_path):
        try:
            df = pd.read_csv(pairs_path)
            return df.to_dict(orient='records')
        except:
            pass
    
    # Apply Bird heuristic

    combinations_of_2_pairs = list(combinations(pairs, 2))
    if limit_no_pair is not None:
        combinations_of_2_pairs = shuffle_list(combinations_of_2_pairs, seed=42)
        combinations_of_2_pairs = combinations_of_2_pairs[:limit_no_pair]

    bird_results = Parallel(n_jobs=-1)(
        delayed(handle_two_pairs)(p1, p2) for p1, p2 in tqdm(combinations_of_2_pairs)
    )

    pd.DataFrame(bird_results).to_csv(pairs_path, index=False)
    
    return pd.DataFrame(bird_results).to_dict(orient="records")

def check_bird_heuristic(two_pairs, thresh_hold=0.8):
    if two_pairs['c1'] >= thresh_hold:
        return True
    if two_pairs['c2'] >= thresh_hold:
        return True
    if two_pairs['c3.1'] >= thresh_hold and two_pairs["c3.2"] >= thresh_hold:
        return True
    if two_pairs['c4']:
        return True
    if two_pairs['c5']:
        return True
    if two_pairs['c6']:
        return True
    if two_pairs['c7']:
        return True
    return False

def filter_pairs(repo_url, devs_similarity, thresh_hold=0.8):
    # Check cache
    repo_hash = hash_repo_url(repo_url)
    run_dir = os.path.join("runs", repo_hash)
    pairs_path = os.path.join(run_dir, f"devs_similarity_t={thresh_hold}.csv")

    filtered_devs_similarity = [
        two_pairs for two_pairs in devs_similarity
        if check_bird_heuristic(two_pairs, thresh_hold=thresh_hold)
    ]

    pd.DataFrame(filtered_devs_similarity).to_csv(pairs_path, index=False)
    
    return pd.DataFrame(filtered_devs_similarity).to_dict(orient="records")



if __name__ == "__main__":
    import os

    # Example: large repo with many contributors
    repo_url = "https://github.com/dotnet-architecture/eShopOnContainers"
    thresh_hold = 0.7

    print("Mining commits...")
    pairs = mine_commits(repo_url)
    print(f"Collected {len(pairs)} unique (name, email) pairs")

    print("Applying Bird heuristic...")
    devs_similarity = apply_bird(repo_url, pairs)
    print(f"Found {len(devs_similarity)} potential duplicate pairs")

    print("Filtering pairs...")
    filtered_pairs = filter_pairs(repo_url, devs_similarity, thresh_hold=0.7)
    print(f"Found {len(filtered_pairs)} potential duplicate pairs")