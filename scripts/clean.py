import pandas as pd

# Replace with the path to your CSV file
CSV_FILE_PATH = '../data/raw/ACSST5Y2021.S1903_2023-11-14T204901/ACSST5Y2021.S1903-Data.csv'

# Replace these with the actual column names you want to keep
COLUMNS_TO_KEEP = [
    'Geography',  # This is likely your ZIP code column
    'Geographic Area Name',  # This contains 'ZCTA5 ' followed by the actual ZIP code
    # Add your median income column names here
]

def clean_data(file_path, columns):
    """
    This function cleans the data from the CSV file.
    """
    data = pd.read_csv(file_path, header=1, usecols=columns)
    data = data.dropna()
    data['Geography'] = data['Geography'].astype(str)
    data['Geographic Area Name'] = data['Geographic Area Name'].str.replace('ZCTA5 ', '')
    return data

# Clean the data using the defined function
cleaned_data = clean_data(CSV_FILE_PATH, COLUMNS_TO_KEEP)

# Define the path to where you want to save your processed data CSV file
CLEANED_DATA_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'

# Save the cleaned data to a CSV file, without the index
cleaned_data.to_csv(CLEANED_DATA_PATH, index=False)