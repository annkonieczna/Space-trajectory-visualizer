from pathlib import Path

import pandas as pd
import plotly.graph_objects as go

from src.calculations.bodies import BodyEllipsoid, create_ellipsoid_mesh


def ensure_output_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def create_trajectory_3d_figure(
    df: pd.DataFrame,
    title: str,
    object_name: str,
    central_body: BodyEllipsoid | None = None,
    central_body_scale: float = 1.0,
) -> go.Figure:
    fig = go.Figure()  # creating an empty Figure
    if central_body is not None:
        add_body_ellipsoid_trace(fig, ellipsoid=central_body, scale=central_body_scale)
    fig.add_trace(  # add to the plot trace of the trajectory
        go.Scatter3d(
            x=df["x_km"],
            y=df["y_km"],
            z=df["z_km"],
            mode="lines",
            name=f" {object_name}'s Trajectory",
            line_color="#493fff",
        )
    )
    fig.add_trace(  # add the Starting Point
        go.Scatter3d(
            x=[df["x_km"].iloc[0]],  # the extra brackets bc in plotly
            # we're required to give an array of points
            y=[df["y_km"].iloc[0]],
            z=[df["z_km"].iloc[0]],
            mode="markers",
            name="Starting point",
            marker=dict(color="green", size=4),
        )
    )
    fig.add_trace(  # add the End Point
        go.Scatter3d(
            x=[df["x_km"].iloc[-1]],
            y=[df["y_km"].iloc[-1]],
            z=[df["z_km"].iloc[-1]],
            mode="markers",
            name="Ending point",
            marker=dict(color="red", size=4),
        )
    )
    update_3d_layout(fig, title)
    return fig


def plot_trajectory_3d(
    df: pd.DataFrame,
    title: str,
    output_path: Path,
    object_name: str,
    central_body: BodyEllipsoid | None = None,
    central_body_scale: float = 1.0,
) -> None:
    fig = create_trajectory_3d_figure(
        df=df,
        title=title,
        object_name=object_name,
        central_body=central_body,
        central_body_scale=central_body_scale,
    )
    fig.write_html(str(output_path))


def create_two_trajectories_3d_figure(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    title_a: str,
    title_b: str,
    title: str,
    central_body: BodyEllipsoid | None = None,
    central_body_scale: float = 1.0,
) -> go.Figure:
    fig = go.Figure()
    if central_body is not None:
        add_body_ellipsoid_trace(fig, ellipsoid=central_body, scale=central_body_scale)

    add_trajectory_trace(
        fig,
        df=df_a,
        line_name=f"{title_a}'s Trajectory",
        start_name=f"{title_a}'s Start",
        end_name=f"{title_a}'s End",
        line_color="#493fff",
        start_color="#87de63",
        end_color="#ef5e38",
    )
    add_trajectory_trace(
        fig,
        df=df_b,
        line_name=f"{title_b}'s Trajectory",
        start_name=f"{title_b}'s Start",
        end_name=f"{title_b}'s End",
        line_color="#ff72fe",
        start_color="#77d5fe",
        end_color="#ffb10b",
    )

    update_3d_layout(fig, title)
    return fig


def plot_two_trajectories_3d(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    title_a: str,
    title_b: str,
    title: str,
    output_path: Path,
    central_body: BodyEllipsoid | None = None,
    central_body_scale: float = 1.0,
) -> None:
    fig = create_two_trajectories_3d_figure(
        df_a=df_a,
        df_b=df_b,
        title_a=title_a,
        title_b=title_b,
        title=title,
        central_body=central_body,
        central_body_scale=central_body_scale,
    )
    fig.write_html(str(output_path))


def create_distance_figure(df: pd.DataFrame, title: str) -> go.Figure:
    x_column = "days_from_start" if "days_from_start" in df.columns else "utc"
    x_axis_title = "Days from start" if x_column == "days_from_start" else "UTC"

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df[x_column],
            y=df["distance_km"],
            mode="lines",
            name="Distance",
            line=dict(color="#0077b6", width=2),
            customdata=df[["utc"]],
            hovertemplate=(
                "UTC=%{customdata[0]}<br>Distance=%{y:,.0f} km<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        template="plotly_dark",
        title=title,
        xaxis_title=x_axis_title,
        yaxis_title="Distance [km]",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="#f8fafc"),
        height=820,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    return fig


def add_trajectory_trace(
    fig: go.Figure,
    df: pd.DataFrame,
    line_name: str,
    start_name: str,
    end_name: str,
    line_color: str,
    start_color: str,
    end_color: str,
) -> None:
    fig.add_trace(
        go.Scatter3d(
            x=df["x_km"],
            y=df["y_km"],
            z=df["z_km"],
            mode="lines",
            name=line_name,
            line_color=line_color,
        )
    )
    fig.add_trace(  # add the Starting Point
        go.Scatter3d(
            x=[df["x_km"].iloc[0]],
            y=[df["y_km"].iloc[0]],
            z=[df["z_km"].iloc[0]],
            mode="markers",
            name=start_name,
            marker=dict(color=start_color, size=4),
        )
    )
    fig.add_trace(  # add the End Point
        go.Scatter3d(
            x=[df["x_km"].iloc[-1]],
            y=[df["y_km"].iloc[-1]],
            z=[df["z_km"].iloc[-1]],
            mode="markers",
            name=end_name,
            marker=dict(color=end_color, size=4),
        )
    )


def add_body_ellipsoid_trace(
    fig: go.Figure,
    ellipsoid: BodyEllipsoid,
    color: str = "gold",
    opacity: float = 1.0,
    scale: float = 1.0,
    number_of_points: int = 100,
) -> None:
    x, y, z = create_ellipsoid_mesh(
        ellipsoid, number_of_points=number_of_points, scale=scale
    )
    fig.add_trace(
        go.Surface(
            x=x,
            y=y,
            z=z,
            name=ellipsoid.name,
            showscale=False,
            opacity=opacity,
            colorscale=[[0, color], [1, color]],
            hovertemplate=(
                f"{ellipsoid.name}<br>"
                "x=%{x:.0f} km<br>"
                "y=%{y:.0f} km<br>"
                "z=%{z:.0f} km"
                "<extra></extra>"
            ),
        )
    )


def update_3d_layout(fig: go.Figure, title: str) -> None:
    fig.update_layout(
        template="plotly_dark",
        title=title,
        scene=dict(
            xaxis_title="X [km]",
            yaxis_title="Y [km]",
            zaxis_title="Z [km]",
            aspectmode="data",
            bgcolor="#0e1117",
            xaxis=dict(backgroundcolor="#0e1117", gridcolor="#334155"),
            yaxis=dict(backgroundcolor="#0e1117", gridcolor="#334155"),
            zaxis=dict(backgroundcolor="#0e1117", gridcolor="#334155"),
        ),
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font=dict(color="#f8fafc"),
        height=820,
        margin=dict(l=0, r=0, t=50, b=0),
    )
