"""
Sprint 5 - Day 33
Company Tearsheet Generator

Author: Manish
"""

from pathlib import Path
import sqlite3
import re
import numpy as np
from matplotlib import pyplot as plt
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
CHART_DIR.mkdir(
    parents=True,
    exist_ok=True
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)
TEARSHEET_DIR = OUTPUT_DIR / "tearsheets"
SECTOR_DIR = OUTPUT_DIR / "sector"

TEARSHEET_DIR.mkdir(parents=True, exist_ok=True)
SECTOR_DIR.mkdir(parents=True, exist_ok=True)
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


def company_snapshot(df, company):

    history = company_history(df, company)

    latest = history.iloc[-1]

    return {

    "company": company,

    "sector": safe_value(latest, "broad_sector"),

    "revenue": safe_value(latest, "sales", 0),

    "net_profit": safe_value(latest, "net_profit", 0),

    "eps": safe_value(latest, "eps", 0),

    "roe": safe_value(latest, "roe_percentage"),

    "roce": safe_value(latest, "roce_percentage"),

    "opm": safe_value(latest, "opm_percentage"),

    "capital_allocation": safe_value(
        latest,
        "capital_allocation",
        "Unknown"
    )

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
def balance_history(df, company):

    history = company_history(df, company).tail(10)

    years = history["year"]

    equity = history["equity_capital"]

    debt = history["borrowings"]

    liabilities = history["other_liabilities"]

    return years, equity, debt, liabilities
def cashflow_history(df, company):

    history = company_history(df, company).tail(10)

    years = history["year"]

    operating = history["operating_activity"]

    investing = history["investing_activity"]

    financing = history["financing_activity"]

    return years, operating, investing, financing

from reportlab.lib.enums import TA_CENTER

def insight_card(title, items, header_color):

    if not items:
        items = ["No insights available"]

    title_para = Paragraph(
        f"<font color='white'><b>{title}</b></font>",
        ParagraphStyle(
            "CardTitle",
            parent=BODY_STYLE,
            alignment=TA_CENTER
        )
    )

    body = []

    for item in items:
        body.append(
            Paragraph(
                f"• {item}",
                BODY_STYLE
            )
        )

    rows = [[title_para]]

    for p in body:
        rows.append([p])

    table = Table(
        rows,
        colWidths=[3.2 * inch]
    )

    table.setStyle(TableStyle([

        ("BACKGROUND", (0,0), (-1,0), header_color),

        ("TEXTCOLOR", (0,0), (-1,0), colors.white),

        ("GRID", (0,0), (-1,-1), 0.5, colors.lightgrey),

        ("BOX", (0,0), (-1,-1), 1, colors.grey),

        ("BOTTOMPADDING", (0,0), (-1,0), 8),

        ("TOPPADDING", (0,0), (-1,0), 8),

        ("BOTTOMPADDING", (0,1), (-1,-1), 6),

        ("TOPPADDING", (0,1), (-1,-1), 6),

        ("VALIGN", (0,0), (-1,-1), "TOP")

    ]))

    return table    
def insights_section(pros, cons):

    pros_card = insight_card(
        "PROS",
        pros,
        colors.darkgreen
    )

    cons_card = insight_card(
        "CONS",
        cons,
        colors.darkred
    )

    table = Table(
        [[pros_card, cons_card]],
        colWidths=[3.3*inch,3.3*inch]
    )

    table.setStyle(TableStyle([

        ("VALIGN",(0,0),(-1,-1),"TOP"),

        ("BOTTOMPADDING",(0,0),(-1,-1),10)

    ]))

    return table
def capital_badge(snapshot):

    label = snapshot.get("capital_allocation", "Unknown")

    palette = {

        "Reinvestor": colors.darkgreen,

        "Mixed": colors.orange,

        "Growth Funded by Debt": colors.blue,

        "Liquidating Assets": colors.red,

        "Distress Signal": colors.darkred,

        "Pre-Revenue": colors.purple,

        "Unknown": colors.grey

    }

    badge = Table(

        [[Paragraph(

            f"<font color='white'><b>{label}</b></font>",

            BODY_STYLE

        )]],

        colWidths=[2.8*inch]

    )

    badge.setStyle(TableStyle([

        ("BACKGROUND",(0,0),(-1,-1),

         palette.get(label, colors.grey)),

        ("ALIGN",(0,0),(-1,-1),"CENTER"),

        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),

        ("TOPPADDING",(0,0),(-1,-1),10),

        ("BOTTOMPADDING",(0,0),(-1,-1),10),

        ("BOX",(0,0),(-1,-1),1,colors.black)

    ]))

    return badge
PROS_CONS_FILE = OUTPUT_DIR.parent / "pros_cons_generated.csv"

PROS_CONS_FILE = OUTPUT_DIR.parent / "pros_cons_generated.csv"
def load_pros_cons():

    try:
        return pd.read_csv(PROS_CONS_FILE)

    except FileNotFoundError:

        print(f"Warning: {PROS_CONS_FILE} not found.")

        return pd.DataFrame(
            columns=["company_id", "type", "statement"]
        )

def company_pros_cons(df, company):

    if df.empty:
        return [], []

    company_df = df[df["company_id"] == company]

    pros = company_df[
        company_df["type"].str.lower() == "pro"
    ]["text"].tolist()

    cons = company_df[
        company_df["type"].str.lower() == "con"
    ]["text"].tolist()

    return pros, cons    
def page2(df, company):

    snapshot = company_snapshot(df, company)

    pc_df = load_pros_cons()

    pros, cons = company_pros_cons(pc_df, company)

    story = []

    # -------------------------------
    # Balance Sheet
    # -------------------------------

    story.append(
        Paragraph(
            "<b>Balance Sheet Composition</b>",
            SUBTITLE_STYLE
        )
    )

    story.append(Spacer(1, 6))

    story.append(balance_section(df, company))

    story.append(Spacer(1, 15))

    # -------------------------------
    # Cash Flow
    # -------------------------------

    story.append(
        Paragraph(
            "<b>Cash Flow Trends</b>",
            SUBTITLE_STYLE
        )
    )

    story.append(Spacer(1, 6))

    story.append(cashflow_section(df, company))

    story.append(Spacer(1, 18))

    # -------------------------------
    # Pros & Cons
    # -------------------------------

    story.append(
        insights_section(
            pros,
            cons
        )
    )

    story.append(Spacer(1, 18))

    # -------------------------------
    # Capital Allocation
    # -------------------------------

    story.append(
        Paragraph(
            "<b>Capital Allocation</b>",
            SUBTITLE_STYLE
        )
    )

    story.append(Spacer(1, 8))

    story.append(
        capital_badge(snapshot)
    )

    return story
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

def balance_chart(df, company):

    years, equity, debt, liabilities = balance_history(df, company)

    x = np.arange(len(years))

    plt.figure(figsize=(6,3))

    plt.bar(x, equity, label="Equity")

    plt.bar(
        x,
        debt,
        bottom=equity,
        label="Debt"
    )

    plt.bar(
        x,
        liabilities,
        bottom=equity + debt,
        label="Other"
    )

    plt.xticks(x, years, rotation=45)

    plt.title("Balance Sheet Composition")

    plt.legend()

    plt.tight_layout()

    path = CHART_DIR / f"{company}_balance.png"

    plt.savefig(path, dpi=200)

    plt.close()

    return str(path)

def cashflow_chart(df, company):

    years, op, inv, fin = cashflow_history(df, company)

    x = np.arange(len(years))

    width = 0.25

    plt.figure(figsize=(6,3))

    plt.bar(x-width, op, width, label="Operating")

    plt.bar(x, inv, width, label="Investing")

    plt.bar(x+width, fin, width, label="Financing")

    plt.xticks(x, years, rotation=45)

    plt.title("Cash Flow")

    plt.legend()

    plt.tight_layout()

    path = CHART_DIR / f"{company}_cashflow.png"

    plt.savefig(path, dpi=200)

    plt.close()

    return str(path)
def safe_chart(chart_func, df, company, width, height):

    try:

        path = chart_func(df, company)

        if Path(path).exists():

            return Image(
                path,
                width=width,
                height=height
            )

    except Exception as e:

        print(f"{company}: {e}")

    return Paragraph(
        "Chart unavailable",
        BODY_STYLE
    )
def safe_value(row, column, default="N/A"):

    if column not in row.index:

        return default

    value = row[column]

    if pd.isna(value):

        return default

    return value
def fmt(value, suffix=""):

    if value == "N/A":

        return "N/A"

    if pd.isna(value):

        return "N/A"

    return f"{value:,.2f}{suffix}"
def balance_section(df, company):

    img = safe_chart(
        balance_chart,
        df,
        company,
        6.6*inch,
        3*inch
    )

    return Table([[img]])
def cashflow_section(df, company):

    img = safe_chart(
        cashflow_chart,
        df,
        company,
        6.6*inch,
        3*inch
    )

    return Table([[img]])
def kpi_grid(snapshot):

    grid = [

        [

            kpi_tile("Revenue", fmt(snapshot["revenue"])),

            kpi_tile("Net Profit", fmt(snapshot["net_profit"])),

            kpi_tile("EPS", fmt(snapshot["eps"]))

        ],

        [

            kpi_tile("ROE", fmt(snapshot["roe"], "%")),

            kpi_tile("ROCE", fmt(snapshot["roce"], "%")),

            kpi_tile("OPM", fmt(snapshot["opm"], "%"))

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
def generate_pdf(company, output_dir=TEARSHEET_DIR):
    df = load_data()

    snapshot = company_snapshot(df, company)

    output_dir.mkdir(parents=True, exist_ok=True)

    pdf = SimpleDocTemplate(
        str(output_dir / f"{company}_tearsheet.pdf"),
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
    story.extend(
        page2(
            df,
            company
        )
    )
    

    pdf.build(story)
def main():

    df = load_data()

    companies = sorted(df["company_id"].dropna().unique())

    skipped = []
    generated = 0

    for company in companies:

        history = company_history(df, company)

        if len(history) < 3:
            skipped.append(company)
            print(f"Skipping {company} (less than 3 years)")
            continue

        try:
            print(f"Generating {company}...")
            generate_pdf(company)
            generated += 1

        except Exception as e:
            print(f"Failed {company}: {e}")
            skipped.append(company)

    pd.DataFrame(
        {"company_id": skipped}
    ).to_csv(
        BASE_DIR / "output" / "skipped_tearsheets.csv",
        index=False
    )

    print("=" * 60)
    print(f"Generated : {generated}")
    print(f"Skipped   : {len(skipped)}")
    print("=" * 60)
    print("Day 34 Batch Tear Sheets Completed!")

# for all companies report
# def main():

#     df = load_data()

#     companies = sorted(df["company_id"].unique())

#     for company in companies:
#         print(f"Generating {company}...")
#         generate_pdf(company)

#     print("=" * 50)
#     print("All tear sheets generated successfully!")
#     print("=" * 50)
if __name__ == "__main__":
    main()



