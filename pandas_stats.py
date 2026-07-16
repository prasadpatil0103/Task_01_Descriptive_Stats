"""
pandas_stats.py

Descriptive statistics on the 2024 Facebook Presidential Ad dataset,
using Pandas.

Run:
    python pandas_stats.py

Expects the dataset at ./data/fb_ads_president_scored_anon.csv
(see README.md for where to download it).
"""

import pandas as pd

DATA_PATH = "data/fb_ads_president_scored_anon.csv"

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)


def print_section(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def main():
    df = pd.read_csv(DATA_PATH)

    print_section("SHAPE & DTYPES")
    print(f"Shape: {df.shape[0]} rows x {df.shape[1]} columns")
    print("\ndf.info():")
    df.info()

    print_section("MISSING VALUES PER COLUMN")
    missing_count = df.isna().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)
    missing_summary = pd.DataFrame(
        {"missing_count": missing_count, "missing_pct": missing_pct}
    )
    print(missing_summary)

    # Split columns by dtype the same way the pure-python script does:
    # numeric = pandas parsed it as int/float, everything else = categorical.
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    print_section("DESCRIBE (NUMERIC COLUMNS)")
    print(df[numeric_cols].describe())

    print_section("DESCRIBE (ALL COLUMNS, include='all')")
    print(df.describe(include="all").T)

    print_section("CATEGORICAL COLUMNS: value_counts() / nunique()")
    for col in categorical_cols:
        print(f"\n-- {col} --")
        print(f"  nunique: {df[col].nunique(dropna=True)}")
        print("  top 5 values:")
        print(df[col].value_counts().head(5).to_string())

    print_section("NUMERIC COLUMNS: stats for cross-check against pure_python_stats.py")
    for col in numeric_cols:
        s = df[col]
        print(f"\n-- {col} --")
        print(f"  count : {s.count()}")
        print(f"  mean  : {s.mean()}")
        print(f"  min   : {s.min()}")
        print(f"  max   : {s.max()}")
        print(f"  std   : {s.std()}")   # pandas uses sample std (ddof=1) by default
        print(f"  median: {s.median()}")


if __name__ == "__main__":
    main()
