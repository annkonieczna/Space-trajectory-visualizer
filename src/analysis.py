from typing import cast

import numpy as np
import pandas as pd

SECONDS_IN_A_DAY: float = 86400.0  # number of seconds in a day


def add_relative_days(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds column with a number of days from the beggining of the analysis
    """
    df = df.copy()
    start_et = df["et"].iloc[0]
    df["days_from_start"] = (df["et"] - start_et) / SECONDS_IN_A_DAY
    return df


def find_global_min(df: pd.DataFrame, column: str = "distance_km") -> pd.Series:
    """
    Returns row with a global minimum.
    """
    idx = df[column].idxmin()
    return cast(pd.Series, df.loc[idx])


def find_global_max(df: pd.DataFrame, column: str = "distance_km") -> pd.Series:
    """
    Returns row with global maximum
    """
    idx = df[column].idxmax()
    return cast(pd.Series, df.loc[idx])


def build_distance_dataframe(
    df_a: pd.DataFrame, df_b: pd.DataFrame, label: str
) -> pd.DataFrame:
    """Function that is given dwo dataframes and it calculates the distance between
    two objects in the same reference frame and are relative to the same observer
    data frame looks like: et utc x y z"""
    coords_a = df_a[["x_km", "y_km", "z_km"]].to_numpy()
    coords_b = df_b[["x_km", "y_km", "z_km"]].to_numpy()
    distances = np.linalg.norm(
        coords_a - coords_b, axis=1
    )  # calculates difference between vectors for every row
    new_df = pd.DataFrame(
        {"et": df_a["et"], "utc": df_a["utc"], "distance_km": distances}
    )
    new_df["pair"] = label
    return add_relative_days(new_df)
