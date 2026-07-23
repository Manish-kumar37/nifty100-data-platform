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
)

from src.reports.tearsheet import load_data

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "output" / "reports" / "sector"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
df = load_data()
print(df["broad_sector"].dropna().nunique())
print(sorted(df["broad_sector"].dropna().unique()))
def latest_snapshot(df):

    latest = (
        df.sort_values("year")
        .groupby("company_id")
        .tail(1)
        .copy()
    )

    return latest

def sector_summary(df):

    return {

        "Companies": len(df),

        "Median Revenue": df["sales"].median(),

        "Median Net Profit": df["net_profit"].median(),

        "Median ROE": df["roe_percentage"].median(),

        "Median ROCE": df["roce_percentage"].median(),

        "Median OPM": df["opm_percentage"].median(),

        "Median Debt/Equity": df["debt_to_equity"].median(),

        "Median Interest Coverage": df["interest_coverage"].median(),

        "Median FCF": df["free_cash_flow_cr"].median(),

        
    }
   
def generate_sector_pdf(df, sector):

    sector_df = df[df["broad_sector"] == sector].copy()

    summary = sector_summary(sector_df)

    pdf = SimpleDocTemplate(
        str(OUTPUT_DIR / f"{sector}_report.pdf"),
        pagesize=A4
    )

    story = []

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    story.append(
        Paragraph(f"{sector} Sector Report", title)
    )

    story.append(Spacer(1, 0.3 * inch))

    data = [["Metric", "Value"]]

    for key, value in summary.items():

        data.append([key, f"{value:,.2f}" if isinstance(value, (int, float)) else value])

    table = Table(data, colWidths=[3*inch, 2.5*inch])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.navy),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND", (0,1), (-1,-1), colors.beige),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
    ]))

    

    print(f"Created {sector}")
    story.append(Spacer(1, 0.4 * inch))

    story.append(
        Paragraph("Companies", styles["Heading2"])
    )
    table_data = [[
        "Company",
        "Revenue",
        "Net Profit",
        "ROE",
        "ROCE",
        "OPM",
        "D/E",
        "Interest",
        "FCF"
    ]]

    for _, row in sector_df.iterrows():

        table_data.append([
            row["company_id"],
            f"{row['sales']:,.0f}",
            f"{row['net_profit']:,.0f}",
            f"{row['roe_percentage']:.2f}",
            f"{row['roce_percentage']:.2f}",
            f"{row['opm_percentage']:.2f}",
            f"{row['debt_to_equity']:.2f}",
            f"{row['interest_coverage']:.2f}",
            f"{row['free_cash_flow_cr']:,.0f}",
        ])
    company_table = Table(table_data, repeatRows=1)

    company_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.darkblue),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.25, colors.grey),
        ("FONTSIZE", (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,0), 6),
    ]))

    story.append(company_table)
    story.append(table)
    
    pdf.build(story)

def main():

    df = load_data()

    df = latest_snapshot(df)

    sectors = sorted(
        df["broad_sector"].dropna().unique()
    )

    for sector in sectors:

        generate_sector_pdf(df, sector)

    print("="*50)
    print("Sector Reports Generated")
    print("="*50)


if __name__ == "__main__":
    main()    