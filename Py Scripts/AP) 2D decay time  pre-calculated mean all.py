import pandas as pd
import numpy as np
import plotly.express as px
import os
import shutil

def main():

    plot_name = "PVT_CUM_NUM_UVX PVT_NUM_UVX_D TDT_7"
    avg_wnd_size = 30
    population_df = pd.read_csv(r"C:\github\CzechFOI-ByAge\TERRA\PVT_CUM_NUM_UVX.csv", sep=',')
    deaths_df = pd.read_csv(r"C:\github\CzechFOI-ByAge\TERRA\PVT_NUM_UVX_D.csv", sep=',')

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

    for age_group in df.columns[1:]:
        decay_times = []
        target_decay_time = 7  # Target decay time in days

        # Calculate the percentage for the target decay time
        max_days = df['DAYS_20200101'].max()  # get the whole day range
        all_death = deaths_df[age_group].sum()  # get the deaths for age group
        max_population = df[age_group].max()  # get the max population value

        target_percentage = ((all_death / max_population) / max_days) * target_decay_time
        percentage_dict[age_group] = target_percentage * 100  # Save the target percentage for legend

        for day in range(len(df)):
            decay_time = None
            # Only start the inner loop if the population is greater than 0
            if df[age_group].iloc[day] > 0:
                for future_day in range(day, len(df)):
                    mean_population = df[age_group].iloc[day:future_day+1].mean()
                    mean_deaths = deaths_df[age_group].iloc[day:future_day+1].mean()
                    deaths  = deaths_df[age_group].iloc[day:future_day+1].sum()

                    if mean_population > 0 and (deaths / mean_population) >= target_percentage:
                        decay_time = future_day - day  # Calculate the difference
                        break

            decay_times.append(decay_time if decay_time is not None else 0)       
        decay_times_df[age_group] = decay_times

    # Create a separate DataFrame for rolling averages
    rolling_avg_df = pd.DataFrame({'DAYS_20200101': df['DAYS_20200101']})

    # Calculate rolling average for 'Decay Time' with a window of 7 days
    for age_group in df.columns[1:]:
        rolling_avg_df[f'{age_group} Rolling Avg'] = decay_times_df[age_group].rolling(window=avg_wnd_size, min_periods=1).mean()

    # Convert data to long format for original decay times
    decay_times_long = decay_times_df.melt(id_vars=['DAYS_20200101'], var_name='Age Group', value_name='Decay Time')

    # Create interactive line plot with logarithmic scale
    fig = px.line(decay_times_long, x='DAYS_20200101', y='Decay Time', color='Age Group',
                title='Decay Time by Age Group over Days - Bigger values are better')

    # Add percentage to the legend for original decay times
    for trace in fig.data:
        if "Rolling Avg" not in trace.name:  # Only add percentage for the original decay times, not the rolling averages
            age_group = trace.name
            trace.name = f"{age_group} ({percentage_dict[age_group]:.6f}%)"

    # Now add the rolling averages to the plot
    # Convert rolling averages to long format
    rolling_avg_long = rolling_avg_df.melt(id_vars=['DAYS_20200101'], value_vars=[f'{age_group} Rolling Avg' for age_group in df.columns[1:]],
                                        var_name='Age Group', value_name='Decay Time (Rolling Avg)')

    # Add rolling averages to the figure
    for trace in rolling_avg_long['Age Group'].unique():
        fig.add_scatter(x=rolling_avg_long[rolling_avg_long['Age Group'] == trace]['DAYS_20200101'],
                        y=rolling_avg_long[rolling_avg_long['Age Group'] == trace]['Decay Time (Rolling Avg)'],
                        mode='lines', name=f"{trace} (Rolling Avg)", line=dict(dash='dash'))

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
