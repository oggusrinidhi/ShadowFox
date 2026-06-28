"""
Final Project: Advanced Sales Data Analysis

This script creates a complete notebook-style data analysis project from
scratch using only the Python standard library. It generates a retail sales
financial dataset, cleans it, answers research questions, creates SVG
visualizations, prints the findings, and writes a Jupyter notebook file.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from statistics import mean, median


PROJECT_DIR = Path(__file__).resolve().parent
DATA_FILE = PROJECT_DIR / "retail_sales_financial_dataset.csv"
CLEAN_FILE = PROJECT_DIR / "cleaned_retail_sales_financial_dataset.csv"
REPORT_FILE = PROJECT_DIR / "sales_financial_analysis_report.md"
NOTEBOOK_FILE = PROJECT_DIR / "sales_financial_analysis.ipynb"
OUTPUT_DIR = PROJECT_DIR / "outputs"


REGIONS = ["North", "South", "East", "West"]
CATEGORIES = ["Technology", "Furniture", "Office Supplies", "Appliances"]
CHANNELS = ["Online", "Retail Store", "Wholesale"]


def fiscal_year(d: date) -> int:
    """Fiscal year starts in April and ends in March."""
    return d.year + 1 if d.month >= 4 else d.year


def fiscal_quarter(d: date) -> str:
    fiscal_month = ((d.month - 4) % 12) + 1
    return f"Q{math.ceil(fiscal_month / 3)}"


def month_key(d: date) -> str:
    return f"{d.year}-{d.month:02d}"


def format_money(value: float) -> str:
    return f"${value:,.2f}"


def generate_dataset(path: Path = DATA_FILE, rows: int = 720) -> list[dict[str, str]]:
    random.seed(42)
    start = date(2024, 1, 1)
    end = date(2025, 12, 31)
    days = (end - start).days
    data: list[dict[str, str]] = []

    category_profile = {
        "Technology": {"base": 920, "cogs": 0.48, "manufacturing": 0.16, "freight": 0.055},
        "Furniture": {"base": 760, "cogs": 0.42, "manufacturing": 0.22, "freight": 0.105},
        "Office Supplies": {"base": 210, "cogs": 0.36, "manufacturing": 0.12, "freight": 0.045},
        "Appliances": {"base": 650, "cogs": 0.44, "manufacturing": 0.19, "freight": 0.08},
    }
    region_multiplier = {"North": 1.08, "South": 0.94, "East": 1.02, "West": 1.13}
    channel_discount = {"Online": 0.08, "Retail Store": 0.05, "Wholesale": 0.13}

    for idx in range(1, rows + 1):
        d = start + timedelta(days=random.randint(0, days))
        category = random.choice(CATEGORIES)
        region = random.choice(REGIONS)
        channel = random.choice(CHANNELS)
        profile = category_profile[category]

        seasonal_multiplier = 1.0
        if d.month in (11, 12):
            seasonal_multiplier += 0.26
        elif d.month in (6, 7):
            seasonal_multiplier += 0.10
        elif d.month in (1, 2):
            seasonal_multiplier -= 0.07

        quantity = random.randint(1, 8)
        gross_sales = (
            profile["base"]
            * quantity
            * region_multiplier[region]
            * seasonal_multiplier
            * random.uniform(0.74, 1.28)
        )
        if idx in (52, 341, 612):
            gross_sales *= random.uniform(3.2, 4.7)

        discount = gross_sales * channel_discount[channel] * random.uniform(0.55, 1.45)
        returns = gross_sales * random.choice([0, 0, 0, 0.015, 0.025, 0.04])
        net_sales = gross_sales - discount - returns
        cogs = gross_sales * profile["cogs"] * random.uniform(0.88, 1.15)
        manufacturing = gross_sales * profile["manufacturing"] * random.uniform(0.86, 1.18)
        freight = gross_sales * profile["freight"] * random.uniform(0.70, 1.55)

        row = {
            "transaction_id": f"TXN-{idx:04d}",
            "date": d.isoformat(),
            "region": region,
            "category": category,
            "sales_channel": channel,
            "quantity": str(quantity),
            "gross_sales": f"{gross_sales:.2f}",
            "discount": f"{discount:.2f}",
            "returns": f"{returns:.2f}",
            "cogs": f"{cogs:.2f}",
            "manufacturing_cost": f"{manufacturing:.2f}",
            "freight_cost": f"{freight:.2f}",
        }

        if idx in (97, 421):
            row["freight_cost"] = ""
        if idx == 208:
            row["cogs"] = ""

        data.append(row)

    write_csv(path, data, list(data[0].keys()))
    return data


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_dataset(path: Path = DATA_FILE) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def to_float(row: dict, key: str) -> float | None:
    value = row.get(key, "")
    if value == "":
        return None
    return float(value)


def clean_dataset(rows: list[dict]) -> tuple[list[dict], dict]:
    numeric_fields = [
        "quantity",
        "gross_sales",
        "discount",
        "returns",
        "cogs",
        "manufacturing_cost",
        "freight_cost",
    ]
    missing_before = {
        field: sum(1 for row in rows if row.get(field, "") == "") for field in numeric_fields
    }
    medians = {
        field: median(to_float(row, field) for row in rows if to_float(row, field) is not None)
        for field in numeric_fields
    }

    cleaned = []
    for row in rows:
        d = date.fromisoformat(row["date"])
        clean_row = dict(row)
        for field in numeric_fields:
            value = to_float(row, field)
            clean_row[field] = medians[field] if value is None else value

        clean_row["date_obj"] = d
        clean_row["month"] = month_key(d)
        clean_row["fiscal_year"] = fiscal_year(d)
        clean_row["fiscal_quarter"] = fiscal_quarter(d)
        clean_row["net_sales"] = (
            clean_row["gross_sales"] - clean_row["discount"] - clean_row["returns"]
        )
        clean_row["total_cost"] = (
            clean_row["cogs"]
            + clean_row["manufacturing_cost"]
            + clean_row["freight_cost"]
        )
        clean_row["profit_loss"] = clean_row["net_sales"] - clean_row["total_cost"]
        clean_row["profit_margin_pct"] = (
            clean_row["profit_loss"] / clean_row["net_sales"] * 100
            if clean_row["net_sales"]
            else 0
        )
        cleaned.append(clean_row)

    write_rows = []
    for row in cleaned:
        out = {
            key: row[key]
            for key in [
                "transaction_id",
                "date",
                "region",
                "category",
                "sales_channel",
                "quantity",
                "gross_sales",
                "discount",
                "returns",
                "cogs",
                "manufacturing_cost",
                "freight_cost",
                "net_sales",
                "total_cost",
                "profit_loss",
                "profit_margin_pct",
                "fiscal_year",
                "fiscal_quarter",
                "month",
            ]
        }
        write_rows.append(out)
    write_csv(CLEAN_FILE, write_rows, list(write_rows[0].keys()))

    stats = {
        "rows": len(rows),
        "missing_before": missing_before,
        "medians_used": medians,
    }
    return cleaned, stats


def aggregate(rows: list[dict], group_key: str, value_keys: list[str]) -> dict:
    grouped = defaultdict(lambda: {key: 0.0 for key in value_keys} | {"count": 0})
    for row in rows:
        key = row[group_key]
        grouped[key]["count"] += 1
        for value_key in value_keys:
            grouped[key][value_key] += float(row[value_key])
    return dict(grouped)


def summarize(rows: list[dict], cleaning_stats: dict) -> dict:
    totals = {
        "gross_sales": sum(row["gross_sales"] for row in rows),
        "net_sales": sum(row["net_sales"] for row in rows),
        "cogs": sum(row["cogs"] for row in rows),
        "manufacturing_cost": sum(row["manufacturing_cost"] for row in rows),
        "freight_cost": sum(row["freight_cost"] for row in rows),
        "profit_loss": sum(row["profit_loss"] for row in rows),
    }
    totals["profit_margin_pct"] = totals["profit_loss"] / totals["net_sales"] * 100

    by_category = aggregate(
        rows,
        "category",
        ["gross_sales", "net_sales", "cogs", "manufacturing_cost", "freight_cost", "profit_loss"],
    )
    by_region = aggregate(rows, "region", ["net_sales", "profit_loss", "freight_cost"])
    by_fy = aggregate(rows, "fiscal_year", ["gross_sales", "net_sales", "profit_loss"])
    by_month = aggregate(rows, "month", ["net_sales", "profit_loss"])

    for group in (by_category, by_region, by_fy, by_month):
        for values in group.values():
            values["profit_margin_pct"] = values["profit_loss"] / values["net_sales"] * 100

    freight_correlations = correlation(
        [row["freight_cost"] for row in rows], [row["profit_margin_pct"] for row in rows]
    )
    manufacturing_correlation = correlation(
        [row["manufacturing_cost"] for row in rows], [row["net_sales"] for row in rows]
    )

    top_category = max(by_category.items(), key=lambda item: item[1]["profit_loss"])
    weakest_category = min(by_category.items(), key=lambda item: item[1]["profit_margin_pct"])
    best_region = max(by_region.items(), key=lambda item: item[1]["profit_margin_pct"])
    peak_month = max(by_month.items(), key=lambda item: item[1]["net_sales"])

    return {
        "cleaning": cleaning_stats,
        "totals": totals,
        "by_category": by_category,
        "by_region": by_region,
        "by_fiscal_year": by_fy,
        "by_month": by_month,
        "freight_margin_correlation": freight_correlations,
        "manufacturing_sales_correlation": manufacturing_correlation,
        "top_category": top_category,
        "weakest_category": weakest_category,
        "best_region": best_region,
        "peak_month": peak_month,
    }


def correlation(xs: list[float], ys: list[float]) -> float:
    x_mean = mean(xs)
    y_mean = mean(ys)
    numerator = sum((x - x_mean) * (y - y_mean) for x, y in zip(xs, ys))
    denominator = math.sqrt(
        sum((x - x_mean) ** 2 for x in xs) * sum((y - y_mean) ** 2 for y in ys)
    )
    return numerator / denominator if denominator else 0.0


def svg_bar_chart(title: str, data: dict[str, float], path: Path, y_label: str) -> None:
    width, height = 980, 560
    margin = 80
    chart_width = width - margin * 2
    chart_height = height - margin * 2
    max_value = max(data.values()) or 1
    bar_width = chart_width / len(data) * 0.64
    gap = chart_width / len(data) * 0.36
    colors = ["#2f6f73", "#b85c38", "#5a6f9f", "#d19c2c", "#6a8055", "#8b5e83"]

    parts = [svg_header(width, height), text(width / 2, 38, title, 24, "middle", "#1f2933")]
    parts.append(text(28, height / 2, y_label, 14, "middle", "#4b5563", rotate=-90))
    for idx, (label, value) in enumerate(data.items()):
        x = margin + idx * (bar_width + gap) + gap / 2
        bar_h = chart_height * (value / max_value)
        y = height - margin - bar_h
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{bar_h:.1f}" '
            f'rx="4" fill="{colors[idx % len(colors)]}"/>'
        )
        parts.append(text(x + bar_width / 2, height - 48, label, 13, "middle", "#374151"))
        parts.append(text(x + bar_width / 2, y - 10, short_money(value), 13, "middle", "#111827"))
    parts.append(svg_footer())
    path.write_text("\n".join(parts), encoding="utf-8")


def svg_line_chart(title: str, data: dict[str, float], path: Path, y_label: str) -> None:
    width, height = 1100, 560
    margin = 80
    chart_width = width - margin * 2
    chart_height = height - margin * 2
    items = sorted(data.items())
    max_value = max(value for _, value in items) or 1
    min_value = min(value for _, value in items)
    span = max(max_value - min_value, 1)

    points = []
    for idx, (_, value) in enumerate(items):
        x = margin + idx * (chart_width / (len(items) - 1))
        y = height - margin - ((value - min_value) / span) * chart_height
        points.append((x, y, value))

    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y, _ in points)
    parts = [svg_header(width, height), text(width / 2, 38, title, 24, "middle", "#1f2933")]
    parts.append(text(28, height / 2, y_label, 14, "middle", "#4b5563", rotate=-90))
    parts.append(
        f'<polyline points="{polyline}" fill="none" stroke="#2f6f73" stroke-width="4" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )
    for idx, ((label, _), (x, y, value)) in enumerate(zip(items, points)):
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="#b85c38"/>')
        if idx % 2 == 0:
            parts.append(text(x, height - 48, label, 12, "middle", "#374151"))
        if value == max_value:
            parts.append(text(x, y - 15, short_money(value), 13, "middle", "#111827"))
    parts.append(svg_footer())
    path.write_text("\n".join(parts), encoding="utf-8")


def svg_cost_breakdown(summary: dict, path: Path) -> None:
    data = {
        "COGS": summary["totals"]["cogs"],
        "Manufacturing": summary["totals"]["manufacturing_cost"],
        "Freight": summary["totals"]["freight_cost"],
    }
    svg_bar_chart("Cost Breakdown Across All Transactions", data, path, "Cost")


def svg_header(width: int, height: int) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">'
        '<rect width="100%" height="100%" fill="#f8fafc"/>'
    )


def svg_footer() -> str:
    return "</svg>"


def text(
    x: float,
    y: float,
    content: str,
    size: int,
    anchor: str,
    fill: str,
    rotate: int | None = None,
) -> str:
    transform = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, sans-serif" '
        f'font-size="{size}" text-anchor="{anchor}" fill="{fill}"{transform}>{content}</text>'
    )


def short_money(value: float) -> str:
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:.0f}"


def create_visualizations(summary: dict) -> list[Path]:
    OUTPUT_DIR.mkdir(exist_ok=True)
    monthly_net_sales = {key: value["net_sales"] for key, value in summary["by_month"].items()}
    category_profit = {
        key: value["profit_loss"] for key, value in sorted(summary["by_category"].items())
    }
    region_margin = {
        key: value["profit_margin_pct"] for key, value in sorted(summary["by_region"].items())
    }

    paths = [
        OUTPUT_DIR / "monthly_net_sales.svg",
        OUTPUT_DIR / "profit_by_category.svg",
        OUTPUT_DIR / "cost_breakdown.svg",
        OUTPUT_DIR / "profit_margin_by_region.svg",
        OUTPUT_DIR / "final_findings_summary.svg",
    ]
    svg_line_chart("Monthly Net Sales Trend", monthly_net_sales, paths[0], "Net sales")
    svg_bar_chart("Profit by Product Category", category_profit, paths[1], "Profit")
    svg_cost_breakdown(summary, paths[2])
    svg_bar_chart("Profit Margin by Region", region_margin, paths[3], "Profit margin %")
    svg_findings_summary(summary, paths[4])
    return paths


def svg_findings_summary(summary: dict, path: Path) -> None:
    width, height = 1200, 780
    totals = summary["totals"]
    top_category, top_values = summary["top_category"]
    weakest_category, weak_values = summary["weakest_category"]
    best_region, best_region_values = summary["best_region"]
    peak_month, peak_values = summary["peak_month"]

    cards = [
        ("Gross Sales", format_money(totals["gross_sales"]), "#2f6f73"),
        ("Net Sales", format_money(totals["net_sales"]), "#5a6f9f"),
        ("Profit", format_money(totals["profit_loss"]), "#b85c38"),
        ("Profit Margin", f"{totals['profit_margin_pct']:.2f}%", "#d19c2c"),
        ("Top Category", f"{top_category}: {format_money(top_values['profit_loss'])}", "#6a8055"),
        ("Weakest Margin", f"{weakest_category}: {weak_values['profit_margin_pct']:.2f}%", "#8b5e83"),
        ("Best Region", f"{best_region}: {best_region_values['profit_margin_pct']:.2f}%", "#2f6f73"),
        ("Peak Month", f"{peak_month}: {format_money(peak_values['net_sales'])}", "#5a6f9f"),
    ]

    parts = [svg_header(width, height)]
    parts.append(text(width / 2, 58, "Final Project Output: Sales Financial Analysis", 30, "middle", "#111827"))
    parts.append(text(width / 2, 96, "Research question: How do product category, fiscal timing, and cost structure influence profitability?", 17, "middle", "#374151"))

    card_w, card_h = 500, 112
    start_x, start_y = 80, 145
    for idx, (label, value, color) in enumerate(cards):
        col = idx % 2
        row = idx // 2
        x = start_x + col * 560
        y = start_y + row * 130
        parts.append(f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="8" fill="#ffffff" stroke="#d1d5db"/>')
        parts.append(f'<rect x="{x}" y="{y}" width="10" height="{card_h}" rx="5" fill="{color}"/>')
        parts.append(text(x + 32, y + 38, label, 18, "start", "#4b5563"))
        parts.append(text(x + 32, y + 78, value, 24, "start", "#111827"))

    parts.append(text(width / 2, 705, f"Freight cost vs. profit margin correlation: {summary['freight_margin_correlation']:.3f}", 18, "middle", "#111827"))
    parts.append(text(width / 2, 738, f"Manufacturing cost vs. net sales correlation: {summary['manufacturing_sales_correlation']:.3f}", 18, "middle", "#111827"))
    parts.append(svg_footer())
    path.write_text("\n".join(parts), encoding="utf-8")


def create_report(summary: dict, visualization_paths: list[Path]) -> str:
    top_category, top_values = summary["top_category"]
    weakest_category, weak_values = summary["weakest_category"]
    best_region, best_region_values = summary["best_region"]
    peak_month, peak_values = summary["peak_month"]
    totals = summary["totals"]

    report = f"""# Advanced Sales Financial Analysis

## Dataset
The dataset contains {summary["cleaning"]["rows"]} retail transactions from 2024 and 2025.
It includes transaction date, region, product category, sales channel, gross sales, discounts,
returns, COGS, manufacturing cost, freight cost, fiscal year, and profit metrics.

## Research Question
How do product category, fiscal timing, and cost structure influence profitability in retail sales?

## Data Cleaning
- Missing COGS values: {summary["cleaning"]["missing_before"]["cogs"]}
- Missing freight cost values: {summary["cleaning"]["missing_before"]["freight_cost"]}
- Missing numeric values were replaced with the median of their column.
- Fiscal year was calculated using an April-to-March reporting period.

## Key Findings
- Total gross sales: {format_money(totals["gross_sales"])}
- Total net sales: {format_money(totals["net_sales"])}
- Total profit: {format_money(totals["profit_loss"])}
- Overall profit margin: {totals["profit_margin_pct"]:.2f}%
- Highest-profit category: {top_category}, with {format_money(top_values["profit_loss"])} in profit.
- Weakest category by margin: {weakest_category}, with a {weak_values["profit_margin_pct"]:.2f}% margin.
- Best region by margin: {best_region}, with a {best_region_values["profit_margin_pct"]:.2f}% margin.
- Peak sales month: {peak_month}, with {format_money(peak_values["net_sales"])} in net sales.
- Freight cost and profit margin correlation: {summary["freight_margin_correlation"]:.3f}
- Manufacturing cost and net sales correlation: {summary["manufacturing_sales_correlation"]:.3f}

## Interpretation
The analysis shows that profitability is shaped by both revenue volume and cost structure.
COGS is the largest cost component, but freight becomes especially important for lower-margin
categories. Seasonal peaks appear near the end of the calendar year, which also falls within
fiscal Q3 for an April-start fiscal calendar.

## Visualizations
"""
    for path in visualization_paths:
        report += f"- {path.relative_to(PROJECT_DIR)}\n"

    REPORT_FILE.write_text(report, encoding="utf-8")
    return report


def create_notebook() -> None:
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Advanced Sales Financial Analysis\n",
                    "\n",
                    "This notebook explores a retail sales financial dataset and answers the research question: "
                    "**How do product category, fiscal timing, and cost structure influence profitability?**\n",
                ],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "The analysis includes data generation, data cleaning, fiscal-year feature engineering, "
                    "financial metrics, and visualizations saved as SVG files.\n",
                ],
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import heart\n",
                    "heart.main()\n",
                ],
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "After running the code cell, open `sales_financial_analysis_report.md` for the written findings "
                    "and the `outputs/` folder for visualization files.\n",
                ],
            },
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    NOTEBOOK_FILE.write_text(json.dumps(notebook, indent=2), encoding="utf-8")


def print_findings(summary: dict, visualization_paths: list[Path]) -> None:
    totals = summary["totals"]
    top_category, top_values = summary["top_category"]
    weakest_category, weak_values = summary["weakest_category"]
    best_region, best_region_values = summary["best_region"]
    peak_month, peak_values = summary["peak_month"]

    print("\nADVANCED SALES FINANCIAL ANALYSIS")
    print("=" * 38)
    print("Research question:")
    print("How do product category, fiscal timing, and cost structure influence profitability?")
    print("\nDataset overview:")
    print(f"- Rows analyzed: {summary['cleaning']['rows']}")
    print(f"- Missing COGS values filled: {summary['cleaning']['missing_before']['cogs']}")
    print(
        f"- Missing freight values filled: {summary['cleaning']['missing_before']['freight_cost']}"
    )
    print("\nFinancial summary:")
    print(f"- Gross sales: {format_money(totals['gross_sales'])}")
    print(f"- Net sales: {format_money(totals['net_sales'])}")
    print(f"- Profit/loss: {format_money(totals['profit_loss'])}")
    print(f"- Overall profit margin: {totals['profit_margin_pct']:.2f}%")
    print("\nFindings:")
    print(f"- Highest-profit category: {top_category} ({format_money(top_values['profit_loss'])})")
    print(
        f"- Weakest margin category: {weakest_category} "
        f"({weak_values['profit_margin_pct']:.2f}%)"
    )
    print(
        f"- Best region by margin: {best_region} "
        f"({best_region_values['profit_margin_pct']:.2f}%)"
    )
    print(f"- Peak net-sales month: {peak_month} ({format_money(peak_values['net_sales'])})")
    print(
        "- Freight cost vs. profit margin correlation: "
        f"{summary['freight_margin_correlation']:.3f}"
    )
    print(
        "- Manufacturing cost vs. net sales correlation: "
        f"{summary['manufacturing_sales_correlation']:.3f}"
    )
    print("\nFiles created:")
    print(f"- Dataset: {DATA_FILE.name}")
    print(f"- Cleaned dataset: {CLEAN_FILE.name}")
    print(f"- Notebook: {NOTEBOOK_FILE.name}")
    print(f"- Report: {REPORT_FILE.name}")
    for path in visualization_paths:
        print(f"- Visualization: {path.relative_to(PROJECT_DIR)}")


def main() -> None:
    raw_rows = generate_dataset()
    cleaned_rows, cleaning_stats = clean_dataset(raw_rows)
    summary = summarize(cleaned_rows, cleaning_stats)
    visualization_paths = create_visualizations(summary)
    create_report(summary, visualization_paths)
    create_notebook()
    print_findings(summary, visualization_paths)


if __name__ == "__main__":
    main()
