import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.interpolate import griddata
import os
import shutil

def main():
    
    plot_name = "PVT_NUM_VX_D_NORM"

    # Load the CSV data
    data = pd.read_csv(r"C:\CzechFOI-BYAGE\TERRA\PVT_NUM_VX_D_NORM.csv")

    # Extract the columns
    days = data['DAYS_20200101']
    age_groups = data.columns[1:]
    values = data.iloc[:, 1:].values

    # Map age groups to numerical values
    age_group_mapping = {age: idx for idx, age in enumerate(age_groups)}
    age_groups_numeric = [age_group_mapping[age] for age in age_groups]

    # Flatten the data for interpolation
    days_flat = np.repeat(days.values, len(age_groups))
    age_groups_flat = np.tile(age_groups_numeric, len(days))
    values_flat = values.flatten()

    # Filter out NaN values
    mask = ~np.isnan(values_flat)
    days_flat = days_flat[mask]
    age_groups_flat = age_groups_flat[mask]
    values_flat = values_flat[mask]

    # Create a grid for the surface plot
    x = np.linspace(days.min(), days.max(), 100)
    y = np.linspace(min(age_groups_numeric), max(age_groups_numeric), 100)
    x_grid, y_grid = np.meshgrid(x, y)

    # Interpolate the z values on the grid using griddata
    z_grid = griddata((days_flat, age_groups_flat), values_flat, (x_grid, y_grid), method='cubic')
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)
    
    # Check if z_grid contains valid data
    if np.isnan(z_grid).all():
        print("Interpolation resulted in all NaN values. Check your data and interpolation method.")
    else:
        # Create the 3D surface plot with contours
        fig = go.Figure(data=[go.Surface(
            x=x_grid,
            y=y_grid,
            z=z_grid,
            colorscale='Cividis',  # Updated color palette
            contours={
                "x": {"show": True, "start": x.min(), "end": x.max(), "size": 5},
                "y": {"show": True, "start": y.min(), "end": y.max(), "size": 5},
                "z": {"show": True, "start": z_grid.min(), "end": z_grid.max(), "size": 5}
            }
        )])

        # Update layout for better visualization
        fig.update_layout(
            title='3D Contour Plot',
            scene=dict(
                zaxis=dict(range=[z_grid.min(), np.percentile(z_grid, 100)])  # Limit the z-axis range
            )    
        )

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
