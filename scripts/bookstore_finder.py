import pandas as pd
from geopy.geocoders import Nominatim

# Read the CSV file into a DataFrame and remove leading/trailing spaces and tabs
csv_file = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/bookstores.csv'

# Read the CSV file and strip leading/trailing spaces and tabs from each field
with open(csv_file, 'r') as file:
    cleaned_lines = [line.strip() for line in file]

# Create a new cleaned CSV file
cleaned_csv_file = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/cleaned_bookstores.csv'
with open(cleaned_csv_file, 'w') as file:
    file.writelines(cleaned_lines)

# Read the cleaned CSV file into a DataFrame
df = pd.read_csv(cleaned_csv_file)

# Create a geocoder object (Nominatim is a free geocoding service)
geolocator = Nominatim(user_agent="bookstore_locator")

# Define a function to get the zip code from an address
def get_zipcode(address):
    location = geolocator.geocode(address)
    if location and location.raw.get('address', {}).get('postcode'):
        return location.raw['address']['postcode']
    else:
        return None

# Add a "Zip Code" column based on the addresses
df['Zip Code'] = df['Address'].apply(get_zipcode)

# Define the output CSV file path
output_directory = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed'
output_csv_file = f'{output_directory}/bookstores_with_zipcode.csv'

# Save the DataFrame back to a CSV file with the "Zip Code" column
df.to_csv(output_csv_file, index=False)

print("Zip codes added and CSV file saved to:", output_csv_file)
