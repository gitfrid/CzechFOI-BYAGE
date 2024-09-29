import pandas as pd
import numpy as np
import plotly.express as px
import os
import shutil

def main():
    
    plot_name = "PVT_CUM_NUM_VX PVT_NUM_VX_D TDT_7"

    population_df = pd.read_csv(r"C:\CzechFOI-ByAge\TERRA\PVT_CUM_NUM_VX.csv", sep=',')
    deaths_df = pd.read_csv(r"C:\CzechFOI-ByAge\TERRA\PVT_NUM_VX_D.csv", sep=',')

    # Ensure both dataframes have the same structure and align by 'DAYS_20200101'
    assert all(population_df['DAYS_20200101'] == deaths_df['DAYS_20200101']), "Date columns do not match!"

    # Calculate the actual population by subtracting cumulative deaths from cumulative population
    df = population_df.copy()
    for age_group in population_df.columns[1:]:
        df[age_group] = population_df[age_group] - deaths_df[age_group]

    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Calculate decay time for each age group
    decay_times_df = pd.DataFrame({'DAYS_20200101': df['DAYS_20200101']})
    
    # Dictionary to save percentage values for legend
    percentage_dict = {}
    debg = False
    for age_group in df.columns[1:]:
        decay_times = []
        target_decay_time = 7  # Target decay time in days

        # Calculate the percentage for the target decay time
        max_days =  df['DAYS_20200101'].max() # get the whole day range
        all_death = deaths_df[age_group].sum()  # get the deaths for age group
        max_population = df[age_group].max()  # get the max population value

        target_percentage = ((all_death / max_population) / max_days) * target_decay_time       
        percentage_dict[age_group] = target_percentage * 100  # Save the target percentage for legend

        #with open(f'{full_plotfile_name}{age_group}debug_info.txt', 'w') as f:
        for day in range(len(df)):
                decay_time = None
                # Only start the inner loop if the population is greater than 0
                if df[age_group].iloc[day] > 0:
                    for future_day in range(day, len(df)):
                        mean_population = df[age_group].iloc[day:future_day+1].mean()
                        mean_deaths = deaths_df[age_group].iloc[day:future_day+1].mean()
                        deaths  = deaths_df[age_group].iloc[day:future_day+1].sum()
                        # debug info
                        #f.write(f"AG: {age_group}, Day: {day}, Future Day: {future_day}, TP: {target_percentage}, DdivMpop: {deaths / mean_population}, Deaths: {deaths}, Mean Deaths: {mean_deaths}, Mean Population: {mean_population}\n")

                        if mean_population > 0 and ( deaths / mean_population) >= target_percentage:
                            decay_time = future_day - day  # Calculate the difference
                            break   
                   
                decay_times.append(decay_time if decay_time is not None else 0)       
        decay_times_df[age_group] = decay_times
        
        # Convert data to long format
        decay_times_long = decay_times_df.melt(id_vars=['DAYS_20200101'], var_name='Age Group', value_name='Decay Time')

    # Loop through each age group and create a separate plot
    for age_group in decay_times_long['Age Group'].unique():
        # Filter data for the current age group
        age_group_data = decay_times_long[decay_times_long['Age Group'] == age_group]

        # Create interactive line plot with logarithmic scale
        fig = px.line(age_group_data, x='DAYS_20200101', y='Decay Time',
                    title=f'Decay Time for {age_group} over Days - bigger values are better')

        # Add percentage to the legend
        fig.update_layout(showlegend=True)
        fig.for_each_trace(lambda trace: trace.update(name=f"{age_group} ({percentage_dict[age_group]:.6f}%)"))

        # Save plot as HTML
        plot_filename = f"{full_plotfile_name}_{age_group}.html"
        fig.write_html(plot_filename)
        print(f"Plot for {age_group} has been saved to HTML file {plot_filename}")


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
