from src.mine_and_dedupe import mine_commits, apply_bird, filter_pairs

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Bird heuristic duplicate detection on a repository")
    parser.add_argument("--repo_url", default="https://github.com/twbs/bootstrap",
                        help="Repository URL to analyze (default: eShopOnContainers)")
    parser.add_argument("--threshold", type=float, default=1,
                        help="Threshold for duplicate detection (default: 0.7)")
    parser.add_argument("--limit_no_pair", type=int, default=None,
                        help="Limit the number of pairs to be processed (default: None)")
    args = parser.parse_args()

    repo_url = args.repo_url
    thresh_hold = args.threshold
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
