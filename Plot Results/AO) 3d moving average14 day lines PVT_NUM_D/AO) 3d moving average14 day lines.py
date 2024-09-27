import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import shutil

def main():
    
    plot_name =  "PVT_NUM_D"

    # Load the CSV file
    df = pd.read_csv(r'C:\github\CzechFOI-BYAGE\TERRA\PVT_NUM_D.csv')

    # Calculate the moving average for each column (age group)
    moving_avg_df = df.iloc[:, 1:].rolling(window=14, axis=0).mean()

    # Extract data for the plot
    x = np.tile(df.columns[1:], len(df))  # Repeat age groups for each day
    y = np.repeat(df['DAYS_20200101'], len(df.columns[1:]))  # Repeat days for each age group
    z = moving_avg_df.values.flatten()  # Flatten the 2D array to 1D

    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Create 3D line plot with linear color range
    fig = go.Figure()

    # Plot each age group as a separate line
    for i, age_group in enumerate(df.columns[1:]):
        fig.add_trace(go.Scatter3d(
            x=[age_group] * len(df),  # Age group repeated for each day
            y=df['DAYS_20200101'],  # Days
            z=moving_avg_df.iloc[:, i],  # Moving average values for the age group
            mode='lines',  # Use lines to represent the moving average
            line=dict(
                color=z[i::len(df.columns[1:])],  # Color by linear z values
                colorscale='Plasma',  # Use the Viridis colormap
                width=2,  # Line width
                cmin=0,  # Set color range minimum to 0
                cmax=z.max()  # Set color range maximum to the max z value
            ),
            name=f'Age Group {age_group}'
        ))

    # Update layout for better visualization
    fig.update_layout(
        title='3D Moving Average Plot with Linear Z-Axis and Color Scale',
        scene=dict(
            xaxis_title='Age Groups',
            yaxis_title='Days',
            zaxis_title='Values',
            xaxis=dict(tickfont=dict(size=10)),
            yaxis=dict(tickfont=dict(size=10)),
            zaxis=dict(tickfont=dict(size=10),              
                range=[0, z.max()]  # Linear range from 0 to max z value
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