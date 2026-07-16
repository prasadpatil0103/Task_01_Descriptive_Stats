# COMPARISON: Pure Python vs. Pandas

## Do the results agree?

Yes — for every column that both scripts classified as **numeric**, the
count, mean, min, max, standard deviation, and median matched exactly
(to floating-point precision). This makes sense: both scripts are
ultimately doing the same arithmetic (sum divided by count for the mean,
sample standard deviation with `ddof=1`/`n-1`, etc.) over the same
underlying values.

## Where the two approaches disagreed on *type*, not *arithmetic*

The real difference between the two scripts isn't in the numbers — it's
in **which columns get treated as numeric in the first place**.

`spend`, `impressions`, and `estimated_audience_size` all *look* like
they should be numeric (they clearly represent quantities), but the raw
values are strings like:

```
"{'lower_bound': '100', 'upper_bound': '499'}"
```

Neither `float()` (pure Python) nor `pd.read_csv`'s automatic dtype
inference (Pandas) can parse that as a number, so **both** tools
independently classify these three columns as non-numeric/"object" —
they simply agree by falling back to the same default. This is exactly
the kind of column Pandas' `df.info()` and `.describe()` will happily
report as an "object" dtype without ever telling you *why*, whereas
writing the pure-Python type-inference function by hand
(`infer_column_type`) forces you to actually look at a raw value and
ask "does `float()` work on this?" — and to realize the answer is no,
and why.

## Where pure Python forced explicit decisions that Pandas made silently

- **What counts as missing.** The pure-Python script has an explicit
  `MISSING_TOKENS` set and an `is_missing()` function. Pandas has its
  own (very similar) built-in rules for what becomes `NaN` on read —
  but those rules are baked into `pd.read_csv` and easy to never think
  about.
- **Sample vs. population standard deviation.** `statistics.stdev()`
  computes the *sample* standard deviation by default, and so does
  `pandas.Series.std()` (`ddof=1`). Getting this wrong (e.g. using
  `statistics.pstdev()`) would have silently produced numbers that
  looked plausible but didn't match.
- **What "numeric" means.** Writing `infer_column_type()` by hand made
  it obvious that a column is only "numeric" if *every* non-missing
  value parses as a float — a single stray value like `"N/A"` would
  flip a whole column to categorical. Pandas' automatic dtype inference
  does something conceptually similar under the hood, but you never see
  the decision being made.

## What writing the pure-Python version taught us that Pandas alone would not have

Writing `pure_python_stats.py` first is what made the range-string
columns (`spend`, `impressions`, `estimated_audience_size`) obvious as a
data-quality issue, rather than something to discover later. Because the
pure-Python script has to explicitly decide "does this value parse as a
float?" for every single value, it's immediately clear *why* those three
columns fail the test. If we had started with Pandas and only glanced at
`df.describe()`, it would have been easy to assume those object-dtype
columns were just "text fields" rather than numeric data trapped in an
unusual string format — because `describe(include='all')` reports a
count/unique/top/freq for them and moves on, without raising any flag
that they're secretly quantities.

## Takeaway

Pandas is faster to write and to run, and for this dataset the two
approaches produced identical numbers wherever a fair, apples-to-apples
comparison was possible. But the pure-Python version is what surfaced
the single most important data-quality fact in this dataset: spend and
impressions aren't stored as numbers at all, and any headline like
"$X million was spent on Facebook ads" requires an explicit, documented
choice about how to turn a range into a single figure.
