# FINDINGS

## What this dataset is

Each row is a single Facebook ad purchased during the 2024 U.S. Presidential
election cycle where the ad text mentions at least one presidential
candidate. The dataset has 246,745 rows and 40 columns, covering the
buyer's page name, ad creation/delivery dates, estimated audience size,
impressions, spend (all three of the latter given as ranges rather than
exact figures), platform, and a large block of `illuminating_*` columns
that appear to be automated topic/message-type classifications (e.g.
whether an ad discusses immigration, is an attack ad, contains a call to
action, and so on).

## Who spent the money

Spend is stored as a range string (e.g. `"{'lower_bound': '100',
'upper_bound': '499'}"`) rather than an exact dollar figure, so any total
is an estimate built from the midpoint of each range. With that caveat,
spending is heavily concentrated at the top: **Kamala Harris** and **Joe
Biden**'s pages together account for well over $100M of estimated spend,
with **Donald J. Trump**'s page a distant third. Beyond the candidates'
own pages, a long tail of PACs, advocacy groups, and media-style pages
(e.g. "Kamala HQ," "The Daily Scroll," "Future Forward," "America PAC")
make up most of the remaining volume — a small number of large spenders,
then a long tail of much smaller ones, which is a fairly typical pattern
for political ad spending.

## Who was mentioned

Trump-related terms ("Donald Trump" + "President Trump") and
Harris-related terms lead the mention counts by a wide margin, which
tracks with them being the two major-party nominees for most of the
election window. Biden appears heavily too — a reminder that he was the
presumptive nominee for a large part of the ad-buying period before
dropping out of the race in July 2024. Down-ballot/primary figures
(Nikki Haley, Ron DeSantis, Dean Phillips, RFK Jr.) show up far less
often, concentrated earlier in the dataset.

## Timing

Ad volume is very low through 2022 and early 2023, rises steadily across
2023 and the first half of 2024, and then spikes sharply from August
through October 2024 — October 2024 alone accounts for roughly a third
of every ad in the entire dataset. That pattern lines up with the
conventional "closing weeks" surge in political ad spending, and likely
also reflects the compressed timeline after Biden withdrew from the race
in July 2024 and the resulting scramble to define the new Harris/Walz
ticket before Election Day.

## Data quality notes

- `spend`, `impressions`, and `estimated_audience_size` are stored as
  range strings, not numbers. Any numeric analysis of "how much was
  spent" requires an explicit parsing decision (e.g. using the midpoint,
  the lower bound, or the upper bound of each range) — this is not
  something either script does automatically, since it changes the
  answer.
- `ad_delivery_stop_time` and `bylines` have a modest amount of missing
  data (under 1% each); `estimated_audience_size` is missing for a
  similarly small fraction of rows.
- The `illuminating_*` binary columns (0/1 flags for topics, message
  type, incivility, etc.) appear to be model-generated labels rather
  than raw survey/self-report data — useful for pattern-finding, but
  worth remembering they carry whatever error rate the underlying
  classifier has.

## What surprised me

How lopsided the spending is once you group by page name rather than by
individual ad: a handful of pages dominate total estimated spend, while
the median ad buyer's page appears only a small number of times. Also
notable is just how much of the entire year's ad volume is packed into
the final ~10 weeks before the election.
