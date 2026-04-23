from pathlib import Path
import pandas as pd 
import plotly.graph_objects as go


def ensure_output_dir(path:Path)-> None:
    path.mkdir(parents=True,exist_ok=True)
def plot_trajectory_3d(df: pd.DataFrame,title:str,output_path: Path) -> None:
    fig = go.Figure() # creating an empty Figure 
    fig.add_trace( # add to the plot trace of the trajectory 
        go.Scatter3d(
            x = df["x_km"],
            y = df["y_km"],
            z = df["z_km"],
            mode= "lines",
            name= "Trajectory",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x = [df["x_km"].iloc[0]], # the extra brackets bc in plotly we're required to give an array of points
            y = [df["y_km"].iloc[0]],
            z = [df["z_km"].iloc[0]],
            mode= "marker",
            name="Start"
        )
    )
    fig.add_trace( # add the Endpoint 
        go.Scatter3d(
            x = [df["x_km"].iloc[-1]],
            y = [df["y_km"].iloc[-1]],
            z = [df["z_km"].iloc[-1]],
            mode="marker",
            name= "End"
        )
    )
    fig.update_layout( # the settings for how the plot looks 
        title = title,
        scene = dict( # scene is used in Plotly to set axes and 3D view 
            xaxis_title = "X [km]",
            yaxis_title = "Y [km]",
            zaxis_title = "Z [km]",
            aspectmode= "data" #  it keeps the proportions consistent with the data
        )
    )
    fig.write_html(str(output_path))



