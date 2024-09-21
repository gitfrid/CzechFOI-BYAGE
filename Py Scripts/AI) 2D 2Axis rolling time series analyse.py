import numpy as np
import pandas as pd
import plotly.graph_objects as go
import os
import shutil

def main():
    
    plot_name = "window7 PVT_NUM_VX_D PVT_CUM_NUM_VX"  

    # CSV-Dateien einlesen
    file_path1 = r"C:\CzechFOI-BYAGE\TERRA\PVT_NUM_VX_D.csv"
    file_path2 = r"C:\CzechFOI-BYAGE\TERRA\PVT_CUM_NUM_VX.csv"

    data1 = pd.read_csv(file_path1)
    data2 = pd.read_csv(file_path2)

    # x-Werte aus den CSV-Dateien extrahieren (assuming these are numerical values)
    x1 = data1.iloc[:, 0].values
    x2 = data2.iloc[:, 0].values

    # Parameter für das gleitende Fenster
    window_size = 7  # Größe des gleitenden Fensters
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Schleife über die Spalten 1 bis 23 für beide Dateien
    for col in range(1, 24):
        z1 = data1.iloc[:, col].values
        z2 = data2.iloc[:, col].values
        age_grp = data1.columns[col]
        z_headertext1 = "PVT_NUM_VX_D_NORM"
        z_headertext2 = "PVT_NUM_UVX_D_NORM"

        # DataFrames erstellen
        df1 = pd.DataFrame({'X': x1, 'Value': z1})
        df2 = pd.DataFrame({'X': x2, 'Value': z2})
        df1.set_index('X', inplace=True)
        df2.set_index('X', inplace=True)

        # Gleitender Mittelwert und Standardabweichung berechnen
        rolling_mean1 = df1['Value'].rolling(window=window_size).mean()
        rolling_std1 = df1['Value'].rolling(window=window_size).std()
        rolling_mean2 = df2['Value'].rolling(window=window_size).mean()
        rolling_std2 = df2['Value'].rolling(window=window_size).std()

        # Plot erstellen
        fig = go.Figure()

        # Originaldaten hinzufügen
        fig.add_trace(go.Scatter(x=df1.index, y=df1['Value'], mode='lines', name=f'Original Data {z_headertext1}'))
        fig.add_trace(go.Scatter(x=df2.index, y=df2['Value'], mode='lines', name=f'Original Data {z_headertext2}'))

        # Gleitender Mittelwert hinzufügen
        fig.add_trace(go.Scatter(x=rolling_mean1.index, y=rolling_mean1, mode='lines', name=f'Rolling Mean {z_headertext1}'))
        fig.add_trace(go.Scatter(x=rolling_mean2.index, y=rolling_mean2, mode='lines', name=f'Rolling Mean {z_headertext2}'))

        # Gleitende Standardabweichung hinzufügen
        fig.add_trace(go.Scatter(x=rolling_std1.index, y=rolling_std1, mode='lines', name=f'Rolling Std Dev {z_headertext1}'))
        fig.add_trace(go.Scatter(x=rolling_std2.index, y=rolling_std2, mode='lines', name=f'Rolling Std Dev {z_headertext2}'))

        fig.update_layout(
            legend=dict(
                orientation="v",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1
            ),
            title=f'Time Series Analysis {age_grp} {z_headertext1} and {z_headertext2}',
            xaxis_title='X',
            yaxis_title='Value'
        )

        fig.write_html(f"{full_plotfile_name} {age_grp}.html")
        print(f"Plot for age band {age_grp} has been saved to HTML file.")


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
