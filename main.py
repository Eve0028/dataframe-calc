import re
import pandas as pd


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
    Creates a new DataFrame with an additional virtual column calculated based
    on the specified mathematical role.

    :param df: The input pandas DataFrame.
    :param role: A string defining the mathematical expression (e.g., 'col_a + col_b').
                 Supported operations are addition (+), subtraction (-), and multiplication (*).
    :param new_column: The name of the new virtual column to be added.
    :return: A new DataFrame with the computed column included. Returns an empty DataFrame
             if the validation of labels or the role fails.
    """
    # STEP - Validate new_column label
    # Must consist only of letters (a-z, A-Z) and underscores (_).
    if not re.fullmatch(r"[a-zA-Z_]+", new_column):
        return pd.DataFrame([])

    # STEP - Validate role string characters
    # Allowed: letters, underscores, whitespace, and operators (+, -, *).
    # This implicitly rejects numbers/digits, division (/), and other symbols.
    if not re.fullmatch(r"[a-zA-Z_\s\+\-\*]+", role):
        return pd.DataFrame([])

    # STEP - Validate existence of referenced columns
    # Extract all potential column names (identifiers) from the role.
    columns_in_role = re.findall(r"[a-zA-Z_]+", role)

    if not columns_in_role:
        # Reject roles that contain no column references (e.g., just operators " + ").
        return pd.DataFrame([])

    # Check if all extracted columns actually exist in the provided DataFrame.
    if not set(columns_in_role).issubset(df.columns):
        return pd.DataFrame([])

    # STEP - Perform calculation
    try:
        # Create a copy to prevent mutation of the original DataFrame.
        df_result = df.copy()

        # Use pandas.DataFrame.eval for efficient computation.
        df_result[new_column] = df_result.eval(role)

        return df_result

    except (SyntaxError, ValueError, TypeError, pd.errors.UndefinedVariableError):
        # Catch operational errors, such as malformed math syntax (e.g., "col_a + * col_b")
        # that passed the character validation but is not valid Python/math.
        return pd.DataFrame([])
