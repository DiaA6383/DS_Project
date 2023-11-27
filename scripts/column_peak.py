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


def print_column_names(file_path):
    """
    print column names from cleaned data
    """
    try:
        cleaned_data = pd.read_csv(file_path)
        print(cleaned_data.columns.tolist())
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except pd.errors.EmptyDataError:
        print(f"No data in file: {file_path}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def main():
    """
    This is the main function that calls the print_second_column_from_csv function.
    """
    cleaned_file_path = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'
    print_column_names(cleaned_file_path)


if __name__ == '__main__':
    main()