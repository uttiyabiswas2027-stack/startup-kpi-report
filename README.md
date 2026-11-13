# startup-kpi-report

A small automation a Founders Office team can run every Monday: it reads weekly metrics from a CSV and produces a Markdown KPI summary (revenue growth, churn, runway, burn multiple) with plain-language flags.

The data in `data/sample_metrics.csv` is made up for demonstration. No real company data is used.

## Run it

```
python kpi_report.py data/sample_metrics.csv
python -m unittest -v
```

Python 3.9+, standard library only.

## Automation

`.github/workflows/weekly-report.yml` runs the tests and the report on every push and every Monday, publishes the table to the run summary and saves `report.md` as an artifact.

## Metrics

- Revenue WoW: change versus last week.
- Weekly churn: churned customers / last week's active customers.
- Runway: cash balance / weekly burn.
- Burn multiple: burn / net new weekly revenue (n/a when revenue did not grow).

## Flags

Runway under 26 weeks, churn above 5%, revenue down week over week. Thresholds are constants in `flags()` and are easy to change.
