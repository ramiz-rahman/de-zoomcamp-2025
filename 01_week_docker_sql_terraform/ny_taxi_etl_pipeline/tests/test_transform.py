import pandas as pd
import pytest
from ny_taxi_etl_pipeline.pipeline import transform


# Sample transformation functions
def add_column(df: pd.DataFrame) -> pd.DataFrame:
    df["new_col"] = 1
    return df


def multiply_values(df: pd.DataFrame) -> pd.DataFrame:
    df["value"] = df["value"] * 2
    return df


def filter_rows(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["value"] > 10]


# Test cases
def test_transform_add_column():
    df = pd.DataFrame({"value": [1, 2, 3]})
    transformers = [add_column]
    df_iter = iter([df])

    result_iter = transform(transformers, df_iter)
    result_df = next(result_iter)

    assert "new_col" in result_df.columns
    assert (result_df["new_col"] == 1).all()


def test_transform_composer_multiple_transformations():
    df = pd.DataFrame({"value": [1, 5, 10]})
    transformers = [multiply_values, filter_rows]
    df_iter = iter([df])

    result_iter = transform(transformers, df_iter)
    result_df = next(result_iter)

    assert len(result_df) == 1  # Only one row should satisfy the filter condition
    assert result_df.iloc[0]["value"] == 20


def test_transform_composer_empty_dataframe():
    df = pd.DataFrame(columns=["value"])
    transformers = [add_column]
    df_iter = iter([df])

    result_iter = transform(transformers, df_iter)
    result_df = next(result_iter)

    assert result_df.empty
    assert "new_col" in result_df.columns
