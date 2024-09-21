import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os
import shutil

def main():
    
    plot_name = "PVT_NUM_UVX_D window_7 step_300"
    

    # Import CSV file
    file_path = r"C:\CzechFOI-BYAGE\TERRA\PVT_NUM_UVX_D.csv"
    data = pd.read_csv(file_path)

    # Extract x-values from the CSV file
    x = data.iloc[:, 0].values

    # Parameters for the sliding histogram
    window_size = 7  # Size of the sliding window
    step_size = 300 # Step size for the sliding window

    # Function for creating a sliding histogram
    def moving_histogram(x, z, window_size, step_size):
        histograms = []
        x_steps = []
        for start in range(0, len(x) - window_size + 1, step_size):
            end = start + window_size
            # Remove NaN values from the window
            z_window = z[start:end]
            z_window = z_window[~np.isnan(z_window)]
            if len(z_window) > 0:
                hist, bins = np.histogram(z_window, bins=10)
                histograms.append(hist)
                x_steps.append(x[start + window_size // 2])  # Average value of the window as x-value
        return histograms, bins, x_steps
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Loop over AG columns 1 to 23
    for col in range(1, 24):
        z = data.iloc[:, col].values
        z_headertext = data.columns[col]

        # Calculate sliding histogram (all steps up to the end of the data)
        histograms, bins, x_steps = moving_histogram(x, z, window_size, step_size)

        # 3D visualisation of the histograms
        x_vals = bins[:-1]
        y_vals = np.array(x_steps)
        z_vals = np.array(histograms)

        fig = go.Figure(data=[go.Surface(z=z_vals, x=x_vals, y=y_vals)])

        fig.update_layout(
            title=f'rolling histogram {z_headertext}',
            scene=dict(
                xaxis_title='Deaths',
                yaxis_title='Days starting from 01.01.2020',
                zaxis_title='Frequency'
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=0.8
            ),
             legend_title='CSV Files'
        )

       #fig.show()
        fig.write_html(f"{full_plotfile_name} {z_headertext}.html")
        print(f"Plot for age band {z_headertext} has been saved to HTML file.")


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
