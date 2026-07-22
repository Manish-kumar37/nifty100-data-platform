"""
Sprint 5 - Day 33
Company Tearsheet Generator

Author: Manish
"""

from pathlib import Path
import sqlite3
import re

import pandas as pd

import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from reportlab.lib.units import inch

from reportlab.lib.pagesizes import A4

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)

from reportlab.graphics.shapes import Drawing
import sqlite3
import pandas as pd

# conn = sqlite3.connect("nifty100.db")
# df = pd.read_sql("SELECT * FROM financial_ratios LIMIT 1", conn)
# print(df.columns.tolist())
# conn.close()
BASE_DIR = Path(".")

DB_FILE = BASE_DIR / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "output" / "reports"

CHART_DIR = BASE_DIR / "assets" / "charts"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
CHART_DIR.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#0B1F3A")

LIGHT_BLUE = colors.HexColor("#EAF2FF")

GREEN = colors.HexColor("#16A34A")

RED = colors.HexColor("#DC2626")

GREY = colors.HexColor("#555555")

WHITE = colors.white

styles = getSampleStyleSheet()

TITLE_STYLE = ParagraphStyle(
    "TITLE",
    parent=styles["Heading1"],
    fontSize=20,
    alignment=TA_CENTER,
    textColor=WHITE,
)

SUBTITLE_STYLE = ParagraphStyle(
    "SUBTITLE",
    parent=styles["Heading2"],
    fontSize=12,
    alignment=TA_LEFT,
)

BODY_STYLE = ParagraphStyle(
    "BODY",
    parent=styles["BodyText"],
    fontSize=10,
    leading=14,
)

SMALL_STYLE = ParagraphStyle(
    "SMALL",
    parent=styles["BodyText"],
    fontSize=8,
)

def load_data():

    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn,
    )

    conn.close()

    return df

def extract_year(year):

    match = re.search(r"\d{4}", str(year))

    return int(match.group()) if match else 0    

def company_history(df, company):

    temp = df[
        df["company_id"] == company
    ].copy()

    temp["sort_year"] = temp["year"].apply(extract_year)

    temp = temp.sort_values("sort_year")

    return temp

def latest_company(df, company):

    history = company_history(df, company)

    return history.iloc[-1]

def header(snapshot):

    title = f"""
    <font size=20><b>{snapshot['company']}</b></font><br/>
    <font size=11>{snapshot['sector']}</font>
    """

    table = Table(
        [[Paragraph(title, TITLE_STYLE)]],
        colWidths=[7.2 * inch]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), NAVY),
            ("TEXTCOLOR", (0,0), (-1,-1), WHITE),
            ("ALIGN", (0,0), (-1,-1), "CENTER"),
            ("TOPPADDING", (0,0), (-1,-1), 16),
            ("BOTTOMPADDING", (0,0), (-1,-1), 16),
        ])
    )

    return table


def kpi_tile(title, value):

    data = [

        [

            Paragraph(

                f"<b>{title}</b>",

                SMALL_STYLE,

            )

        ],

        [

            Paragraph(

                str(value),

                SUBTITLE_STYLE,

            )

        ],

    ]

    table = Table(

        data,

        colWidths=2.2 * inch,

        rowHeights=[0.3 * inch, 0.45 * inch],

    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),

            ("BOX", (0, 0), (-1, -1), 0.5, colors.black),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

        ])

    )

    return table

def generate_pdf(company):

    df = load_data()

    snapshot = company_snapshot(df, company)

    pdf = SimpleDocTemplate(
        str(OUTPUT_DIR / f"{company}.pdf"),
        pagesize=A4,
        topMargin=20,
        bottomMargin=20,
    )

    story = []

    # HEADER
    story.append(header(snapshot))

    story.append(Spacer(1,18))

    # KPI GRID

    story.append(kpi_grid(snapshot))

    story.append(Spacer(1,18))

    # REVENUE + PROFIT

    story.append(chart_row(df, company))

    story.append(Spacer(1,18))

    # ROE ROCE

    story.append(performance_chart(df, company))

    # PAGE 2 PLACEHOLDER

    story.append(PageBreak())

    story.append(
        Paragraph(
            "<b>Page 2 (Coming in Part 3)</b>",
            SUBTITLE_STYLE
        )
    )

    pdf.build(story)
def company_snapshot(df, company):

    history = company_history(df, company)

    latest = history.iloc[-1]

    return {

        "company": company,

        "sector": latest["broad_sector"],

        "revenue": latest["sales"],

        "net_profit": latest["net_profit"],

        "eps": latest["eps"],

        "roe": latest["roe_percentage"],

        "roce": latest["roce_percentage"],

        "opm": latest["opm_percentage"]

    }
def revenue_history(df, company):

    history = company_history(df, company)

    history = history.tail(10)

    return history["year"], history["sales"]
def profit_history(df, company):

    history = company_history(df, company)

    history = history.tail(10)

    return history["year"], history["net_profit"]
def roe_history(df, company):

    history = company_history(df, company)

    history = history.tail(10)

    return history["year"], history["roe_percentage"]
def roce_history(df, company):

    history = company_history(df, company)

    history = history.tail(10)

    return history["year"], history["roce_percentage"]
def revenue_chart(df, company):

    years, revenue = revenue_history(df, company)

    plt.figure(figsize=(5,3))

    plt.bar(years, revenue)

    plt.title("Revenue")

    plt.xticks(rotation=45)

    plt.tight_layout()

    path = CHART_DIR / f"{company}_revenue.png"

    plt.savefig(path)

    plt.close()

    return str(path)
def profit_chart(df, company):

    years, profit = profit_history(df, company)

    plt.figure(figsize=(5,3))

    plt.bar(years, profit)

    plt.title("Net Profit")

    plt.xticks(rotation=45)

    plt.tight_layout()

    path = CHART_DIR / f"{company}_profit.png"

    plt.savefig(path)

    plt.close()

    return str(path)
def roe_roce_chart(df, company):

    years, roe = roe_history(df, company)

    _, roce = roce_history(df, company)

    plt.figure(figsize=(6,3))

    plt.plot(years, roe, marker="o", label="ROE")

    plt.plot(years, roce, marker="s", label="ROCE")

    plt.legend()

    plt.xticks(rotation=45)

    plt.tight_layout()

    path = CHART_DIR / f"{company}_roe_roce.png"

    plt.savefig(path)

    plt.close()

    return str(path)
def kpi_grid(snapshot):

    grid = [

        [

            kpi_tile("Revenue", f"{snapshot['revenue']:.2f}"),

            kpi_tile("Net Profit", f"{snapshot['net_profit']:.2f}"),

            kpi_tile("EPS", f"{snapshot['eps']:.2f}")

        ],

        [

            kpi_tile("ROE", f"{snapshot['roe']:.2f}%"),

            kpi_tile("ROCE", f"{snapshot['roce']:.2f}%"),

            kpi_tile("OPM", f"{snapshot['opm']:.2f}%")

        ]

    ]

    table = Table(

        grid,

        colWidths=[2.2*inch]*3

    )

    table.setStyle(

        TableStyle([

            ("BOTTOMPADDING",(0,0),(-1,-1),10),

            ("TOPPADDING",(0,0),(-1,-1),10),

            ("ALIGN",(0,0),(-1,-1),"CENTER")

        ])

    )

    return table

def chart_row(df, company):

    revenue = Image(
        revenue_chart(df, company),
        width=3.2*inch,
        height=2.2*inch
    )

    profit = Image(
        profit_chart(df, company),
        width=3.2*inch,
        height=2.2*inch
    )

    table = Table(
        [[revenue, profit]],
        colWidths=[3.4*inch,3.4*inch]
    )

    table.setStyle(
        TableStyle([
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("BOTTOMPADDING",(0,0),(-1,-1),12)
        ])
    )

    return table
def performance_chart(df, company):

    img = Image(
        roe_roce_chart(df, company),
        width=6.6*inch,
        height=2.8*inch
    )

    table = Table([[img]])

    table.setStyle(
        TableStyle([
            ("ALIGN",(0,0),(-1,-1),"CENTER")
        ])
    )

    return table
def main():
    generate_pdf("TCS")
    print("=" * 50)
    print("Page 1 Generated Successfully")
    print("=" * 50)

if __name__ == "__main__":
    main()



