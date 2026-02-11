import pandas as pd
from main import add_virtual_column


def test_operator_precedence():
    """Test that standard mathematical precedence is respected (multiplication before addition)."""
    df = pd.DataFrame([[10, 2, 5]] * 2, columns=["A", "B", "C"])
    # 10 + (2 * 5) = 20, NOT (10 + 2) * 5 = 60
    df_expected = pd.DataFrame([[10, 2, 5, 20]] * 2, columns=["A", "B", "C", "D"])
    
    df_result = add_virtual_column(df, "A + B * C", "D")
    assert df_result.equals(df_expected), (
        f"Multiplication should take precedence over addition.\n"
        f"Expected:\n{df_expected}\nResult:\n{df_result}"
    )


def test_syntax_error_in_role():
    """Test that syntactically invalid roles (despite valid characters) return an empty DataFrame."""
    df = pd.DataFrame([[1, 1]] * 2, columns=["A", "B"])
    # "A + * B" contains only allowed chars but is invalid syntax
    df_result = add_virtual_column(df, "A + * B", "C")
    assert df_result.empty, "Should return empty DataFrame for invalid syntax 'A + * B'"


def test_numeric_literals_rejected():
    """Test that roles containing numbers (not allowed in column labels) are rejected."""
    df = pd.DataFrame([[10]] * 2, columns=["A"])
    # Digits are not in the allowed regex [a-zA-Z_]
    df_result = add_virtual_column(df, "A * 10", "B")
    assert df_result.empty, "Should return empty DataFrame when role contains numbers/literals."


def test_invalid_new_column_name():
    """Test validation for the new_column argument."""
    df = pd.DataFrame([[1, 1]], columns=["A", "B"])
    
    # Case 1: Contains number
    res_num = add_virtual_column(df, "A + B", "C1")
    assert res_num.empty, "Should fail if new_column contains numbers."
    
    # Case 2: Contains hyphen
    res_hyphen = add_virtual_column(df, "A + B", "C-new")
    assert res_hyphen.empty, "Should fail if new_column contains special characters."


def test_column_missing_in_dataframe():
    """Test that using a validly named column that doesn't exist in the DF fails."""
    df = pd.DataFrame([[1]], columns=["A"])
    # 'B' is a valid label format, but not in df.columns
    df_result = add_virtual_column(df, "A + B", "C")
    assert df_result.empty, "Should fail if a column in role does not exist in the DataFrame."


def test_no_identifiers_in_role():
    """Test roles that contain operators but no column names."""
    df = pd.DataFrame([[1]], columns=["A"])
    df_result = add_virtual_column(df, " + ", "B")
    assert df_result.empty, "Should fail if role contains no column identifiers."


def test_case_sensitivity():
    """Test that column matching is case-sensitive."""
    df = pd.DataFrame([[1, 2]], columns=["ColA", "ColB"])
    # 'cola' is valid format but different from 'ColA'
    df_result = add_virtual_column(df, "cola + ColB", "ColC")
    assert df_result.empty, "Should be case-sensitive regarding column names."
