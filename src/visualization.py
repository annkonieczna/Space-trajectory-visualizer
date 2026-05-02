from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from itertools import cycle

starting_point_colours = cycle(
    {"Green": "#87de63", "Dark_green": "#1a8b3d", "Blue": "#77d5fe"}
)
ending_point_colours = cycle(
    {"Red": "#ef5e38", "Orange": "#ffb10b", "Violet": "#940bff"}
)
trajectory_colours = cycle(
    {"Dark_blue": "#493fff", "Yellow": "#fff527", "Pink": "#ff72fe"}
)


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def plot_trajectory_3d(df: pd.DataFrame, title: str, output_path: Path) -> None:
    fig = go.Figure()  # creating an empty Figure
    fig.add_trace(  # add to the plot trace of the trajectory
        go.Scatter3d(
            x=df["x_km"],
            y=df["y_km"],
            z=df["z_km"],
            mode="lines",
            name="Trajectory",
            line_color="#493fff",
        )
    )
    fig.add_trace(  # add the Starting Point
        go.Scatter3d(
            x=[
                df["x_km"].iloc[0]
            ],  # the extra brackets bc in plotly we're required to give an array of points
            y=[df["y_km"].iloc[0]],
            z=[df["z_km"].iloc[0]],
            mode="markers",
            name="Start",
            marker_color="green",
        )
    )
    fig.add_trace(  # add the End Point
        go.Scatter3d(
            x=[df["x_km"].iloc[-1]],
            y=[df["y_km"].iloc[-1]],
            z=[df["z_km"].iloc[-1]],
            mode="markers",
            name="End",
            marker_color="red",
        )
    )
    fig.update_layout(  # the settings for how the plot looks
        title=title,
        scene=dict(  # scene is used in Plotly to set axes and 3D view
            xaxis_title="X [km]",
            yaxis_title="Y [km]",
            zaxis_title="Z [km]",
            aspectmode="data",  #  it keeps the proportions consistent with the data
        ),
    )
    fig.write_html(str(output_path))


def plot_two_trajectories_3d(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    title_a: str,
    title_b: str,
    title: str,
    outputPath: Path,
):
    fig = go.Figure()
    # plotting object A
    fig.add_trace(
        go.Scatter3d(
            x=df_a["x_km"],
            y=df_a["y_km"],
            z=df_a["z_km"],
            mode="lines",
            name=title_a,
            line_color=next(trajectory_colours),
        )
    )
    fig.add_trace(  # add the Starting Point
        go.Scatter3d(
            x=[df_a["x_km"].iloc[0]],
            y=[df_a["y_km"].iloc[0]],
            z=[df_a["z_km"].iloc[0]],
            mode="markers",
            name="Start",
            marker_color=next(starting_point_colours),
        )
    )
    fig.add_trace(  # add the End Point
        go.Scatter3d(
            x=[df_a["x_km"].iloc[-1]],
            y=[df_a["y_km"].iloc[-1]],
            z=[df_a["z_km"].iloc[-1]],
            mode="markers",
            name="End",
            marker_color=next(ending_point_colours),
        )
    )
    # plotting object B

    fig.add_trace(
        go.Scatter3d(
            x=df_b["x_km"],
            y=df_b["y_km"],
            z=df_b["z_km"],
            mode="lines",
            name=title_b,
            line_color=next(trajectory_colours),
        )
    )
    fig.add_trace(  # add the Starting Point
        go.Scatter3d(
            x=[df_b["x_km"].iloc[0]],
            y=[df_b["y_km"].iloc[0]],
            z=[df_b["z_km"].iloc[0]],
            mode="markers",
            name="Start",
            marker_color=next(starting_point_colours),
        )
    )
    fig.add_trace(  # add the End Point
        go.Scatter3d(
            x=[df_b["x_km"].iloc[-1]],
            y=[df_b["y_km"].iloc[-1]],
            z=[df_b["z_km"].iloc[-1]],
            mode="markers",
            name="End",
            marker_color=next(ending_point_colours),
        )
    )

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X [km]",
            yaxis_title="Y [km]",
            zaxis_title="Z [km]",
            aspectmode="data",  #  it keeps the proportions consistent with the data
        ),
    )
    fig.write_html(str(outputPath))
