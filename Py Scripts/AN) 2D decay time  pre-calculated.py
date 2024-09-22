import pandas as pd
import numpy as np
import plotly.express as px
import os
import shutil

def main():
    
    plot_name = "PVT_POP_TOTAL_MINUS_D"

    # Read the CSV file
    df = pd.read_csv(r"C:\github\CzechFOI-ByAge\TERRA\PVT_POP_TOTAL_MINUS_D.csv", sep=',')

    # Initialize the directory and script copy
    full_plotfile_name = init_function(plot_name)

    # Calculate decay time for each age group
    decay_times_df = pd.DataFrame({'DAYS_20200101': df['DAYS_20200101']})
    # Dictionaryto save percentage values
    percentage_dict = {}

    for age_group in df.columns[1:]:
        decay_times = []
        target_decay_time = 100  # Target decay time in days

        # Calculate the percentage for the target decay time
        initial_population = df[age_group].iloc[0]  # Assuming the initial population is the first value
        percentage = 1 - (initial_population - target_decay_time) / initial_population
        percentage_dict[age_group] = percentage * 100  # Speichere den Prozentsatz

        for day in range(len(df)):
            initial_population = df[age_group].iloc[day]
            target_population = initial_population * (1 - percentage)

            decay_time = None
            for future_day in range(day, len(df)):
                current_population = df[age_group].iloc[future_day]
                if current_population <= target_population:
                    decay_time = future_day - day  # Calculate the difference
                    break
            decay_times.append(decay_time)
        decay_times_df[age_group] = decay_times

    # Convert data to long format
    decay_times_long = decay_times_df.melt(id_vars=['DAYS_20200101'], var_name='Age Group', value_name='Decay Time')

    # Create interactive line plot with logarithmic scale
    fig = px.line(decay_times_long, x='DAYS_20200101', y='Decay Time', color='Age Group', 
                title='Decay Time by Age Group over Time')
    #fig.update_layout(yaxis_type="log")
    
    # add percentage to the legend
    for trace in fig.data:
        age_group = trace.name
        trace.name = f"{age_group} ({percentage_dict[age_group]:.2f}%)"

    # Save plot as HTML
    fig.write_html(f"{full_plotfile_name}.html")
    print(f"Plot has been saved to HTML file {full_plotfile_name}")


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
