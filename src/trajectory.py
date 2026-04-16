import spiceypy as spice 
import numpy as np 
import pandas as pd 

from time_utilis import et_to_utc
from config import DEFAULT_FRAME,DEFAULT_ABCORR
from typing import cast

#Function that deteminess the state of our targetin reference too the observer for a specific moment in time  
#It returns a vector [x,y,z,vx,vy,vz] (position and velocity vector), and float light_time-- one way light time between the observer and target in seconds 
#Units are km and km/sec and sec 

def get_state_at_epoch(
        target: str, 
        et:float,
        observer: str,
        frame: str = DEFAULT_FRAME, 
        abcorr: str  = DEFAULT_ABCORR,
) -> tuple[np.ndarray,float]:
    state, light_time = spice.spkezr(target,et,frame,abcorr,observer)
    return np.array(state),cast(float,light_time) 
        


def get_states_over_time(
        target: str,
        observer: str,
        ets: np.ndarray,
        frame: str = DEFAULT_FRAME,
        abcorr: str = DEFAULT_ABCORR,
) -> tuple[np.ndarray,np.ndarray]:
    states = []
    light_times = []
    for et in ets: 
        state, lt = get_state_at_epoch(target,et,frame,abcorr,observer)
        states.append(state)
        light_times.append(lt)
    return np.array(states),np.array(light_times)
    



