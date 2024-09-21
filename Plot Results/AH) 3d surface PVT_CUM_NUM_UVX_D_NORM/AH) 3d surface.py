import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import shutil

def main():
    
    plot_name =  "PVT_CUM_NUM_UVX_D_NORM"

        
    # Load the CSV data
    data = pd.read_csv(r"C:\CzechFOI-BYAGE\TERRA\PVT_CUM_NUM_UVX_D_NORM.csv")

    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Extract the headers and data
    headers = data.columns[1:]  # Skip the first column which is 'DAYS_20200101'
    days = data.iloc[:, 0]  # First column
    values = data.iloc[:, 1:].values  # All other columns

    # Create a meshgrid for the surface plot
    x, y = np.meshgrid(headers, days)

    # Create the 3D surface plot
    fig = go.Figure(data=[go.Surface(z=values, x=x, y=y,
                                    colorscale='HSV',  # Use HSV color palette
                                    )])

    # Update layout for better visualization
    fig.update_layout(
        title='3D Surface Plot',autosize=False,
                        width=800, height=800,
        scene=dict(
                    xaxis=dict(
                                title='Age Groups',
                                tickmode='array',
                                tickfont=dict(size=10, color='black', family='Arial')
                            ),
            xaxis_title='Age Groups',
            yaxis_title='Days',
            zaxis_title='Values'
            
        ),
        legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1,
                xanchor="right",
                x=0.8
        ),
    )

    # Export to HTML

    #fig.show()
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