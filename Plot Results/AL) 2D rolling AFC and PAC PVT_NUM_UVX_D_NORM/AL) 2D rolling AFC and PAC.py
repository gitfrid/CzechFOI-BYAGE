import numpy as np
import pandas as pd
import plotly.graph_objects as go
from statsmodels.tsa.stattools import acf, pacf
import os
import shutil

def main():
           
    plot_name = "PVT_NUM_UVX_D_NORM"

    # CSV-Datei einlesen
    file_path = r"C:\github\CzechFOI-BYAGE\TERRA\PVT_NUM_UVX_D_NORM.csv"
    data = pd.read_csv(file_path)

    # x-Werte aus der CSV-Datei extrahieren
    x = data.iloc[:, 0].values
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Schleife über die Spalten 1 bis 23
    for col in range(1, 24):
        z = data.iloc[:, col].values
        z_headertext = data.columns[col]

        # ACF und PACF berechnen
        acf_values = acf(z, nlags=40)
        pacf_values = pacf(z, nlags=40)

        # ACF plot
        fig_acf = go.Figure()
        fig_acf.add_trace(go.Scatter(x=np.arange(len(acf_values)), y=acf_values, mode='lines+markers', name='ACF'))
        fig_acf.update_layout(
            title=f'ACF for {z_headertext}',
            xaxis_title='Lag',
            yaxis_title='Autocorrelation'
        )      
        fig_acf.write_html(rf"{full_plotfile_name} acf {z_headertext}.html")
        print(f"Plot acf for age band {z_headertext} has been saved to HTML file.")

        # PACF plot
        fig_pacf = go.Figure()
        fig_pacf.add_trace(go.Scatter(x=np.arange(len(pacf_values)), y=pacf_values, mode='lines+markers', name='PACF'))
        fig_pacf.update_layout(
            title=f'PACF for {z_headertext}',
            xaxis_title='Lag',
            yaxis_title='Partial Autocorrelation'
        )
        
        fig_pacf.write_html(rf"{full_plotfile_name} pacf {z_headertext}.html")
        #fig_pacf.show()
        print(f"Plot pacf for age band {z_headertext} has been saved to HTML file.")


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
