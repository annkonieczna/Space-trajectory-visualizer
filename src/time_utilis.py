import spiceypy as spice
import numpy as np
from typing import cast


def utc_to_et(utc_str: str) -> float:
    """Converts time given by the user to Ephemeris Time used by SPICE"""
    return cast(float, spice.str2et(utc_str))


def et_to_utc(
    et: float, format_str: str = "ISOC", prec: int = 3
) -> str:  # ISOC - ISO Calendar (standard format)
    """the oppsite conversion"""
    return cast(str, spice.et2utc(et, format_str, prec))


def generate_et_range(utc_start: str, utc_end: str, step_seconds: int) -> np.ndarray:
    """Generates range of time in ET format"""
    start = utc_to_et(utc_start)
    stop = utc_to_et(utc_end)
    return np.arange(start, stop + step_seconds, step_seconds)
