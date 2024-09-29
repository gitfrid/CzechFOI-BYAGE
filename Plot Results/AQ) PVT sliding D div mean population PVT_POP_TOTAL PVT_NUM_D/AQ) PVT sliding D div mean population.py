import pandas as pd
import plotly.graph_objects as go
import os
import shutil

def main():
    
    plot_name = "PVT_POP_TOTAL PVT_NUM_D"
    # Read the CSV files
    population_df = pd.read_csv(r"C:\github\CzechFOI-BYAGE\TERRA\PVT_POP_TOTAL.csv", sep=',')
    deaths_df = pd.read_csv(r"C:\github\CzechFOI-BYAGE\TERRA\PVT_NUM_D.csv", sep=',')

    # Ensure both dataframes have the same structure and align by 'DAYS_20200101'
    assert all(population_df['DAYS_20200101'] == deaths_df['DAYS_20200101']), "Date columns do not match!"

    # Calculate the actual population by subtracting cumulative deaths from cumulative population
    df = population_df.copy()
    for age_group in population_df.columns[1:]:
        df[age_group] = population_df[age_group] - deaths_df[age_group]

    # Determine the range value from the population_df
    range_value = len(population_df)
    
    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Loop through each age group to create individual plots
    for age_group in df.columns[1:]:

        # Initialize a list to collect data for the pivot DataFrame
        pivot_data = []
        
        # Initialize the pivot DataFrame with zeros
        pivot_df = pd.DataFrame(index=range(range_value), columns=range(range_value))
        pivot_df.index.name = 'DAYS_20200101'

        # Calculate the values for the pivot table
        for day in range(range_value):
            for future_day in range(day, range_value):
                mean_population = df[age_group].iloc[day:future_day+1].mean()
                deaths = deaths_df[age_group].iloc[day:future_day+1].sum()
                if mean_population > 0:
                    value = deaths / mean_population
                else:
                    value = 0
                pivot_df.at[day, future_day] = value


        # Collect the pivot DataFrame data
        pivot_data.append(pivot_df)

        # Concatenate all pivot DataFrames
        final_pivot_df = pd.concat(pivot_data, axis=1) 

        # Save the pivot DataFrame to a CSV file
        final_pivot_df.to_csv(f"{full_plotfile_name}_{age_group}.csv")

        # Read the values for the plot from the CSV file
        pivot_df = pd.read_csv(fr"{full_plotfile_name}_{age_group}.csv", index_col=0)

        # Plot the heatmap using Plotly
        fig = go.Figure(data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns,
            y=pivot_df.index,
            colorscale='turbo'
        ))

        fig.update_layout(
            title=f'Heatmap death div mean population over future Days for: {age_group}',
            xaxis_title='Future Day',
            yaxis_title='Day',
            autosize=False,
            width=1600,
            height=1200
        )

        # Save plot as HTML
        fig.write_html(f"{full_plotfile_name}_{age_group}.html")
        print(f"Plot has been saved to HTML file {full_plotfile_name}_{age_group}.html")

        # reset to empty fig
        fig.data = [] 

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
