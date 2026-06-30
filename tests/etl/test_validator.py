import pandas as pd

from src.etl.validator import (
    check_primary_key_uniqueness,
    check_duplicate_company_year
)


def test_pk_duplicates():

    df = pd.DataFrame({
        "id": ["A", "A", "B"]
    })

    result = check_primary_key_uniqueness(
        df,
        "id",
        "companies"
    )

    assert len(result) == 2


def test_company_year_duplicates():

    df = pd.DataFrame({
        "company_id": ["A", "A", "B"],
        "year": ["2024", "2024", "2023"]
    })

    result = check_duplicate_company_year(
        df,
        "profitandloss"
    )

    assert len(result) == 2