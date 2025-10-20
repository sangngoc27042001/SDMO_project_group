# SDMO Project Group

This project provides tools for detecting duplicate developer identities in Git repositories using the **Bird heuristic** and an extended **Proposed Method**.

---

## Installation

We use [uv](https://github.com/astral-sh/uv) for environment and dependency management.

```bash
# Create a virtual environment
uv venv

# Install dependencies
uv pip install -r requirements.txt
```

---

## Usage

### 1. Bird Heuristic

Run the Bird heuristic duplicate detection:

```bash
uv run python -m src.main --repo_url <URL> --threshold <float> [--limit_no_pair <int>]
```

#### Parameters
- `--repo_url` (str): GitHub repository URL to analyze.  
  *Default:* `https://github.com/twbs/bootstrap`
- `--threshold` (float): Similarity threshold for duplicate detection.  
  *Default:* `1.0` (recommended: `0.7`)
- `--limit_no_pair` (int, optional): Limit the number of pairs to process.  
  *Default:* `None` (process all pairs)

#### Example
```bash
uv run python -m src.main --repo_url https://github.com/dotnet-architecture/eShopOnContainers --threshold 0.7
```

---

### 2. Proposed Method

Run the extended duplicate detection method:

```bash
uv run python -m src.proposed_method --repo_url <URL> --threshold <float> --threshold_2 <float> [--limit_no_pair <int>]
```

#### Parameters
- `--repo_url` (str): GitHub repository URL to analyze.  
  *Default:* `https://github.com/twbs/bootstrap`
- `--threshold` (float): First-level Bird heuristic similarity threshold.  
  *Default:* `1.0` (recommended: `0.7`)
- `--threshold_2` (float): Second-level vector similarity threshold.  
  *Default:* `0.6`
- `--limit_no_pair` (int, optional): Limit the number of pairs to process.  
  *Default:* `None`

#### Example
```bash
uv run python -m src.proposed_method --repo_url https://github.com/dotnet-architecture/eShopOnContainers --threshold 0.7 --threshold_2 0.6
```

---

## Output

Both methods generate CSV files under the `runs/<repo_hash>/` directory:
- `devs_similarity.csv` (Bird heuristic results)
- `devs_similarity_proposed_method.csv` (Proposed method results)
- Filtered results with thresholds applied are also saved with filenames like:
  - `devs_similarity_t=0.7.csv`
  - `devs_similarity_proposed_method_t=0.6.csv`

---

## Testing

Unit tests are available in the `src/unit_test/` directory.

Run all tests and generate a coverage report in XML format with:

```bash
uv run pytest --cov=src --cov-report=xml
```

- The coverage report will be saved as `coverage.xml` in the project root.

---

## Summary of Methods

- **Bird Heuristic**: Uses name and email similarity with heuristics (Levenshtein ratio, prefix checks, initials).
- **Proposed Method**: Extends Bird heuristic with additional vector-based similarity checks across multiple dimensions.
