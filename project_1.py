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