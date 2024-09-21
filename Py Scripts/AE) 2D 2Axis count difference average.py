import pandas as pd
import plotly.graph_objects as go
import os
import shutil

def main():
    
    plot_name = "PVT_NUM_D PVT_NUM_D_NORM"
    # List of CSV file paths for the primary y-axis

    # Liste der CSV-Dateipfade für die primäre y-Achse
    csv_files_primary = [
        r"C:\CzechFOI-BYAGE\TERRA\PVT_NUM_UVX_D.csv",
        r"C:\CzechFOI-BYAGE\TERRA\PVT_NUM_VX_D.csv"
    ]

    # Liste der CSV-Dateipfade für die sekundäre y-Achse
    csv_files_secondary = [
        r"C:\CzechFOI-BYAGE\TERRA\PVT_NUM_UVX_D_NORM.csv",
        r"C:\CzechFOI-BYAGE\TERRA\PVT_NUM_VX_D_NORM.csv"
    ]

    # Read all CSV files into a list of DataFrames
    dataframes_primary = [pd.read_csv(file) for file in csv_files_primary]
    dataframes_secondary = [pd.read_csv(file) for file in csv_files_secondary]

    # Get the list of age bands from the columns (excluding the first column which is 'days')
    age_bands = dataframes_primary[0].columns[1:]

    # Function to normalize and filter the signals
    def normalize_and_filter(df_primary, df_secondary):
        normalized_signals = {}
        for age_band in age_bands:
            # Normalize the primary signal
            normalized_signal = (df_primary[age_band] / df_secondary[age_band]) * 100000
            
            # Apply difference filter
            diff_filtered_signal = normalized_signal.diff().fillna(0)
            
            # Apply moving average to smooth the signal
            smoothed_signal = diff_filtered_signal.rolling(window=7).mean().fillna(0)
            
            normalized_signals[age_band] = smoothed_signal
        return normalized_signals
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Create a plot for each age band
    for age_band in age_bands:
        fig = go.Figure()
        
        # Add traces for the primary y-axis
        for df_primary, df_secondary, file in zip(dataframes_primary, dataframes_secondary, csv_files_primary):
            normalized_signals = normalize_and_filter(df_primary, df_secondary)
            fig.add_trace(go.Scatter(x=df_primary.iloc[:, 0], y=normalized_signals[age_band], mode='lines', name=file))
        
        # Add traces for the secondary y-axis
        for df, file in zip(dataframes_secondary, csv_files_secondary):
            fig.add_trace(go.Scatter(x=df.iloc[:, 0], y=df[age_band], mode='lines', name=file, yaxis='y2'))
        
        # Update layout to include a secondary y-axis
        fig.update_layout(
            title=f'Age Band PVT_NUM_D cumulated compared: {age_band}',
            xaxis_title='Days',
            yaxis_title='Values (Primary)',
            yaxis2=dict(
                title='Values (Secondary)',
                overlaying='y',
                side='right'
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
        
        # Save the plot to an HTML file
        fig.write_html(f"{full_plotfile_name} {age_band}.html")
        print(f"Plot for age band {age_band} has been saved to HTML file.")


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