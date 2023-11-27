import pandas as pd

# Paths to your CSV files
METADATA_FILE_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/ACSST5Y2021.S1903_2023-11-14T204901/metadata.csv'
CSV_FILE_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/ACSST5Y2021.S1903_2023-11-14T204901/data.csv'

# Define the path to where you want to save your processed data CSV file
CLEANED_DATA_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'

def clean_column_names(column_names):
    replacements = {
        "Estimate!!": "",
        "Margin of Error!!": "MOE_",
        "Annotation of Estimate!!": "Note_",
        "Annotation of Margin of Error!!": "Note_MOE_",
        "Number!!": "",
        "Percent Distribution!!": "PctDist_",
        # Add more replacements as needed
    }

    clean_names = []
    for name in column_names:
        for to_replace, replacement in replacements.items():
            name = name.replace(to_replace, replacement)
        name = name.replace('!!', '_')
        clean_names.append(name)

    return clean_names

def load_metadata(file_path):
    metadata = pd.read_csv(file_path)
    rename_dict = dict(zip(metadata['Column Name'], metadata['Label']))
    return rename_dict

def clean_data(file_path, rename_dict):
    """
    This function cleans the data from the CSV file.
    """
    data = pd.read_csv(file_path, header=1)
    data = data.rename(columns=rename_dict)  # Rename columns based on metadata
    data['Geographic Area Name'] = data['Geographic Area Name'].str.replace('ZCTA5 ', '')
    data = data.rename(columns={'Geographic Area Name': 'Zip Code'})
    #drop Geography column
    data = data.drop(columns=['Geography'])
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