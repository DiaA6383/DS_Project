import pandas as pd

# Replace 'your_raw_data.csv' with the path to your raw data CSV file
raw_data_path = 'data/raw/ACSST5Y2021.S1903_2023-11-14T204901/ACSST5Y2021.S1903-Data.csv'

# Replace these with the actual column names you want to keep
columns_to_keep = ['ZIP_Code_Column_Name', 'Number_of_Households_Column_Name', 'Median_Income_Column_Name']

def clean_data(file_path, columns):
    # Load the data
    data = pd.read_csv(file_path, usecols=columns)

    # Check for missing values and decide how to handle them
    # For example, you might fill missing values with the median or mode, or drop them entirely
    data = data.dropna()

    # Ensure correct data types, e.g., ZIP Code might be better as a string rather than a numeric type
    data['ZIP_Code_Column_Name'] = data['ZIP_Code_Column_Name'].astype(str)

    # Any additional cleaning steps would go here

    return data

# Use the function to clean the data
cleaned_data = clean_data(raw_data_path, columns_to_keep)

# Replace 'your_cleaned_data.csv' with the path to where you want to save your processed data CSV file
cleaned_data_path = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed'
cleaned_data.to_csv(cleaned_data_path, index=False)
