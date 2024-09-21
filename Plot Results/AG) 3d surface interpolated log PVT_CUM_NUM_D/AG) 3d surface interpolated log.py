import plotly.graph_objects as go
import pandas as pd
import numpy as np
from scipy.interpolate import griddata
import os
import shutil

def main():
    
    plot_name = "PVT_CUM_NUM_D"
    
    # Load the CSV file without headers
    file_path = r"C:\CzechFOI-BYAGE\TERRA\PVT_CUM_NUM_D.csv"
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)
    
    # Read the CSV file and skip the first row (header)
    df = pd.read_csv(file_path, header=None, skiprows=1)

    # Extract the header row separately for age group labels
    header = pd.read_csv(file_path, nrows=0).columns.tolist()

    # Extract days and age groups
    days = df.iloc[:, 0].astype(int).values  # All rows, first column
    age_groups = header[1:]  # Use the header row for age group labels

    # Prepare data for the grid
    x, y, z = [], [], []

    for i, day in enumerate(days):
        for j, age_group in enumerate(age_groups):
            x.append(j)  # Use index for interpolation
            y.append(day)
            z_value = df.iloc[i, j + 1]  # Adjust indexing to skip header
            #z.append(z_value)  # Directly append the value without applying logarithm
            z.append(np.log10(z_value) if z_value > 0 else 0)  # Apply logarithm to z values



    # Check if x and y are not empty
    if len(x) > 0 and len(y) > 0:
        # Create a grid for interpolation
        xi, yi = np.meshgrid(np.linspace(0, len(age_groups) - 1, len(age_groups)),
                            np.linspace(min(y), max(y), len(days)))


        
        

        # Interpolate the data
        zi = griddata((x, y), z, (xi, yi), method='cubic')

        #Apply logarithmic transformation to the values for color scaling
        log_values = np.log10(zi + 1)  # Adding 1 to avoid log(0)


        # Create the 3D surface plot
        fig = go.Figure(data=[go.Surface(
            x=xi,
            y=yi,
            z=zi,
            surfacecolor=log_values,
            colorscale='HSV',  # Use HSV color palette
        )])

        # Update plot layout
        fig.update_layout(title='3D Mesh Grid Plot with Logarithmic Z Values', autosize=False,
                        width=800, height=800,
                        scene=dict(
                            xaxis=dict(
                                title='Age Groups',
                                tickmode='array',
                                tickvals=np.arange(len(age_groups)),
                                ticktext=age_groups,
                                tickfont=dict(size=10, color='black', family='Arial')
                            ),
                                                             
                            yaxis_title='Days',
                            zaxis_title='Values',
                            zaxis=dict(type='log')  # Set z-axis to logarithmic scale                                   
                            ),
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1,
                                xanchor="right",
                                x=0.8
                            ),  
                          )

        # Show the plot
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
