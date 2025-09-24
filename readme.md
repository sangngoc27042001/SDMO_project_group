# Developer Identity Deduplication

## What is this repo about?
This project provides tools to detect and filter duplicate developer identities in Git repositories.  
It uses heuristics based on names and emails (Bird heuristic) to identify potential duplicates among commit authors.

## How to set up
Install dependencies:
```bash
python3 -m pip install -r requirements.txt
```

## How to run
You can run the main script directly from the terminal:

```bash
python3 -m src.main --repo_url https://github.com/dotnet-architecture/eShopOnContainers --threshold 0.7
```

Arguments:
- `--repo_url`: Repository URL to analyze (default: `https://github.com/dotnet-architecture/eShopOnContainers`)
- `--threshold`: Threshold for duplicate detection (default: `0.7`)

## How to test
Run the unit tests with:
```bash
python3 -m unittest discover -s src/unit_test -p "test_*.py"
