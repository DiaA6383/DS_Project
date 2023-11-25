import pandas as pd

def load_and_display_income_data(file_path):
    # Read the data
    df = pd.read_csv(file_path)
    
    # Identify columns of interest
    # Assuming 'GEO_ID' is the column for ZIP codes and 'S1903_C03_0XXE' is the median income column
    # Replace 'S1903_C03_0XXE' with the correct column identifier for median income
    zip_code_column = 'GEO_ID'
    median_income_column = 'S1903_C03_0XXE'  # Replace with the actual column name for median income
    
    # Extract ZIP code and median income columns
    income_data = df[[zip_code_column, median_income_column]]
    
    # Print the first row to verify correct data extraction
    print(income_data.iloc[0])

def main():
    # File path to the median income data by ZIP code
    file_path = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/median_income_by_zip.csv'  # Update with your actual file path
    
    # Load the data and display the first row
    load_and_display_income_data(file_path)

if __name__ == '__main__':
    main()
