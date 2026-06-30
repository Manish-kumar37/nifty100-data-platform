from src.etl.normaliser import normalize_ticker


def test_uppercase():
    assert normalize_ticker("hdfcbank") == "HDFCBANK"


def test_strip_spaces():
    assert normalize_ticker("  infy  ") == "INFY"


def test_mixed_case():
    assert normalize_ticker("ReLiAnCe") == "RELIANCE"


def test_none():
    assert normalize_ticker(None) is None


def test_empty_string():
    assert normalize_ticker("") == ""


def test_bankbaroda():
    assert normalize_ticker("bankbaroda") == "BANKBARODA"


def test_tcs():
    assert normalize_ticker("tcs") == "TCS"


def test_axisbank():
    assert normalize_ticker("axisbank") == "AXISBANK"


def test_with_newline():
    assert normalize_ticker("infy\n") == "INFY"


def test_with_tab():
    assert normalize_ticker("  tcs\t") == "TCS"


def test_already_clean():
    assert normalize_ticker("SBIN") == "SBIN"


def test_hyphen():
    assert normalize_ticker("bajaj-auto") == "BAJAJ-AUTO"


def test_ltim():
    assert normalize_ticker("ltim") == "LTIM"


def test_jswsteel():
    assert normalize_ticker("jswsteel") == "JSWSTEEL"


def test_powergrid():
    assert normalize_ticker("powergrid") == "POWERGRID"