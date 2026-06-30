from pathlib import Path

OUTPUT = Path("output")
LOG_FILE = OUTPUT / "ratio_edge_cases.log"


def clear_log():
    OUTPUT.mkdir(exist_ok=True)

    with open(LOG_FILE, "w", encoding="utf8") as f:
        f.write("=== Ratio Edge Cases ===\n\n")


def log_edge_case(message):
    with open(LOG_FILE, "a", encoding="utf8") as f:
        f.write(message + "\n")


def compare_ratio(company, year, calculated, source, ratio_name):

    if calculated is None:
        return

    if source is None:
        return

    diff = abs(calculated - source)

    if diff > 5:

        category = "Formula discrepancy"

        if ratio_name == "ROE":
            category = "Source value anomaly"

        log_edge_case(
            f"{company} | {year} | "
            f"{ratio_name} | "
            f"Calculated={round(calculated,2)} | "
            f"Source={round(source,2)} | "
            f"Diff={round(diff,2)} | "
            f"{category}"
        )