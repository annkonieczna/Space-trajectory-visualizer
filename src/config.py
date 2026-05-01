#This file contains all of the constants neccessary for this project 
from pathlib import Path 

#used paths 
PROJECT_ROOT = Path(__file__).resolve().parent.parent
KERNEL_DIR = PROJECT_ROOT / "data" / "kernels"
META_KERNEL = KERNEL_DIR / "meta.tm"

#time settings 
DEFAULT_START_UTC = "2017-04-22T00:00:00" #T as a seperator between date and an hour 
DEFAULT_END_UTC = "2017-09-15T10:00:00"
DEFAULT_STEP_IN_SECONDS = 3600

#Reference frame 

DEFAULT_FRAME = "J2000" #reference frame I'll be using most of the time, it's an inertial reference frame 
#so it's useful for calculating most of the 
DEFAULT_ABCORR = "NONE" #the aberration correction we want to apply 
#in my case I want to have the geometrical state of the object relative to the observer 

CASSINI_NAME = "CASSINI"
SATURN_NAME = "SATURN"
TITAN_NAME = "TITAN"