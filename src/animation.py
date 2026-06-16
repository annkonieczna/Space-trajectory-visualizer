from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from bodies import BodyEllipsoid, create_ellipsoid_mesh


def interpolate_trajectory(
    df: pd.DataFrame,
    points_between: int = 4,
) -> pd.DataFrame:
    """
    Creates additional points between trajectory points.

    It's used for smoother animation.
    and does not replace the scientific trajectory data.
    """

    if points_between <= 0:
        return df.copy()

    x_values: list[float] = []
    y_values: list[float] = []
    z_values: list[float] = []

    for i in range(len(df) - 1):
        current_row = df.iloc[i]
        next_row = df.iloc[i + 1]

        for j in range(points_between + 1):
            alpha = j / (points_between + 1)

            x = (1 - alpha) * current_row["x_km"] + alpha * next_row["x_km"]
            y = (1 - alpha) * current_row["y_km"] + alpha * next_row["y_km"]
            z = (1 - alpha) * current_row["z_km"] + alpha * next_row["z_km"]

            x_values.append(x)
            y_values.append(y)
            z_values.append(z)

    last_row = df.iloc[-1]

    x_values.append(last_row["x_km"])
    y_values.append(last_row["y_km"])
    z_values.append(last_row["z_km"])

    return pd.DataFrame(
        {
            "x_km": x_values,
            "y_km": y_values,
            "z_km": z_values,
        }
    )


def add_body_ellipsoid_trace(
    fig: go.Figure,
    ellipsoid: BodyEllipsoid,
    color: str = "gold",
    opacity: float = 1.0,
    scale: float = 1.0,
    number_of_points: int = 70,
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


def animate_moving_point_on_static_trajectory(
    df: pd.DataFrame,
    title: str,
    output_path: Path,
    central_body: BodyEllipsoid | None = None,
    central_body_scale: float = 1.0,
    animation_frames: int = 300,
    frame_duration_ms: int = 15,
    frame_step: int = 2,
    points_between: int = 3,
) -> None:
    fig = go.Figure()

    if central_body is not None:
        add_body_ellipsoid_trace(
            fig,
            ellipsoid=central_body,
            scale=central_body_scale,
        )

    sampled_df = df.iloc[::frame_step].copy()

    if sampled_df.index[-1] != df.index[-1]:
        sampled_df = pd.concat([sampled_df, df.iloc[[-1]]])

    animated_df = interpolate_trajectory(
        sampled_df,
        points_between=points_between,
    )

    if len(animated_df) > animation_frames:
        animation_indices = np.linspace(
            0,
            len(animated_df) - 1,
            animation_frames,
            dtype=int,
        )

        animated_df = animated_df.iloc[animation_indices].copy()

    # Full trajectory as a static line
    fig.add_trace(
        go.Scatter3d(
            x=df["x_km"],
            y=df["y_km"],
            z=df["z_km"],
            mode="lines",
            name="Trajectory",
            line=dict(color="#9898a4", width=2),
            opacity=0.2,
        )
    )

    # Current position as an animated point
    current_point_trace_index = len(tuple(fig.data))

    fig.add_trace(
        go.Scatter3d(
            x=[animated_df["x_km"].iloc[0]],
            y=[animated_df["y_km"].iloc[0]],
            z=[animated_df["z_km"].iloc[0]],
            mode="markers",
            name="Current position",
            marker=dict(color="red", size=5),
        )
    )

    # Starting point
    fig.add_trace(
        go.Scatter3d(
            x=[df["x_km"].iloc[0]],
            y=[df["y_km"].iloc[0]],
            z=[df["z_km"].iloc[0]],
            mode="markers",
            name="Start",
            marker=dict(color="green", size=1, symbol="diamond"),
        )
    )

    # Ending point
    fig.add_trace(
        go.Scatter3d(
            x=[df["x_km"].iloc[-1]],
            y=[df["y_km"].iloc[-1]],
            z=[df["z_km"].iloc[-1]],
            mode="markers",
            name="End",
            marker=dict(color="red", size=1, symbol="diamond"),
        )
    )

    frames = []

    for frame_number in range(len(animated_df)):
        row = animated_df.iloc[frame_number]

        frames.append(
            go.Frame(
                name=str(frame_number),
                data=[
                    go.Scatter3d(
                        x=[row["x_km"]],
                        y=[row["y_km"]],
                        z=[row["z_km"]],
                        mode="markers",
                        marker=dict(
                            color="red",
                            size=5,
                            symbol="circle",
                        ),
                    )
                ],
                traces=[current_point_trace_index],
            )
        )

    fig.frames = frames

    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X [km]",
            yaxis_title="Y [km]",
            zaxis_title="Z [km]",
            aspectmode="data",
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                x=0.1,
                y=0,
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=frame_duration_ms, redraw=True),
                                transition=dict(duration=0),
                                fromcurrent=True,
                                mode="immediate",
                            ),
                        ],
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=True),
                                transition=dict(duration=0),
                                mode="immediate",
                            ),
                        ],
                    ),
                ],
            )
        ],
    )

    fig.write_html(str(output_path))


def animate_two_moving_points_on_static_trajectory(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    title: str,
    title_a: str,
    title_b: str,
    output_path: Path,
    central_body: BodyEllipsoid | None = None,
    central_body_scale: float = 1.0,
    animation_frames: int = 300,
    frame_duration_ms: int = 15,
    frame_step: int = 2,
    points_between: int = 3,
) -> None:
    fig = go.Figure()

    if central_body is not None:
        add_body_ellipsoid_trace(
            fig,
            ellipsoid=central_body,
            scale=central_body_scale,
        )
    # First dataframe

    sampled_df = df_a.iloc[::frame_step].copy()

    if sampled_df.index[-1] != df_a.index[-1]:
        sampled_df = pd.concat([sampled_df, df_a.iloc[[-1]]])

    animated_df_a = interpolate_trajectory(
        sampled_df,
        points_between=points_between,
    )

    if len(animated_df_a) > animation_frames:
        animation_indices = np.linspace(
            0,
            len(animated_df_a) - 1,
            animation_frames,
            dtype=int,
        )

        animated_df_a = animated_df_a.iloc[animation_indices].copy()

    # Full trajectory as a static line for df_a
    fig.add_trace(
        go.Scatter3d(
            x=df_a["x_km"],
            y=df_a["y_km"],
            z=df_a["z_km"],
            mode="lines",
            name=f"Trajectory of {title_a}",
            line=dict(color="#6161ff", width=2),
            opacity=0.2,
        )
    )

    # Current position for object A as an animated point
    current_point_trace_a_index = len(tuple(fig.data))

    fig.add_trace(
        go.Scatter3d(
            x=[animated_df_a["x_km"].iloc[0]],
            y=[animated_df_a["y_km"].iloc[0]],
            z=[animated_df_a["z_km"].iloc[0]],
            mode="markers",
            name=f"Current position of {title_a}",
            marker=dict(color="blue", size=3),
        )
    )

    # Starting point
    fig.add_trace(
        go.Scatter3d(
            x=[df_a["x_km"].iloc[0]],
            y=[df_a["y_km"].iloc[0]],
            z=[df_a["z_km"].iloc[0]],
            mode="markers",
            name=f"Start point od {title_a}",
            marker=dict(color="green", size=1, symbol="diamond"),
        )
    )

    # Ending point
    fig.add_trace(
        go.Scatter3d(
            x=[df_a["x_km"].iloc[-1]],
            y=[df_a["y_km"].iloc[-1]],
            z=[df_a["z_km"].iloc[-1]],
            mode="markers",
            name=f"End point of {title_a} ",
            marker=dict(color="red", size=3, symbol="diamond"),
        )
    )

    # moving point number 2:
    sampled_df = df_b.iloc[::frame_step].copy()

    if sampled_df.index[-1] != df_b.index[-1]:
        sampled_df = pd.concat([sampled_df, df_b.iloc[[-1]]])

    animated_df_b = interpolate_trajectory(
        sampled_df,
        points_between=points_between,
    )

    if len(animated_df_b) > animation_frames:
        animation_indices = np.linspace(
            0,
            len(animated_df_b) - 1,
            animation_frames,
            dtype=int,
        )

        animated_df_b = animated_df_b.iloc[animation_indices].copy()

    # Full trajectory as a static line
    fig.add_trace(
        go.Scatter3d(
            x=df_b["x_km"],
            y=df_b["y_km"],
            z=df_b["z_km"],
            mode="lines",
            name=f"Trajectory of {title_b}",
            line=dict(color="#e541fb", width=2),
            opacity=0.2,
        )
    )

    # Current position of object B as an animated point
    current_point_trace_b_index = len(tuple(fig.data))

    fig.add_trace(
        go.Scatter3d(
            x=[animated_df_b["x_km"].iloc[0]],
            y=[animated_df_b["y_km"].iloc[0]],
            z=[animated_df_b["z_km"].iloc[0]],
            mode="markers",
            name=f"Current position of {title_b}",
            marker=dict(color="purple", size=5),
        )
    )

    # Starting point
    fig.add_trace(
        go.Scatter3d(
            x=[df_b["x_km"].iloc[0]],
            y=[df_b["y_km"].iloc[0]],
            z=[df_b["z_km"].iloc[0]],
            mode="markers",
            name=f"Start point of {title_b}",
            marker=dict(color="green", size=1, symbol="diamond"),
        )
    )

    # Ending point
    fig.add_trace(
        go.Scatter3d(
            x=[df_b["x_km"].iloc[-1]],
            y=[df_b["y_km"].iloc[-1]],
            z=[df_b["z_km"].iloc[-1]],
            mode="markers",
            name=f"End point of {title_b}",
            marker=dict(color="red", size=1, symbol="diamond"),
        )
    )
    number_of_frames = min(len(animated_df_a), len(animated_df_b))

    frames = []

    for frame_number in range(number_of_frames):
        row_a = animated_df_a.iloc[frame_number]
        row_b = animated_df_b.iloc[frame_number]

        frames.append(
            go.Frame(
                name=str(frame_number),
                data=[
                    go.Scatter3d(
                        x=[row_a["x_km"]],
                        y=[row_a["y_km"]],
                        z=[row_a["z_km"]],
                        mode="markers",
                        marker=dict(
                            color="blue",
                            size=3,
                            symbol="circle",
                        ),
                    ),
                    go.Scatter3d(
                        x=[row_b["x_km"]],
                        y=[row_b["y_km"]],
                        z=[row_b["z_km"]],
                        mode="markers",
                        marker=dict(color="purple", size=5),
                    ),
                ],
                traces=[current_point_trace_a_index, current_point_trace_b_index],
            )
        )

    fig.frames = frames
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X [km]",
            yaxis_title="Y [km]",
            zaxis_title="Z [km]",
            aspectmode="data",
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                x=0.1,
                y=0,
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=frame_duration_ms, redraw=True),
                                transition=dict(duration=0),
                                fromcurrent=True,
                                mode="immediate",
                            ),
                        ],
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=True),
                                transition=dict(duration=0),
                                mode="immediate",
                            ),
                        ],
                    ),
                ],
            )
        ],
    )

    fig.write_html(str(output_path))


def animate_two_moving_points(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    title: str,
    title_a: str,
    title_b: str,
    output_path: Path,
    central_body: BodyEllipsoid | None = None,
    central_body_scale: float = 1.0,
    animation_frames: int = 300,
    frame_duration_ms: int = 15,
    frame_step: int = 2,
    points_between: int = 3,
) -> None:
    fig = go.Figure()

    if central_body is not None:
        add_body_ellipsoid_trace(
            fig,
            ellipsoid=central_body,
            scale=central_body_scale,
        )
    # First dataframe

    sampled_df = df_a.iloc[::frame_step].copy()

    if sampled_df.index[-1] != df_a.index[-1]:
        sampled_df = pd.concat([sampled_df, df_a.iloc[[-1]]])

    animated_df_a = interpolate_trajectory(
        sampled_df,
        points_between=points_between,
    )

    if len(animated_df_a) > animation_frames:
        animation_indices = np.linspace(
            0,
            len(animated_df_a) - 1,
            animation_frames,
            dtype=int,
        )

        animated_df_a = animated_df_a.iloc[animation_indices].copy()

    # Full trajectory as a static line for df_a
    fig.add_trace(
        go.Scatter3d(
            x=df_a["x_km"],
            y=df_a["y_km"],
            z=df_a["z_km"],
            mode="lines",
            name=f"Trajectory of {title_a}",
            line=dict(color="#6161ff", width=2),
            opacity=0,
        )
    )

    # Current position for object A as an animated point
    current_point_trace_a_index = len(tuple(fig.data))

    fig.add_trace(
        go.Scatter3d(
            x=[animated_df_a["x_km"].iloc[0]],
            y=[animated_df_a["y_km"].iloc[0]],
            z=[animated_df_a["z_km"].iloc[0]],
            mode="markers",
            name=f"Current position of {title_a}",
            marker=dict(color="blue", size=3),
        )
    )

    # moving point number 2:
    sampled_df = df_b.iloc[::frame_step].copy()

    if sampled_df.index[-1] != df_b.index[-1]:
        sampled_df = pd.concat([sampled_df, df_b.iloc[[-1]]])

    animated_df_b = interpolate_trajectory(
        sampled_df,
        points_between=points_between,
    )

    if len(animated_df_b) > animation_frames:
        animation_indices = np.linspace(
            0,
            len(animated_df_b) - 1,
            animation_frames,
            dtype=int,
        )

        animated_df_b = animated_df_b.iloc[animation_indices].copy()

    # Full trajectory as a static line
    fig.add_trace(
        go.Scatter3d(
            x=df_b["x_km"],
            y=df_b["y_km"],
            z=df_b["z_km"],
            mode="lines",
            name=f"Trajectory of {title_b}",
            line=dict(color="#e541fb", width=2),
            opacity=0,
        )
    )

    # Current position of object B as an animated point
    current_point_trace_b_index = len(tuple(fig.data))

    fig.add_trace(
        go.Scatter3d(
            x=[animated_df_b["x_km"].iloc[0]],
            y=[animated_df_b["y_km"].iloc[0]],
            z=[animated_df_b["z_km"].iloc[0]],
            mode="markers",
            name=f"Current position of {title_b}",
            marker=dict(color="purple", size=3),
        )
    )
    number_of_frames = min(len(animated_df_a), len(animated_df_b))

    frames = []

    for frame_number in range(number_of_frames):
        row_a = animated_df_a.iloc[frame_number]
        row_b = animated_df_b.iloc[frame_number]

        frames.append(
            go.Frame(
                name=str(frame_number),
                data=[
                    go.Scatter3d(
                        x=[row_a["x_km"]],
                        y=[row_a["y_km"]],
                        z=[row_a["z_km"]],
                        mode="markers",
                        marker=dict(
                            color="blue",
                            size=3,
                            symbol="circle",
                        ),
                    ),
                    go.Scatter3d(
                        x=[row_b["x_km"]],
                        y=[row_b["y_km"]],
                        z=[row_b["z_km"]],
                        mode="markers",
                        marker=dict(color="purple", size=3),
                    ),
                ],
                traces=[current_point_trace_a_index, current_point_trace_b_index],
            )
        )

    fig.frames = frames
    fig.update_layout(
        title=title,
        scene=dict(
            xaxis_title="X [km]",
            yaxis_title="Y [km]",
            zaxis_title="Z [km]",
            aspectmode="data",
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="left",
                x=0.1,
                y=0,
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(duration=frame_duration_ms, redraw=True),
                                transition=dict(duration=0),
                                fromcurrent=True,
                                mode="immediate",
                            ),
                        ],
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[
                            [None],
                            dict(
                                frame=dict(duration=0, redraw=True),
                                transition=dict(duration=0),
                                mode="immediate",
                            ),
                        ],
                    ),
                ],
            )
        ],
    )

    fig.write_html(str(output_path))
