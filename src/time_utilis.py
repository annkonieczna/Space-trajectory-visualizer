import spiceypy as spice 
import numpy as np 
from typing import cast 

def utc_to_et(utc_str: str) -> float: 
    '''Converts time given by the user to Ephemeris Time used by SPICE '''
    return cast(float,spice.str2et(utc_str))


def et_to_utc(et: float, format_str: str = "ISOC",  prec: int = 3) -> str: #ISOC - ISO Calendar (standard format)
    '''the oppsite conversion'''
    return cast(str,spice.et2utc(et,format_str,prec))





