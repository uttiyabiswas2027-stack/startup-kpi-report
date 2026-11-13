"""Weekly KPI report for a startup. Reads a CSV of weekly metrics, prints a Markdown summary.

Usage: python kpi_report.py data/sample_metrics.csv > report.md
Columns: week, revenue, new_customers, churned_customers, active_customers, cash_balance, burn
"""
import csv
import sys


def load(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in r:
            if k != "week":
                r[k] = float(r[k])
    return rows


def pct(new, old):
    return None if not old else (new - old) / old * 100


def summarize(rows):
    if len(rows) < 2:
        raise ValueError("need at least two weeks of data")
    cur, prev = rows[-1], rows[-2]
    out = {
        "week": cur["week"],
        "revenue": cur["revenue"],
        "revenue_wow_pct": pct(cur["revenue"], prev["revenue"]),
        "active_customers": cur["active_customers"],
        "churn_pct": cur["churned_customers"] / prev["active_customers"] * 100 if prev["active_customers"] else None,
        "burn": cur["burn"],
        "cash_balance": cur["cash_balance"],
        "runway_weeks": cur["cash_balance"] / cur["burn"] if cur["burn"] else None,
    }
    net_new = cur["revenue"] - prev["revenue"]
    out["burn_multiple"] = cur["burn"] / net_new if net_new > 0 else None
    return out


def flags(s):
    f = []
    if s["runway_weeks"] is not None and s["runway_weeks"] < 26:
        f.append("Runway under 26 weeks: plan fundraising or cut burn.")
    if s["churn_pct"] is not None and s["churn_pct"] > 5:
        f.append("Weekly churn above 5%: check onboarding and support tickets.")
    if s["revenue_wow_pct"] is not None and s["revenue_wow_pct"] < 0:
        f.append("Revenue fell week over week.")
    return f


def fmt(v, suffix=""):
    return "n/a" if v is None else f"{v:,.1f}{suffix}"


def render(s):
    lines = [
        f"# Weekly KPI report - {s['week']}",
        "",
        "| Metric | Value |",
        "| --- | --- |",
        f"| Revenue | {fmt(s['revenue'])} |",
        f"| Revenue WoW | {fmt(s['revenue_wow_pct'], '%')} |",
        f"| Active customers | {fmt(s['active_customers'])} |",
        f"| Weekly churn | {fmt(s['churn_pct'], '%')} |",
        f"| Burn | {fmt(s['burn'])} |",
        f"| Runway (weeks) | {fmt(s['runway_weeks'])} |",
        f"| Burn multiple | {fmt(s['burn_multiple'])} |",
        "",
        "## Flags",
    ]
    fl = flags(s)
    lines += [f"- {x}" for x in fl] if fl else ["- None"]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    sys.stdout.write(render(summarize(load(sys.argv[1]))))
