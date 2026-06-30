import pandas as pd
from pathlib import Path

OUTPUT_DIR = Path("output")


def save_load_audit(audit_rows):

    OUTPUT_DIR.mkdir(exist_ok=True)

    df = pd.DataFrame(audit_rows)

    df.to_csv(
        OUTPUT_DIR / "load_audit.csv",
        index=False
    )

    print("load_audit.csv created")