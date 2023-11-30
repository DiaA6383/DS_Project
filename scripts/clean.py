import pandas as pd
import os

# Get the current directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Define the paths to the metadata, data, and cleaned data CSV files
METADATA_FILE_PATH = os.path.join(current_dir, '../data/raw/ACSST5Y2021.S1903_2023-11-14T204901/metadata.csv')
CSV_FILE_PATH = os.path.join(current_dir, '../data/raw/ACSST5Y2021.S1903_2023-11-14T204901/data.csv')
CLEANED_DATA_PATH = os.path.join(current_dir, '../data/processed/cleaned_data.csv')

def load_metadata(file_path):
    """
    Load metadata from a CSV file into a pandas DataFrame and create a dictionary for renaming columns.
    """
    metadata = pd.read_csv(file_path)
    rename_dict = dict(zip(metadata['Column Name'], metadata['Label']))
    return rename_dict


def load_data(file_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    """
    data = pd.read_csv(file_path, header=1)
    return data


def rename_columns(data):
    rename_dict = {
        'Geographic Area Name': 'Zip Code',
        'Number of Households': 'Total Households',
        'Number of Families!!With own children of householder under 18 years': 'Number Families with Children',
        'Number of Families!!With no own children of householder under 18 years': 'Number of Families with NO Children',
        'Number!!FAMILY INCOME BY NUMBER OF EARNERS!!No earners': 'Families with no Earners',
        'Percent Distribution!!FAMILIES!!Families': 'Family_Percent_Distribution',
        'Percent Distribution!!FAMILIES!!Families!!With own children of householder under 18 years': 'Family_with_Children_Percent',
        'Percent Distribution!!FAMILIES!!Families!!With no own children of householder under 18 years': 'Family_no_Children_Percent',
        'Median income (dollars)!!HOUSEHOLD INCOME BY RACE AND HISPANIC OR LATINO ORIGIN OF HOUSEHOLDER!!Households': 'Household_Median_Income',
        'Median income (dollars)!!FAMILIES!!Families': 'Family_Median_Income'
    }
    data.rename(columns=rename_dict, inplace=True)
    return data

def clean_data(data):
    """
    Clean the data by dropping unnecessary columns, and modifying column values.
    """
    data['Zip Code'] = data['Zip Code'].str.replace('ZCTA5 ', '')
    data.drop(columns=['Geography'], inplace=True)
    data.drop(data.columns[data.columns.str.startswith(('Annotation', 'Margin of Error!!'))], axis=1, inplace=True)
    data.columns = data.columns.str.replace('Estimate!!', '')
    data.columns = data.columns.str.replace('Number!!HOUSEHOLD INCOME BY RACE AND HISPANIC OR LATINO ORIGIN OF HOUSEHOLDER!!', 'Number of ')
    data.columns = data.columns.str.replace("Number!!FAMILIES!!", "Number of ")
    data.columns = data.columns.str.replace("Number of Families!!With own children of householder under 18 years", "Number of Families with Children")
    data.columns = data.columns.str.replace("Number of Families!!With no own children of householder under 18 years", "Number of Families with NO Children")
    data.columns = data.columns.str.replace("Number!!FAMILY INCOME BY NUMBER OF EARNERS!!No earners", "Families with no Earners")
    data.columns = data.columns.str.replace("Percent Distribution!!FAMILIES!!", "Percent Distribution of ")
    data.columns = data.columns.str.replace("Percent Distribution of Families!!With own children of householder under 18 years", "Percent Distribution of Families with Children")
    data.columns = data.columns.str.replace("Percent Distribution of Families!!With no own children of householder under 18 years", "Percent Distribution of Families with NO Children")
    data.columns = data.columns.str.replace("Median income (dollars)!!HOUSEHOLD INCOME BY RACE AND HISPANIC OR LATINO ORIGIN OF HOUSEHOLDER!!Households", "Median Income of all Households") 
    data.columns = data.columns.str.replace("Median income (dollars)!!FAMILIES!!Families", "Median Income of all Families")
     # Handle special values like "250,000+"
    # For example, convert "250,000+" to 250000 in 'Median Income of all Families' column
    data['Median Income of all Families'] = data['Median Income of all Families'].replace('250,000+', '250000')

    # Convert the 'Median Income of all Families' column to numeric
    data['Median Income of all Families'] = pd.to_numeric(data['Median Income of all Families'], errors='coerce')
    data.drop(data.columns[2:15], axis=1, inplace=True)
    data.drop(data.columns[5:17], axis=1, inplace=True)
    data.drop(data.columns[6:26], axis=1, inplace=True)
    data.drop(data.columns[6:10], axis=1, inplace=True)
    data.drop(data.columns[9: 32], axis=1, inplace=True)
    data.drop(data.columns[10: 23], axis=1, inplace=True)
    data.drop(data.columns[11::], axis=1, inplace=True)
    return data


def main():
    """
    Main function to load, rename, clean, and save the data.
    """
    # Load the data
    data = load_data(CSV_FILE_PATH)
    data = rename_columns(data)
    cleaned_data = clean_data(data)
    cleaned_data.to_csv(CLEANED_DATA_PATH, index=False)
if __name__ == '__main__':
    main()