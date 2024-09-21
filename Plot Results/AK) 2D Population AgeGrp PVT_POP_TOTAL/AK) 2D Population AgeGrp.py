import pandas as pd
import plotly.express as px
import os
import shutil

def main():
     
    plot_name = "PVT_POP_TOTAL"

    # Read the CSV file
    df = pd.read_csv(r"C:\github\CzechFOI-BYAGE\TERRA\PVT_POP_TOTAL.csv")

    # Melt the DataFrame to have a long format suitable for Plotly
    df_melted = df.melt(id_vars=['DAYS_20200101'], var_name='Age Group', value_name='Count')

    # Create the line plot
    fig = px.line(df_melted, x='DAYS_20200101', y='Count', color='Age Group', title='Age Group Counts Over Days')
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)
    
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