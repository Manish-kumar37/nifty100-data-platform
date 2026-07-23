from pathlib import Path

import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

from src.reports.tearsheet import load_data

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "output" / "reports" / "portfolio"

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

styles = getSampleStyleSheet()

def latest_snapshot(df):

    return (
        df.sort_values("year")
          .groupby("company_id")
          .tail(1)
          .sort_values("company_id")
          .reset_index(drop=True)
    )

UP = "↑"
DOWN = "↓"
FLAT = "→"


def trend_arrow(current, previous):

    if pd.isna(current) or pd.isna(previous):
        return FLAT

    if previous == 0:
        return FLAT

    change = ((current - previous) / abs(previous)) * 100

    if change > 2:
        return UP

    elif change < -2:
        return DOWN

    return FLAT

def previous_year(df, company):

    history = (
        df[df["company_id"] == company]
        .sort_values("year")
    )

    if len(history) < 2:
        return None

    return history.iloc[-2]

def kpi_table(latest, previous):

    rows = [
        ["Metric", "Value", "Trend"],
        [
            "Revenue",
            f"{latest['sales']:,.0f}",
            trend_arrow(latest["sales"], previous["sales"])
        ],
        [
            "Net Profit",
            f"{latest['net_profit']:,.0f}",
            trend_arrow(latest["net_profit"], previous["net_profit"])
        ],
        [
            "ROE",
            f"{latest['roe_percentage']:.2f}%",
            trend_arrow(latest["roe_percentage"], previous["roe_percentage"])
        ],
        [
            "ROCE",
            f"{latest['roce_percentage']:.2f}%",
            trend_arrow(latest["roce_percentage"], previous["roce_percentage"])
        ],
        [
            "OPM",
            f"{latest['opm_percentage']:.2f}%",
            trend_arrow(latest["opm_percentage"], previous["opm_percentage"])
        ],
        [
            "Debt / Equity",
            f"{latest['debt_to_equity']:.2f}",
            trend_arrow(latest["debt_to_equity"], previous["debt_to_equity"])
        ],
    ]

    table = Table(rows, colWidths=[2.4*inch, 2*inch, 0.8*inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.navy),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.3, colors.grey),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("ALIGN", (2,1), (2,-1), "CENTER"),
    ]))

    return table

def generate_portfolio_pdf():

    df = load_data()

    latest_df = latest_snapshot(df)

    pdf = SimpleDocTemplate(
        str(OUTPUT_DIR / "portfolio_summary.pdf"),
        pagesize=A4
    )

    story = []

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    for _, latest in latest_df.iterrows():

        previous = previous_year(
            df,
            latest["company_id"]
        )

        if previous is None:
            continue

        story.append(
            Paragraph(
                latest["company_id"],
                title
            )
        )

        story.append(
            Paragraph(
                f"<b>Sector:</b> {latest['broad_sector']}",
                styles["Heading3"]
            )
        )

        story.append(
            Spacer(1, 0.25 * inch)
        )

        story.append(
            kpi_table(latest, previous)
        )

        story.append(
            PageBreak()
        )

    pdf.build(story)

    print("Portfolio Summary Created")


def main():

    generate_portfolio_pdf()

    print("="*50)
    print("Day 35 Completed Successfully")
    print("="*50)


if __name__ == "__main__":
    main()    