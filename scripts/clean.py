import pandas as pd

# Replace with the path to your CSV file
csv_file_path = '../data/raw/ACSST5Y2021.S1903_2023-11-14T204901/ACSST5Y2021.S1903-Data.csv'

# Replace these with the actual column names you want to keep
columns_to_keep = [
    'Geography',  # This is likely your ZIP code column
    'Geographic Area Name',  # This contains 'ZCTA5 ' followed by the actual ZIP code
    # Add your median income column names here
]

def clean_data(file_path, columns):
    # Load the data with the specified columns only
    data = pd.read_csv(file_path, usecols=columns)

    # Check for missing values and decide how to handle them
    data = data.dropna()

    # Ensure ZIP codes are read as strings to preserve leading zeros
    data['Geography'] = data['Geography'].astype(str)

    # Remove 'ZCTA5 ' from the 'Geographic Area Name' to keep only the ZIP code
    data['Geographic Area Name'] = data['Geographic Area Name'].str.replace('ZCTA5 ', '')

    # Any additional cleaning steps would go here
def clean_data(file_path, columns):
    data = pd.read_csv(file_path, header=1, usecols=columns)
    data = data.dropna()
    data['Geography'] = data['Geography'].astype(str)
    data['Geographic Area Name'] = data['Geographic Area Name'].str.replace('ZCTA5 ', '')
    return data

# Clean the data using the defined function
cleaned_data = clean_data(csv_file_path, columns_to_keep)

# Define the path to where you want to save your processed data CSV file
cleaned_data_path = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'

# Save the cleaned data to a CSV file, without the index
cleaned_data.to_csv(cleaned_data_path, index=False)
