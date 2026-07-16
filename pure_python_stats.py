"""
pure_python_stats.py

Descriptive statistics on the 2024 Facebook Presidential Ad dataset,
using ONLY the Python standard library (csv, statistics, collections).

Run:
    python pure_python_stats.py

Expects the dataset at ./data/fb_ads_president_scored_anon.csv
(see README.md for where to download it).
"""

import csv
import statistics
from collections import Counter

DATA_PATH = "data/fb_ads_president_scored_anon.csv"

# Values that should be treated as "missing" even though they are
# technically a non-empty string in the raw CSV.
MISSING_TOKENS = {"", "na", "n/a", "null", "none", "nan"}


def is_missing(value):
    return value is None or value.strip().lower() in MISSING_TOKENS


def try_float(value):
    """Return float(value) if possible, else None."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def load_rows(path):
    """Load the CSV into a list of dicts using csv.DictReader."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames
    return rows, fieldnames


def infer_column_type(values):
    """
    Decide whether a column is 'numeric' or 'categorical'.

    Strategy: look at every non-missing value. If every single one of
    them can be parsed as a float, call the column numeric. Otherwise
    it's categorical. This is intentionally strict -- a column like
    estimated_audience_size that stores a Python-dict-looking string
    such as "{'lower_bound': '100', 'upper_bound': '499'}" will FAIL
    this test and correctly fall through to categorical, because it
    is not literally a number. (Pandas does the same thing -- it will
    read that column as an "object"/string dtype for the same reason.)
    """
    non_missing = [v for v in values if not is_missing(v)]
    if not non_missing:
        return "empty"
    numeric_count = sum(1 for v in non_missing if try_float(v) is not None)
    if numeric_count == len(non_missing):
        return "numeric"
    return "categorical"


def compute_numeric_stats(values):
    """
    values: list of raw strings (may include missing markers).
    Returns a dict of stats computed from scratch with the
    standard library, handling missing values gracefully.
    """
    numbers = [try_float(v) for v in values if not is_missing(v)]
    numbers = [n for n in numbers if n is not None]

    stats = {
        "count": len(numbers),
        "mean": None,
        "min": None,
        "max": None,
        "std": None,
        "median": None,
    }

    if not numbers:
        return stats

    stats["mean"] = sum(numbers) / len(numbers)
    stats["min"] = min(numbers)
    stats["max"] = max(numbers)
    stats["median"] = statistics.median(numbers)

    # Sample standard deviation needs at least 2 points.
    if len(numbers) > 1:
        stats["std"] = statistics.stdev(numbers)
    else:
        stats["std"] = 0.0  # only one data point -> no spread

    return stats


def compute_categorical_stats(values):
    """
    values: list of raw strings (may include missing markers).
    Returns count, number of unique values, mode + its frequency,
    and the top 5 most frequent values.
    """
    clean = [v for v in values if not is_missing(v)]

    stats = {
        "count": len(clean),
        "unique": 0,
        "mode": None,
        "mode_freq": 0,
        "top5": [],
    }

    if not clean:
        return stats

    counts = Counter(clean)
    stats["unique"] = len(counts)
    top5 = counts.most_common(5)
    stats["top5"] = top5
    stats["mode"], stats["mode_freq"] = top5[0]
    return stats


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    rows, fieldnames = load_rows(DATA_PATH)
    total_rows = len(rows)
    total_cols = len(fieldnames)

    # Build a column-name -> list-of-raw-values lookup.
    columns = {name: [row.get(name, "") for row in rows] for name in fieldnames}

    print_section("DATASET OVERVIEW")
    print(f"Total rows:    {total_rows}")
    print(f"Total columns: {total_cols}")

    missing_counts = {}
    inferred_types = {}
    for name in fieldnames:
        values = columns[name]
        missing_counts[name] = sum(1 for v in values if is_missing(v))
        inferred_types[name] = infer_column_type(values)

    print("\nMissing values per column:")
    for name in fieldnames:
        print(f"  {name:45s} missing={missing_counts[name]:>7}  "
              f"inferred_type={inferred_types[name]}")

    print_section("NUMERIC COLUMNS")
    for name in fieldnames:
        if inferred_types[name] != "numeric":
            continue
        s = compute_numeric_stats(columns[name])
        print(f"\n-- {name} --")
        print(f"  count : {s['count']}")
        print(f"  mean  : {s['mean']}")
        print(f"  min   : {s['min']}")
        print(f"  max   : {s['max']}")
        print(f"  std   : {s['std']}")
        print(f"  median: {s['median']}")

    print_section("CATEGORICAL COLUMNS")
    for name in fieldnames:
        if inferred_types[name] not in ("categorical", "empty"):
            continue
        s = compute_categorical_stats(columns[name])
        print(f"\n-- {name} --")
        print(f"  count       : {s['count']}")
        print(f"  unique      : {s['unique']}")
        print(f"  mode        : {s['mode']!r} (freq={s['mode_freq']})")
        print("  top 5 values:")
        for value, freq in s["top5"]:
            # Truncate long values (like dict-looking strings) for readability.
            display = value if len(value) <= 60 else value[:57] + "..."
            print(f"    {display!r:65s} freq={freq}")


if __name__ == "__main__":
    main()
