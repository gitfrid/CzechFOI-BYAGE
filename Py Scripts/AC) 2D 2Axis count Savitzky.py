import pandas as pd
import plotly.graph_objects as go
from scipy.signal import savgol_filter
import os
import shutil

def main():
    
    plot_name = "PVT_NUM_D PVT_CUM_NUM"

    # Funktion zur Anwendung des Savitzky-Golay-Filters
    def apply_savgol_filter(data, window_size, poly_order):
        return savgol_filter(data, window_size, poly_order)

    # Liste der CSV-Dateipfade für die primäre y-Achse
    csv_files_primary = [
        r"C:\CzechFOI-BYAGE\TERRA\PVT_NUM_UVX_D.csv",
        r"C:\CzechFOI-BYAGE\TERRA\PVT_NUM_VX_D.csv"
    ]

    # Liste der CSV-Dateipfade für die sekundäre y-Achse
    csv_files_secondary = [
        r"C:\CzechFOI-BYAGE\TERRA\PVT_CUM_NUM_UVX.csv",
        r"C:\CzechFOI-BYAGE\TERRA\PVT_CUM_NUM_VX.csv"
    ]

    # Alle CSV-Dateien in eine Liste von DataFrames einlesen
    dataframes_primary = [pd.read_csv(file) for file in csv_files_primary]
    dataframes_secondary = [pd.read_csv(file) for file in csv_files_secondary]

    # Liste der Altersgruppen aus den Spalten (ohne die erste Spalte, die 'days' ist)
    age_bands = dataframes_primary[0].columns[1:]

    # Fenstergröße und Polynomgrad für den Savitzky-Golay-Filter
    #window_size = 51  # Muss ungerade sein
    #poly_order = 3

    window_size = 101  # Muss ungerade sein
    poly_order = 2
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Ein Diagramm für jede Altersgruppe erstellen
    for age_band in age_bands:
        fig = go.Figure()
        
        # Traces für die primäre y-Achse hinzufügen
        for df, file in zip(dataframes_primary, csv_files_primary):
            smoothed_data = apply_savgol_filter(df[age_band], window_size, poly_order)
            fig.add_trace(go.Scatter(x=df.iloc[:, 0], y=smoothed_data, mode='lines', name=file))
        
        # Traces für die sekundäre y-Achse hinzufügen
        for df, file in zip(dataframes_secondary, csv_files_secondary):
            smoothed_data = apply_savgol_filter(df[age_band], window_size, poly_order)
            fig.add_trace(go.Scatter(x=df.iloc[:, 0], y=smoothed_data, mode='lines', name=file, yaxis='y2'))
        
        # Layout aktualisieren, um eine sekundäre y-Achse einzuschließen
        fig.update_layout(
            title=f'Altersgruppe PVT_NUM_D kumuliert verglichen: {age_band}',
            xaxis_title='Tage',
            yaxis_title='Werte (Primär)',
            yaxis2=dict(
                title='Werte (Sekundär)',
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
            legend_title='CSV-Dateien'
        )
        
        # save as  HTML-File
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
