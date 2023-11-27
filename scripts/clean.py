import pandas as pd

# Define the paths to the metadata, data, and cleaned data CSV files
METADATA_FILE_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/ACSST5Y2021.S1903_2023-11-14T204901/metadata.csv'
DATA_FILE_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/ACSST5Y2021.S1903_2023-11-14T204901/data.csv'
CLEANED_DATA_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'

def load_csv(file_path):
    return pd.read_csv(file_path, header=1)

def get_rename_dict(metadata):
    return dict(zip(metadata['Column Name'], metadata['Label']))

def rename_columns(data, rename_dict):
    data.rename(columns=rename_dict, inplace=True)
    return data

def clean_data(data):
    data.rename(columns={'Geographic Area Name': 'Zip Code'}, inplace=True)
    data['Zip Code'] = data['Zip Code'].str.replace('ZCTA5 ', '')
    data.drop(columns=['Geography'], inplace=True)
    data.drop(data.columns[data.columns.str.startswith(('Annotation', 'Margin of Error!!'))], axis=1, inplace=True)
    data.columns = data.columns.str.replace('Estimate!!', '')
    data.columns = data.columns.str.replace('Number!!HOUSEHOLD INCOME BY RACE AND HISPANIC OR LATINO ORIGIN OF HOUSEHOLDER!!', 'Number of ')
    data.columns = data.columns.str.replace("Number!!FAMILIES!!", "Number of ")
    data.drop(data.columns[2:15], axis=1, inplace=True)
    data.rename(columns={'Number of Households': 'Total Households'}, inplace=True)
    data.rename(columns={'Number of Families!!With own children of householder under 18 years': 'Number Families with Children'}, inplace=True)
    data.rename(columns={'Number of Families!!With no own children of householder under 18 years': 'Number of Families with NO Children'}, inplace=True)
    data.rename(columns={'Number!!FAMILY INCOME BY NUMBER OF EARNERS!!No earners': 'Families with no Earners'}, inplace=True)
    data.drop(data.columns[5:17], axis=1, inplace=True)
    data.drop(data.columns[6:26], axis=1, inplace=True)
    data.drop(data.columns[6:10], axis=1, inplace=True)
    data.drop(data.columns[9: 32], axis=1, inplace=True)
    data.drop(data.columns[10: 23], axis=1, inplace=True)
    data.drop(data.columns[11::], axis=1, inplace=True)
    return data

def main():
    metadata = load_csv(METADATA_FILE_PATH)
    rename_dict = get_rename_dict(metadata)
    data = load_csv(DATA_FILE_PATH)
    data = rename_columns(data, rename_dict)
    cleaned_data = clean_data(data)
    cleaned_data.to_csv(CLEANED_DATA_PATH, index=False)

if __name__ == '__main__':
    main()