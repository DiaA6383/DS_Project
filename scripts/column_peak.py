"""
This script reads a CSV file and prints the second column.
"""

import pandas as pd

def print_second_column_from_csv(file_path):
    """
    This function reads a CSV file and prints the second column.
    """
    try:
        metadata = pd.read_csv(file_path)
        second_column = metadata.iloc[:, 1]
        print(second_column.tolist())
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        print(f"No data in file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main(file_path):
    """
    This is the main function that calls the print_second_column_from_csv function.
    """
    print_second_column_from_csv(file_path)

if __name__ == '__main__':
    META_FILE = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/ACSST5Y2021.S1903_2023-11-14T204901/ACSST5Y2021.S1903-Column-Metadata.csv'
    main(META_FILE)