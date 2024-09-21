import pandas as pd
import plotly.express as px
import os
import shutil
import numpy as np

def main():
    
    plot_name = "PVT_NUM_VX_D"

    # Load the CSV file
    file_path = r'C:\CzechFOI-BYAGE\TERRA\PVT_NUM_VX_D.csv'
    data = pd.read_csv(file_path)

    # Apply a logarithmic transformation to the data to enhance small values
    data_transformed = data.iloc[:, 1:].applymap(lambda x: np.log1p(x))

     
    # Create the heatmap with Plasma color palette
    fig = px.imshow(data_transformed.T,  # Transpose the data to switch axes
                    labels=dict(x="Days", y="Age Groups", color="Log Values"),
                    x=data['DAYS_20200101'], 
                    y=data.columns[1:],
                    color_continuous_scale='Plasma')  # Use color scale Plasma Inferno Magma or Viridis    
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Update layout for better readability
    fig.update_layout(
        title=f"2D Heatmap of Values by Days and Age Groups {plot_name}",
        xaxis_title="Age Groups",
        yaxis_title="Days",
        coloraxis_colorbar=dict(title="Log Values"),
        legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=1
        ),
    )

    # Export plot to HTML
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