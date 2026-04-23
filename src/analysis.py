import pandas as pd
from typing import cast

SECONDS_IN_A_DAY:float = 86400.0 # number of seconds in a day 

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
    return cast(pd.Series,df.loc[idx]) 


def find_global_max(df: pd.DataFrame, column: str = "distance_km") -> pd.Series:
    """
    Returns row with global maximum 
    """
    idx = df[column].idxmax()
    return  cast(pd.Series,df.loc[idx]) 
