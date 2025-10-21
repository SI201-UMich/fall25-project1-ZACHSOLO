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