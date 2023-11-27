import pandas as pd

# Define the paths to the metadata, data, and cleaned data CSV files
METADATA_FILE_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/ACSST5Y2021.S1903_2023-11-14T204901/metadata.csv'
CSV_FILE_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/ACSST5Y2021.S1903_2023-11-14T204901/data.csv'
CLEANED_DATA_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'

def load_metadata(file_path):
    # Load the metadata from the CSV file into a pandas DataFrame
    metadata = pd.read_csv(file_path)
    # Create a dictionary that maps the 'Column Name' to the 'Label'
    rename_dict = dict(zip(metadata['Column Name'], metadata['Label']))
    return rename_dict

def clean_data(file_path, rename_dict):
    # Load the data from the CSV file into a pandas DataFrame
    data = pd.read_csv(file_path, header=1)
    # Rename the columns based on the metadata
    data.rename(columns=rename_dict, inplace=True)
    # Clean the 'Geographic Area Name' column and rename it to 'Zip Code'
    data.rename(columns={'Geographic Area Name': 'Zip Code'}, inplace=True)
    data['Zip Code'] = data['Zip Code'].str.replace('ZCTA5 ', '')
    # Drop the 'Geography' column and columns that start with 'Annotation' or 'Margin of Error!!'
    data.drop(columns=['Geography'], inplace=True)
    data.drop(data.columns[data.columns.str.startswith(('Annotation', 'Margin of Error!!'))], axis=1, inplace=True)
    # Replace 'Estimate!!' and 'Number!!HOUSEHOLD INCOME BY RACE AND HISPANIC OR LATINO ORIGIN OF HOUSEHOLDER!!' in column names
    data.columns = data.columns.str.replace('Estimate!!', '')
    data.columns = data.columns.str.replace('Number!!HOUSEHOLD INCOME BY RACE AND HISPANIC OR LATINO ORIGIN OF HOUSEHOLDER!!', 'Number of ')
    data.drop(data.columns[2:15], axis=1, inplace=True)
    return data

def main():
    # Load the renaming dictionary from the metadata file
    rename_dict = load_metadata(METADATA_FILE_PATH)
    # Clean the data with the renaming dictionary
    cleaned_data = clean_data(CSV_FILE_PATH, rename_dict)
    # Save the cleaned data to a CSV file, without the index
    cleaned_data.to_csv(CLEANED_DATA_PATH, index=False)

if __name__ == '__main__':
    main()