import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import shutil

def main():
    
    plot_name =  "PVT_NUM_VX_D_NORM"

    # Load the CSV file
    df = pd.read_csv(r'C:\github\CzechFOI-BYAGE\TERRA\PVT_NUM_VX_D_NORM.csv')

    # Calculate the moving average for each row (day)
    moving_avg_df = df.iloc[:, 1:].rolling(window=14, axis=1).mean()

    # Extract data for the plot
    x = np.tile(df.columns[1:], len(df))  # Repeat age groups for each day
    y = np.repeat(df['DAYS_20200101'], len(df.columns[1:]))  # Repeat days for each age group
    z = moving_avg_df.values.flatten()  # Flatten the 2D array to 1D

    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Transform z values to a logarithmic scale
    log_z = np.log10(z)

    # Create 3D scatter plot with pixel-like points and logarithmic color range
    fig = go.Figure(data=[go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode='markers',  # Use markers to represent the moving average
        marker=dict(
            size=0.5,  # Very small size for pixel-like points
            symbol='circle',  # Use circles
            color=log_z,  # Color by log-transformed z values
            colorscale='Viridis',
            opacity=0.8,
            cmin=np.log10(1),  # Set color range minimum to log(1)
            cmax=np.log10(1000)  # Set color range maximum to log(1000)
        )
    )])

    # Update layout for better visualization and set z-axis to logarithmic scale
    fig.update_layout(
        title='3D Moving Average Plot with Logarithmic Z-Axis and Color Scale',
        scene=dict(
            xaxis_title='Age Groups',
            yaxis_title='Days',
            zaxis_title='Values',
            xaxis=dict(tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=10)),
            zaxis=dict(tickfont=dict(size=10),            
                type='log',  # Set z-axis to logarithmic scale
                range=[0, 3]  # Logarithmic range from 10^0 to 10^3 (1 to 1000)
            )
        )
    )

    fig.show()
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