import re
import pandas as pd


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
