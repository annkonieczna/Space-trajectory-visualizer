from datetime import date, datetime, time

import pandas as pd
import streamlit as st

from src.analysis import (
    add_relative_days,
    build_distance_dataframe,
    find_global_max,
    find_global_min,
)
from src.animation import (
    animate_moving_point_on_static_trajectory,
    animate_two_moving_points_on_static_trajectory,
)
from src.bodies import build_body_ellipsoid
from src.config import (
    CASSINI_NAME,
    DEFAULT_END_UTC,
    DEFAULT_START_UTC,
    DEFAULT_STEP_IN_SECONDS,
    META_KERNEL,
    SATURN_NAME,
    TITAN_NAME,
)
from src.spice_loader import load_kernels
from src.time_utilis import generate_et_range
from src.trajectory import build_trajectory_dataframe
from src.visualization import (
    create_distance_figure,
    create_trajectory_3d_figure,
    create_two_trajectories_3d_figure,
)

# list of available targets and observers for analysis
AVAILABLE_TARGETS = [CASSINI_NAME, TITAN_NAME]
AVAILABLE_OBSERVERS = [SATURN_NAME]


# helper for parsing ISO into datetime ( default format for Streamlit)
def parse_default_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def to_utc_string(date_value: date, time_value: time) -> str:
    return datetime.combine(date_value, time_value).strftime("%Y-%m-%dT%H:%M:%S")


# formatting helper functions
def format_distance(value: float) -> str:
    return f"{value:,.0f} km"


def format_speed(value: float) -> str:
    return f"{value:,.3f} km/s"


def add_speed_column(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["speed_km_s"] = df[["vx_km_s", "vy_km_s", "vz_km_s"]].pow(2).sum(axis=1).pow(0.5)
    return df


# streamlit decorator that informs the app that the result of that function needs to be
# calculated once and kept between different runs
@st.cache_resource
def load_spice_kernels() -> bool:
    load_kernels(META_KERNEL)
    return True


# if user runs the analysis with the same values, Streamlit will return the
# saved Dataframe instead of caculation the trajectory again
@st.cache_data(
    show_spinner=False
)  # show_spinner=False turns off the default Streamlit message
# about the function being calculated
def calculate_single_object(
    target: str,
    observer: str,
    start_utc: str,
    end_utc: str,
    step_seconds: int,
) -> pd.DataFrame:
    ets = generate_et_range(start_utc, end_utc, step_seconds)
    df = build_trajectory_dataframe(target=target, observer=observer, ets=ets)
    return add_relative_days(df)


@st.cache_data(show_spinner=False)
def calculate_comparison(
    target_a: str,
    target_b: str,
    observer: str,
    start_utc: str,
    end_utc: str,
    step_seconds: int,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Cashed comparison between two objects"""
    ets = generate_et_range(start_utc, end_utc, step_seconds)
    df_a = build_trajectory_dataframe(target=target_a, observer=observer, ets=ets)
    df_b = build_trajectory_dataframe(target=target_b, observer=observer, ets=ets)
    distance_df = build_distance_dataframe(df_a, df_b, f"{target_a}-{target_b}")
    return add_relative_days(df_a), add_relative_days(df_b), distance_df


def create_single_animation_figure(
    df: pd.DataFrame,
    target: str,
    observer: str,
    central_body,
    central_body_scale: float,
):
    frame_duration_ms = 11
    return animate_moving_point_on_static_trajectory(
        df=df,
        title=f"{target} trajectory relative to {observer}",
        output_path=None,
        central_body=central_body,
        central_body_scale=central_body_scale,
        animation_frames=700,
        frame_duration_ms=frame_duration_ms,
        frame_step=2,
        points_between=3,
    )


def create_comparison_animation_figure(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    target_a: str,
    target_b: str,
    observer: str,
    central_body,
    central_body_scale: float,
):
    frame_duration_ms = 11
    return animate_two_moving_points_on_static_trajectory(
        df_a=df_a,
        df_b=df_b,
        title=f"{target_a} and {target_b} relative to {observer}",
        title_a=target_a,
        title_b=target_b,
        output_path=None,
        central_body=central_body,
        central_body_scale=central_body_scale,
        animation_frames=700,
        frame_duration_ms=frame_duration_ms,
        frame_step=2,
        points_between=3,
    )


def build_central_body(observer: str, show_central_body: bool):
    """Funtion building a central body depending whether the user wants to see it"""
    if not show_central_body:
        return None

    return build_body_ellipsoid(
        body_name=observer,
        center_km=(0.0, 0.0, 0.0),
    )


def render_summary(distance_df: pd.DataFrame) -> None:
    """Function displaing a summary of min and max"""
    min_row = find_global_min(distance_df)
    max_row = find_global_max(distance_df)

    col_min, col_max, col_samples = st.columns(3)
    col_min.metric("Minimum distance", format_distance(float(min_row["distance_km"])))
    col_max.metric("Maximum distance", format_distance(float(max_row["distance_km"])))
    col_samples.metric("Samples", f"{len(distance_df):,}")

    summary_df = pd.DataFrame(
        [
            {
                "Type": "Minimum",
                "UTC": min_row["utc"],
                "Days from start": round(float(min_row["days_from_start"]), 3),
                "Distance [km]": round(float(min_row["distance_km"]), 3),
            },
            {
                "Type": "Maximum",
                "UTC": max_row["utc"],
                "Days from start": round(float(max_row["days_from_start"]), 3),
                "Distance [km]": round(float(max_row["distance_km"]), 3),
            },
        ]
    )
    st.dataframe(summary_df, hide_index=True, width="stretch")


def render_single_object_stats(df: pd.DataFrame, target: str, observer: str) -> None:
    df = add_speed_column(df)
    min_distance = find_global_min(df)
    max_distance = find_global_max(df)

    col_min, col_max, col_mean, col_speed = st.columns(4)
    col_min.metric(
        f"Closest to {observer}",
        format_distance(float(min_distance["distance_km"])),
    )
    col_max.metric(
        f"Farthest from {observer}",
        format_distance(float(max_distance["distance_km"])),
    )
    col_mean.metric("Mean distance", format_distance(float(df["distance_km"].mean())))
    col_speed.metric("Mean speed", format_speed(float(df["speed_km_s"].mean())))

    stats_df = pd.DataFrame(
        [
            {
                "Quantity": "Minimum distance",
                "UTC": min_distance["utc"],
                "Value": format_distance(float(min_distance["distance_km"])),
            },
            {
                "Quantity": "Maximum distance",
                "UTC": max_distance["utc"],
                "Value": format_distance(float(max_distance["distance_km"])),
            },
            {
                "Quantity": "Minimum speed",
                "UTC": df.loc[df["speed_km_s"].idxmin(), "utc"],
                "Value": format_speed(float(df["speed_km_s"].min())),
            },
            {
                "Quantity": "Maximum speed",
                "UTC": df.loc[df["speed_km_s"].idxmax(), "utc"],
                "Value": format_speed(float(df["speed_km_s"].max())),
            },
        ]
    )
    st.subheader(f"Analysis summary for {target}")
    st.dataframe(stats_df, hide_index=True, width="stretch")


def render_comparison_stats(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    distance_df: pd.DataFrame,
    target_a: str,
    target_b: str,
) -> None:
    render_summary(distance_df)

    speed_a = add_speed_column(df_a)["speed_km_s"]
    speed_b = add_speed_column(df_b)["speed_km_s"]
    extra_stats = pd.DataFrame(
        [
            {
                "Object": target_a,
                "Mean speed [km/s]": round(float(speed_a.mean()), 3),
                "Min speed [km/s]": round(float(speed_a.min()), 3),
                "Max speed [km/s]": round(float(speed_a.max()), 3),
                "Mean observer distance [km]": round(
                    float(df_a["distance_km"].mean()), 3
                ),
            },
            {
                "Object": target_b,
                "Mean speed [km/s]": round(float(speed_b.mean()), 3),
                "Min speed [km/s]": round(float(speed_b.min()), 3),
                "Max speed [km/s]": round(float(speed_b.max()), 3),
                "Mean observer distance [km]": round(
                    float(df_b["distance_km"].mean()), 3
                ),
            },
        ]
    )
    st.subheader("Object statistics")
    st.dataframe(extra_stats, hide_index=True, width="stretch")


def main() -> None:
    st.set_page_config(
        page_title="Space trajectory visualizer",
        layout="wide",
    )
    st.title("Space trajectory visualizer")

    if not META_KERNEL.exists():
        st.error(f"Missing SPICE meta-kernel: {META_KERNEL}")
        st.stop()

    default_start = parse_default_datetime(DEFAULT_START_UTC)
    default_end = parse_default_datetime(DEFAULT_END_UTC)

    with st.sidebar:
        st.header("Parameters")
        analysis_mode = st.radio(
            "Analysis mode",
            ["Single object", "Compare objects"],
        )
        with st.form("analysis_parameters"):
            target_a = st.selectbox("Object", AVAILABLE_TARGETS, index=0)
            target_b = None
            if analysis_mode == "Compare objects":
                target_b = st.selectbox("Object B", AVAILABLE_TARGETS, index=1)
            observer = st.selectbox("Observer", AVAILABLE_OBSERVERS, index=0)

            start_date = st.date_input("Start date", value=default_start.date())
            start_time = st.time_input("Start time", value=default_start.time())
            end_date = st.date_input("End date", value=default_end.date())
            end_time = st.time_input("End time", value=default_end.time())

            step_seconds = st.number_input(
                "Step [seconds]",
                min_value=60,
                max_value=86_400,
                value=DEFAULT_STEP_IN_SECONDS,
                step=60,
            )
            show_central_body = st.checkbox("Show Saturn", value=True)
            show_animation = st.checkbox("Show animation", value=False)
            central_body_scale = st.slider(
                "Saturn scale",
                min_value=0.2,
                max_value=5.0,
                value=1.0,
                step=0.1,
                disabled=not show_central_body,
            )
            submitted = st.form_submit_button(
                "Run analysis",
                type="primary",
                width="stretch",
            )

    params = {
        "analysis_mode": analysis_mode,
        "target_a": target_a,
        "target_b": target_b,
        "observer": observer,
        "start_utc": to_utc_string(start_date, start_time),
        "end_utc": to_utc_string(end_date, end_time),
        "step_seconds": int(step_seconds),
        "show_central_body": show_central_body,
        "show_animation": show_animation,
        "central_body_scale": central_body_scale,
    }
    if (
        submitted
        or "analysis_params" not in st.session_state
        or "analysis_mode" not in st.session_state["analysis_params"]
    ):
        st.session_state["analysis_params"] = params

    active_params = st.session_state["analysis_params"]
    is_comparison = active_params["analysis_mode"] == "Compare objects"

    if is_comparison and active_params["target_a"] == active_params["target_b"]:
        st.warning("Choose two different objects to compare their distance.")
        st.stop()

    try:
        load_spice_kernels()
        with st.spinner("Calculating trajectories..."):
            if is_comparison:
                df_a, df_b, distance_df = calculate_comparison(
                    target_a=active_params["target_a"],
                    target_b=active_params["target_b"],
                    observer=active_params["observer"],
                    start_utc=active_params["start_utc"],
                    end_utc=active_params["end_utc"],
                    step_seconds=active_params["step_seconds"],
                )
            else:
                df_a = calculate_single_object(
                    target=active_params["target_a"],
                    observer=active_params["observer"],
                    start_utc=active_params["start_utc"],
                    end_utc=active_params["end_utc"],
                    step_seconds=active_params["step_seconds"],
                )
                df_b = None
                distance_df = df_a
    except Exception as exc:
        st.error(str(exc))
        st.stop()

    central_body = build_central_body(
        active_params["observer"],
        active_params["show_central_body"],
    )

    if is_comparison:
        assert df_b is not None
        render_comparison_stats(
            df_a=df_a,
            df_b=df_b,
            distance_df=distance_df,
            target_a=active_params["target_a"],
            target_b=active_params["target_b"],
        )
    else:
        render_single_object_stats(
            df=df_a,
            target=active_params["target_a"],
            observer=active_params["observer"],
        )

    distance_tab_label = "Distance between objects" if is_comparison else "Distance"
    tab_trajectory, tab_distance, tab_animation, tab_data = st.tabs(
        ["Trajectory", distance_tab_label, "Animation", "Data"]
    )

    with tab_trajectory:
        if is_comparison:
            assert df_b is not None
            trajectory_fig = create_two_trajectories_3d_figure(
                df_a=df_a,
                df_b=df_b,
                title_a=active_params["target_a"],
                title_b=active_params["target_b"],
                title=(
                    f"{active_params['target_a']} and {active_params['target_b']} "
                    f"relative to {active_params['observer']}"
                ),
                central_body=central_body,
                central_body_scale=active_params["central_body_scale"],
            )
        else:
            trajectory_fig = create_trajectory_3d_figure(
                df=df_a,
                title=(
                    f"{active_params['target_a']} trajectory relative "
                    f"to {active_params['observer']}"
                ),
                object_name=f"{active_params['target_a']}",
                central_body=central_body,
                central_body_scale=active_params["central_body_scale"],
            )
        st.plotly_chart(trajectory_fig, width="stretch")

    with tab_distance:
        if is_comparison:
            distance_title = (
                f"Distance between {active_params['target_a']} "
                f"and {active_params['target_b']}"
            )
        else:
            distance_title = (
                f"Distance from {active_params['target_a']} "
                f"to {active_params['observer']}"
            )

        distance_fig = create_distance_figure(
            distance_df,
            title=distance_title,
        )
        st.plotly_chart(distance_fig, width="stretch")

    with tab_animation:
        if active_params["show_animation"]:
            st.caption(
                "The animation uses sampled trajectory points for smoother playback."
            )
            with st.spinner("Preparing animation..."):
                if is_comparison:
                    assert df_b is not None
                    animation_fig = create_comparison_animation_figure(
                        df_a=df_a,
                        df_b=df_b,
                        target_a=active_params["target_a"],
                        target_b=active_params["target_b"],
                        observer=active_params["observer"],
                        central_body=central_body,
                        central_body_scale=active_params["central_body_scale"],
                    )
                else:
                    animation_fig = create_single_animation_figure(
                        df=df_a,
                        target=active_params["target_a"],
                        observer=active_params["observer"],
                        central_body=central_body,
                        central_body_scale=active_params["central_body_scale"],
                    )
            st.plotly_chart(animation_fig, width="stretch")
        else:
            st.info("Enable Show animation in the sidebar and run the analysis again.")

    with tab_data:
        st.subheader("Distance data" if is_comparison else "Trajectory data")
        st.dataframe(distance_df, hide_index=True, width="stretch")
        if is_comparison:
            file_name = (
                f"{active_params['target_a'].lower()}_"
                f"{active_params['target_b'].lower()}_distances.csv"
            )
        else:
            file_name = f"{active_params['target_a'].lower()}_trajectory.csv"

        st.download_button(
            "Download CSV",
            data=distance_df.to_csv(index=False).encode("utf-8"),
            file_name=file_name,
            mime="text/csv",
        )


if __name__ == "__main__":
    main()
