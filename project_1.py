#Name: Zachary Solomon
#Student ID: 25386711
#Email: zsolly@umich.edu
#Who or what you worked with on this project: I orignally was in a group for this project, but decided it would be for the best to work alone after the first checkpoint.
#I used chatgpt with some help structuring my test cases and a couple pandas functions
#My knowledge in pandas comes from my father, he was a compsci major in college and helped me work through this project
#along with consulting him for help i also used chatgpt to help me go about creating a new csv file to store my output in.


import pandas as pd
import unittest

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
    grouped = df.loc[df.groupby('island')['body_mass_g'].idxmax(), ['island', 'species', 'body_mass_g']]
    result = grouped.set_index('island').to_dict(orient='index')
    return result

def save_results_to_csv(avg_flipper, max_mass, output_file="penguin_summary.csv"):
    avg_df = pd.DataFrame(list(avg_flipper.items()), columns = ['Sex', 'Average_Flipper_Length_mm'])
    mass_df = pd.DataFrame.from_dict(max_mass, orient='index').reset_index()
    mass_df.rename(columns={'index': 'Island', 'species': 'Heaviest_Species', 'body_mass_g': 'Max_Body_Mass_g'}, inplace=True)
    

    summary_df = pd.concat([avg_df, mass_df], axis=1)
    summary_df.to_csv(output_file, index=False)
    print(f"Results successfully written to '{output_file}'.")


class TestPenguinFunctions(unittest.TestCase):
    """Unit tests for penguin dataset analysis functions."""


    # average_flipper_length_by_sex tests


    # General / usual cases
    def test_avg_flipper_general_case_1(self):
        df = pd.DataFrame({
            'sex': ['Male', 'Female', 'Male', 'Female'],
            'flipper_length_mm': [200, 180, 210, 190],
            'body_mass_g': [4000, 3500, 4200, 3600]
        })
        expected = {'Female': 185.0, 'Male': 205.0}
        self.assertEqual(average_flipper_length_by_sex(df), expected)

    def test_avg_flipper_general_case_2(self):
        df = pd.DataFrame({
            'sex': ['Male', 'Female', 'Female'],
            'flipper_length_mm': [210, 195, 185],
            'body_mass_g': [4200, 3500, 3300]
        })
        expected = {'Female': 190.0, 'Male': 210.0}
        self.assertEqual(average_flipper_length_by_sex(df), expected)

    # Edge cases
    def test_avg_flipper_edge_missing_values(self):
        df = pd.DataFrame({
            'sex': ['Male', 'Female', None],
            'flipper_length_mm': [200, None, 210],
            'body_mass_g': [4000, 3600, 4200]
        })
        expected = {'Male': 200.0}
        self.assertEqual(average_flipper_length_by_sex(df), expected)

    def test_avg_flipper_edge_one_sex_only(self):
        df = pd.DataFrame({
            'sex': ['Male', 'Male', 'Male'],
            'flipper_length_mm': [200, 210, 220],
            'body_mass_g': [4000, 4100, 4200]
        })
        expected = {'Male': 210.0}
        self.assertEqual(average_flipper_length_by_sex(df), expected)


   
    # max_body_mass_by_island tests


    # General / usual cases
    def test_max_mass_general_case_1(self):
        df = pd.DataFrame({
            'island': ['Dream', 'Biscoe', 'Dream', 'Torgersen'],
            'body_mass_g': [3500, 4000, 3700, 3800],
            'species': ['Adelie', 'Gentoo', 'Adelie', 'Chinstrap']
        })
        expected = {
            'Biscoe': {'species': 'Gentoo', 'body_mass_g': 4000},
            'Dream': {'species': 'Adelie', 'body_mass_g': 3700},
            'Torgersen': {'species': 'Chinstrap', 'body_mass_g': 3800}
        }
        self.assertEqual(max_body_mass_by_island(df), expected)

    def test_max_mass_general_case_2(self):
        df = pd.DataFrame({
            'island': ['Dream', 'Dream', 'Biscoe'],
            'body_mass_g': [3200, 3400, 3600],
            'species': ['Adelie', 'Gentoo', 'Chinstrap']
        })
        expected = {
            'Dream': {'species': 'Gentoo', 'body_mass_g': 3400},
            'Biscoe': {'species': 'Chinstrap', 'body_mass_g': 3600}
        }
        self.assertEqual(max_body_mass_by_island(df), expected)

    # Edge cases
    def test_max_mass_edge_duplicate_values(self):
        df = pd.DataFrame({
            'island': ['Dream', 'Dream', 'Biscoe'],
            'body_mass_g': [3600, 3600, 3500],
            'species': ['Adelie', 'Gentoo', 'Chinstrap']
        })
        result = max_body_mass_by_island(df)
        self.assertIn('Dream', result)
        self.assertEqual(result['Dream']['body_mass_g'], 3600)

    def test_max_mass_edge_missing_values(self):
        df = pd.DataFrame({
            'island': ['Dream', 'Biscoe', 'Dream', 'Torgersen'],
            'body_mass_g': [3500, None, 3700, None],
            'species': ['Adelie', 'Gentoo', 'Adelie', 'Chinstrap']
        })
        expected = {'Dream': {'species': 'Adelie', 'body_mass_g': 3700}}
        self.assertEqual(max_body_mass_by_island(df), expected)


def main():
    df = load_penguin_data("/Users/zacharysolomon/Documents/SI206/fall25-project1-ZACHSOLO/penguins.csv")
    if df is None:
        return
    
    avg_flipper = average_flipper_length_by_sex(df)
    max_mass = max_body_mass_by_island(df)
    print("Average Flipper Length by Sex:")
    print(avg_flipper)
    print("\nMaximum Body Mass per Island:")
    print(max_mass)
    
    save_results_to_csv(avg_flipper, max_mass)


if __name__ == "__main__":
    main()
    unittest.main()


