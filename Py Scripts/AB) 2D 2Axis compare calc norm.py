import pandas as pd
import plotly.graph_objects as go
import os
import shutil

def main():
    
    plot_name = "PVT_CUM_NUM_D PVT_CUM_NUM CALC"

    # List of CSV file paths
    csv_files = [
        r"C:\CzechFOI-BYAGE\TERRA\PVT_CUM_NUM_VX_D.csv",
        r"C:\CzechFOI-BYAGE\TERRA\PVT_CUM_NUM_UVX_D.csv",
        r"C:\CzechFOI-BYAGE\TERRA\PVT_CUM_NUM_VX.csv",
        r"C:\CzechFOI-BYAGE\TERRA\PVT_CUM_NUM_UVX.csv"
    ]

    # Read all CSV files into a list of DataFrames
    dataframes = [pd.read_csv(file) for file in csv_files]

    # Get the list of age bands from the columns (excluding the first column which is 'days')
    age_bands = dataframes[0].columns[1:]

    # ** Normalize the data per 100,000 for the first two CSV files **
    # ** used to check if comapaired with the normalized pivot data by SQlite query gives same plot result** 
    for i in range(2):
        for age_band in age_bands:
            dataframes[i][age_band] = dataframes[i][age_band] / dataframes[i + 2][age_band] * 100000

    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Create a plot for each age band
    for age_band in age_bands:
        fig = go.Figure()
        
        # Add traces for the first two CSV files on the primary y-axis
        fig.add_trace(go.Scatter(x=dataframes[0].iloc[:, 0], y=dataframes[0][age_band], mode='lines', name=csv_files[0]))
        fig.add_trace(go.Scatter(x=dataframes[1].iloc[:, 0], y=dataframes[1][age_band], mode='lines', name=csv_files[1]))
        
        # Add traces for the second two CSV files on the secondary y-axis
        fig.add_trace(go.Scatter(x=dataframes[2].iloc[:, 0], y=dataframes[2][age_band], mode='lines', name=csv_files[2], yaxis='y2'))
        fig.add_trace(go.Scatter(x=dataframes[3].iloc[:, 0], y=dataframes[3][age_band], mode='lines', name=csv_files[3], yaxis='y2'))
        
        # Update layout for secondary y-axis
        fig.update_layout(
            title=f'Age Group PVT_NUM_D cumulated compared: {age_band}',
            xaxis_title='Days',
            yaxis_title='Values per 100,000',
            yaxis2=dict(
                title='Cumulative Values',
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
