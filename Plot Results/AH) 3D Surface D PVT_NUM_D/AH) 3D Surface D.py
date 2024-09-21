import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata
import os
import shutil

def main():
    
    plot_name = "PVT_NUM_D"
    
    # Load data
    chunk = np.loadtxt(r"C:\github\CzechFOI-BYAGE\TERRA\PVT_NUM_D.csv", comments='#', delimiter=',', skiprows=1)
    DATA = np.array(chunk)
    Ys = DATA[:, 0]
    Xs = DATA[:, 1]
    Zs = DATA[:, 2]

    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Create a grid for the surface plot
    xi = np.linspace(Xs.min(), Xs.max(), 100)
    yi = np.linspace(Ys.min(), Ys.max(), 100)
    xi, yi = np.meshgrid(xi, yi)
    zi = griddata((Xs, Ys), Zs, (xi, yi), method='linear')

    # Create a 3D surface plot
    # Create a 3D surface plot with a color bar
    fig = go.Figure(data=[go.Surface(
        x=xi, y=yi, z=zi, 
        colorscale='HSV',
        colorbar=dict(title='Number of Deaths')  # Add a color bar with a title
    )])



    # Update layout for better visualization
    fig.update_layout(
        scene=dict(
            xaxis_title='Day of Death from 2020-01-01',
            yaxis_title='Age of Death',
            zaxis_title='Number of Deaths',
            xaxis=dict(nticks=20),  # Increase the number of ticks on the x-axis
            yaxis=dict(nticks=6),
            zaxis=dict(nticks=5),
            xaxis_showspikes=False,
            yaxis_showspikes=False,
            zaxis_showspikes=False,
            aspectratio=dict(x=2, y=1, z=1)  # Adjust aspect ratio to stretch x-axis
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1,
            xanchor="right",
            x=1
        ),
        width=1920,
        height=1080,
        margin=dict(r=20, b=10, l=10, t=10)
    )

    # Export to HTML
    fig.write_html(f"{full_plotfile_name}.html")
    print(f"Plot has been saved to HTML file.")


# Initialize the "Plot Results" directory and copy this PyScript into it
def init_function(plot_name):
    script_name = os.path.splitext(os.path.basename(__file__))[0]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    first_root_dir = os.path.abspath(os.sep.join(script_dir.split(os.sep)[:2]))
    plot_result_path = os.path.join(first_root_dir, "Plot Results", f"{script_name} {plot_name}")
    os.makedirs(plot_result_path, exist_ok=True)
    
    script_file_name = os.path.join(plot_result_path, f"{script_name}.py")
    if not os.path.exists(script_file_name):
        shutil.copy(__file__, script_file_name)
    # return plot file name without extension
    return plot_result_path + os.sep + f"{script_name} {plot_name}"

# call main script
if __name__ == "__main__": main()
