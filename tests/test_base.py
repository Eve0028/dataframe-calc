import pandas as pd
from main import add_virtual_column


def test_sum_of_two_columns(base_df: pd.DataFrame) -> None:
    """Test standard addition of two columns."""
    df_expected = pd.DataFrame(
        [[1, 1, 2]] * 2, columns=["label_one", "label_two", "label_three"]
    )
    df_result = add_virtual_column(base_df, "label_one+label_two", "label_three")

    error_msg = (
        f"The function should sum the columns: label_one and label_two.\n\n"
        f"Result:\n{df_result}\n\nExpected:\n{df_expected}"
    )
    assert df_result.equals(df_expected), error_msg


def test_multiplication_of_two_columns(base_df: pd.DataFrame) -> None:
    """Test standard multiplication of two columns."""
    df_expected = pd.DataFrame(
        [[1, 1, 1]] * 2, columns=["label_one", "label_two", "label_three"]
    )
    df_result = add_virtual_column(base_df, "label_one * label_two", "label_three")

    error_msg = (
        f"The function should multiply the columns: label_one and label_two.\n\n"
        f"Result:\n{df_result}\n\nExpected:\n{df_expected}"
    )
    assert df_result.equals(df_expected), error_msg


def test_subtraction_of_two_columns(base_df: pd.DataFrame) -> None:
    """Test standard subtraction of two columns."""
    df_expected = pd.DataFrame(
        [[1, 1, 0]] * 2, columns=["label_one", "label_two", "label_three"]
    )
    df_result = add_virtual_column(base_df, "label_one - label_two", "label_three")

    error_msg = (
        f"The function should subtract the columns: label_one and label_two.\n\n"
        f"Result:\n{df_result}\n\nExpected:\n{df_expected}"
    )
    assert df_result.equals(df_expected), error_msg


def test_empty_result_when_invalid_labels() -> None:
    """Test that function returns empty DataFrame when new column name is invalid."""
    df = pd.DataFrame([[1, 2]] * 3, columns=["label_one", "label_two"])
    # 'label3' might be considered invalid in your regex logic (if strictly letters/underscores)
    # or purely intended as a specific failure case.
    df_result = add_virtual_column(df, "label_one + label_two", "label3")

    error_msg = (
        f"Should return an empty df when the 'new_column' is invalid.\n\n"
        f"Result:\n{df_result}\n\nExpected:\nEmpty df"
    )
    assert df_result.empty, error_msg


def test_empty_result_when_invalid_rules(base_df: pd.DataFrame) -> None:
    """Test validation of the mathematical role string."""
    # Case 1: Invalid character '&'
    df_result = add_virtual_column(base_df, "label&one + label_two", "label_three")
    assert df_result.empty, (
        f"Should return empty df when role has invalid char '&'.\n"
        f"Result:\n{df_result}"
    )

    # Case 2: Column not present in DataFrame
    df_result = add_virtual_column(base_df, "label_five + label_two", "label_three")
    assert df_result.empty, (
        f"Should return empty df when role has missing column 'label_five'.\n"
        f"Result:\n{df_result}"
    )


def test_when_extra_spaces_in_rules(base_df: pd.DataFrame) -> None:
    """Test that extra whitespace in the role string is handled correctly."""
    df_expected = pd.DataFrame(
        [[1, 1, 2]] * 2, columns=["label_one", "label_two", "label_three"]
    )

    # Case 1: Space inside expression
    df_result = add_virtual_column(base_df, "label_one + label_two ", "label_three")
    assert df_result.equals(df_expected), (
        f"Should work with trailing spaces in operation.\nResult:\n{df_result}"
    )

    # Case 2: Leading/Trailing spaces
    df_result = add_virtual_column(base_df, "  label_one + label_two ", "label_three")
    assert df_result.equals(df_expected), (
        f"Should work with extra start/end spaces.\nResult:\n{df_result}"
    )
