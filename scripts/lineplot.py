import os
import pandas as pd
import matplotlib.pyplot as plt

# Get the current directory
current_dir = os.path.dirname(os.path.realpath(__file__))

# Define the paths to the cleaned data CSV file
CLEANED_DATA_PATH = os.path.join(current_dir, '../data/processed/cleaned_data.csv')

def open_data(file_path):
    """
    Open data from a CSV file into a pandas DataFrame.
    """
    data = pd.read_csv(file_path)
    return data

def main():
    data = open_data(CLEANED_DATA_PATH)

    # Bar Plot: Number of Families with Children per Zip Code
    data.plot.bar(x='Zip Code', y='Number of Families with Children', title='Families with Children per Zip Code')
    plt.show()

    # Bar Plot: Median Income of all Families per Zip Code
    data.plot.bar(x='Zip Code', y='Median Income of all Families', title='Median Family Income per Zip Code')
    plt.show()

    # Scatter Plot: Number of Families with Children vs Median Income
    plt.scatter(data['Median Income of all Families'], data['Number of Families with Children'])
    plt.xlabel('Median Family Income')
    plt.ylabel('Number of Families with Children')
    plt.title('Families with Children vs Median Family Income')
    plt.show()

if __name__ == '__main__':
    main()
