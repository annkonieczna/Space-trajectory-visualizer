import spiceypy as spice 
import numpy as np 
import pandas as pd 

from time_utilis import et_to_utc
from config import DEFAULT_FRAME,DEFAULT_ABCORR
from typing import cast


def get_state_at_epoch(
        target: str, 
        et:float,
        observer: str,
        frame: str = DEFAULT_FRAME, 
        abcorr: str  = DEFAULT_ABCORR,
) -> tuple[np.ndarray,float]:
    '''Function that detemines the state of our targetin reference too the observer for a specific moment in time  
    It returns a vector [x,y,z,vx,vy,vz] (position and velocity vector), and float light_time-- one way light time between the observer and target in seconds 
    Units are km and km/sec and sec '''
    state, light_time = spice.spkezr(target,et,frame,abcorr,observer)
    return np.array(state),cast(float,light_time) 
        


def get_states_over_time(
        target: str,
        ets: np.ndarray,
        observer: str,
        frame: str = DEFAULT_FRAME,
        abcorr: str = DEFAULT_ABCORR,
) -> tuple[np.ndarray,np.ndarray]:
    '''The same function as above but for a period of time'''
    states = []
    light_times = []
    for et in ets: 
        state, lt = get_state_at_epoch(target,et,observer,frame,abcorr)
        states.append(state)
        light_times.append(lt)
    return np.array(states),np.array(light_times)
    
def build_trajectory_dataframe(
    target: str,
    observer: str,
    ets: np.ndarray,
    frame: str = DEFAULT_FRAME,
    abcorr: str = DEFAULT_ABCORR,
) -> pd.DataFrame:
    """
    Build DataFrame with position, velocity and distance.
    """
    states, light_times = get_states_over_time(target, ets, observer, frame, abcorr)

    positions = states[:, :3]
    velocities = states[:, 3:]

    distances = np.linalg.norm(positions, axis=1)
    utc_times = [et_to_utc(et) for et in ets]

    df = pd.DataFrame(
        {
            "et": ets,
            "utc": utc_times,
            "x_km": positions[:, 0],
            "y_km": positions[:, 1],
            "z_km": positions[:, 2],
            "vx_km_s": velocities[:, 0],
            "vy_km_s": velocities[:, 1],
            "vz_km_s": velocities[:, 2],
            "light_time_s": light_times,
            "distance_km": distances,
        }
    )

    return df


