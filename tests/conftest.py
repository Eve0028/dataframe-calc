import pytest
import pandas as pd


@pytest.fixture
def base_df():
    return pd.DataFrame([[1, 1]] * 2, columns=["label_one", "label_two"])
