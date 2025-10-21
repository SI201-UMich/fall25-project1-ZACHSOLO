import pandas as pd
def load_penguin_data(csv_file):
    try:
        df = pd.read_csv(csv_file)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
        return None
    


def average_flipper_length_by_sex(df):
    df = df.dropna(subset = ['sex', 'flipper_length_mm', 'body_mass_g'])
    avg_flipper = df.groupby('sex')['flipper_length_mm'].mean().round(2)
    return avg_flipper.to_dict()


def max_body_mass_by_island(df):
    df = df.dropna(subset=['island', 'body_mass_g', 'species'])
    grouped = df.loc[df.groupby('island')['body_mass_g'].idmax(), ['island', 'species', 'body_mass_g']]
    result = grouped.set_index('island').to_dict(orient='index')
    return result

def save_results_to_csv(avg_flipper, max_mass, output_file="penguin_summary.csv"):
    avg_df = pd.DataFrame(list(avg_flipper.items()), columns = ['Sex', 'Average_Flipper_Length_mm'])
    mass_df = pd.DataFrame.from_dict(max_mass, orient='index').reset_index()
    mass_df.rename(columns={'index': 'Island', 'species': 'Heaviest_Species', 'body_mass_g': 'Max_Body_Mass_g'}, inplace=True)
    

    summary_df = pd.concat([avg_df, mass_df], axis=1)
    summary_df.to_csv(output_file, index=False)
    print(f"Results successfully written to '{output_file}'.")

def main


