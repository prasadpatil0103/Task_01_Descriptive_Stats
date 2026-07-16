# Task_01_Descriptive_Stats

Descriptive statistics on the **2024 U.S. Presidential Facebook political ads**
dataset, computed two independent ways: once with only Python's standard
library, and once with Pandas. The point of the exercise is to see whether
the two approaches agree, and to notice everything Pandas quietly handles
for you.

## Project structure

```
Task_01_Descriptive_Stats/
├── data/                     <- put the CSV here (not tracked in git)
├── pure_python_stats.py       <- stdlib-only analysis
├── pandas_stats.py            <- Pandas analysis
├── requirements.txt
├── FINDINGS.md                 <- narrative write-up of what's in the data
├── COMPARISON.md                <- pure Python vs. Pandas reflection
└── README.md
```

## Getting the data

This repo does **not** include the dataset. Download it from:

- Source: Google Drive — 2024 Facebook Political Ads

Save the file as:

```
data/fb_ads_president_scored_anon.csv
```

Both scripts read from that relative path, so as long as you keep this
folder structure and run the scripts from the project root, no path editing
is required.

## Setup

Pure Python script — no installation needed, just Python 3.

Pandas script:

```bash
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running

```bash
python pure_python_stats.py
python pandas_stats.py
```

Each script prints:
- Dataset shape and missing-value counts
- Per-column statistics (numeric: count/mean/min/max/std/median;
  categorical: count/unique/mode/top-5)

## Summary of findings (short version — see FINDINGS.md for the full write-up)

- The dataset contains **246,745 ad records** across **40 columns**.
- Spending and impressions are stored as **range strings** (e.g.
  `"{'lower_bound': '100', 'upper_bound': '499'}"`), not plain numbers —
  this is the single biggest "gotcha" in the dataset (see COMPARISON.md).
- **Kamala Harris**, **Joe Biden**, and **Donald J. Trump** were the three
  highest-spending page names by a wide margin, together accounting for the
  large majority of estimated ad spend in the dataset.
- **Donald Trump** and **Kamala Harris** were the two most-mentioned
  candidates by a wide margin.
- Ad volume rose steadily through 2024 and spiked sharply in the final
  weeks before the election (October 2024 alone accounts for roughly a
  third of all ads in the dataset).

## Comparison of approaches

See [COMPARISON.md](COMPARISON.md) for the full reflection. Short version:
numeric results (mean/min/max/std/median) matched exactly between the two
scripts for every genuinely numeric column. The interesting differences
show up in **type inference** — Pandas and the pure-Python script both
classify `spend`, `impressions`, and `estimated_audience_size` as
non-numeric "object"/string columns, because their values are dict-like
range strings rather than plain numbers. Neither tool "sees through" that
formatting automatically; a human has to decide how to parse it.
