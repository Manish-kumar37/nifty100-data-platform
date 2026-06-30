from src.etl.normaliser import normalize_year


def test_mar_2024():
    assert normalize_year("Mar 2024") == "Mar 2024"


def test_mar_2019():
    assert normalize_year("Mar 2019") == "Mar 2019"


def test_dec_2018():
    assert normalize_year("Dec 2018") == "Dec 2018"


def test_ttm():
    assert normalize_year("TTM") == "TTM"


def test_strip_spaces():
    assert normalize_year("  Mar 2024  ") == "Mar 2024"


def test_none():
    assert normalize_year(None) is None


def test_empty():
    assert normalize_year("") == ""


def test_mar_2010():
    assert normalize_year("Mar 2010") == "Mar 2010"


def test_mar_2011():
    assert normalize_year("Mar 2011") == "Mar 2011"


def test_mar_2012():
    assert normalize_year("Mar 2012") == "Mar 2012"


def test_mar_2013():
    assert normalize_year("Mar 2013") == "Mar 2013"


def test_mar_2014():
    assert normalize_year("Mar 2014") == "Mar 2014"


def test_mar_2015():
    assert normalize_year("Mar 2015") == "Mar 2015"


def test_mar_2016():
    assert normalize_year("Mar 2016") == "Mar 2016"


def test_mar_2017():
    assert normalize_year("Mar 2017") == "Mar 2017"


def test_mar_2018():
    assert normalize_year("Mar 2018") == "Mar 2018"


def test_mar_2020():
    assert normalize_year("Mar 2020") == "Mar 2020"


def test_mar_2021():
    assert normalize_year("Mar 2021") == "Mar 2021"


def test_mar_2022():
    assert normalize_year("Mar 2022") == "Mar 2022"


def test_mar_2023():
    assert normalize_year("Mar 2023") == "Mar 2023"