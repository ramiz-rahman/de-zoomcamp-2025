import pandas as pd
from .utils import log_step


### Transformers
@log_step
def transform_pickup_dropoff_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts the 'lpep_pickup_datetime' and 'lpep_dropoff_datetime' columns
    from string format to pandas datetime format.

    Args:
        df (pd.DataFrame): The input DataFrame containing pickup and dropoff columns
                          as strings.

    Returns:
        pd.DataFrame: A DataFrame with the 'lpep_pickup_datetime' and
                      'lpep_dropoff_datetime' columns converted to datetime objects.

    Raises:
        KeyError: If the required columns are not present in the DataFrame.
        ValueError: If the column values cannot be converted to datetime.
    """
    transformed_df = df.assign(
        lpep_pickup_datetime=pd.to_datetime(df["lpep_pickup_datetime"]),
        lpep_dropoff_datetime=pd.to_datetime(df["lpep_dropoff_datetime"]),
    )
    return transformed_df
