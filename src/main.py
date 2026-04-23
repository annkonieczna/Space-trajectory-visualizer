from pathlib import Path 

from config import(
        META_KERNEL,
        DEFAULT_START_UTC,
        DEFAULT_END_UTC,
        DEFAULT_STEP_IN_SECONDS,
        DEFAULT_FRAME,
        DEFAULT_ABCORR,
        CASSINI_NAME,
        SATURN_NAME,
        TITAN_NAME,
)
from spice_loader import clear_kernels,load_kernels
from time_utilis import generate_et_range
from trajectory import build_trajectory_dataframe
from analysis import (
    add_relative_days,
    find_global_max,
    find_global_min,
    build_distance_dataframe
)

from visualization import (
    plot_trajectory_3d,
    ensure_output_dir
)

def main() -> None:
    output_dir = Path("data/output/plots/figures")
    ensure_output_dir(output_dir)
    load_kernels(META_KERNEL)
    try: 
        ets = generate_et_range(DEFAULT_START_UTC,DEFAULT_END_UTC,DEFAULT_STEP_IN_SECONDS)
        cassini_df = build_trajectory_dataframe(target=CASSINI_NAME,observer=SATURN_NAME,ets=ets)
        titan_df = build_trajectory_dataframe(target=TITAN_NAME,observer=SATURN_NAME,ets=ets)
        cassini_titan_distance_df = build_distance_dataframe(cassini_df,titan_df,"Cassini-Titan")
        plot_trajectory_3d(cassini_df,"Cassini",output_dir/"Cassini_3d.html")
        print("Analysis complete.Figures saved to output/figures")
    finally:
        clear_kernels()

if __name__ == "__main__":
    main()