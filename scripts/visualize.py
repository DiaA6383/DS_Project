import geopandas as gpd
import folium
import pandas as pd
"""
Visualize Heatmap of NYC Data

This script reads in a cleaned dataset containing New York City information by ZIP code and a shapefile of NYC ZIP code boundaries.
It merges these datasets and uses Folium to generate an interactive heatmap visualization. The resulting map highlights the
distribution of a specified indicator across different ZIP codes in NYC with color gradients to represent different data ranges.

The heatmap is saved as an HTML file that can be opened in a web browser.

Usage:
    Run this script after the data cleaning process has been completed and you have a 'cleaned_data.csv' file. Ensure that
    the shapefile with ZIP code boundaries is correctly formatted and located in the specified path. The script expects the
    following files:
        - Cleaned data CSV: '../data/processed/cleaned_data.csv'
        - NYC ZIP code shapefile: '../data/raw/Modified Zip Code Tabulation Areas (MODZCTA)/geo_export_152003af-efec-4038-9b6f-1963116a24c2.shp'

    The output HTML file will be saved to '../maps/nyc_heatmap.html'.

Requirements:
    - Pandas: For data manipulation.
    - GeoPandas: For handling geospatial data.
    - Folium: For creating the interactive map.

The script contains functions to handle the loading, merging, and visualization steps. It can be modified to adjust for different
data indicators, geographic areas, or visualization libraries as needed.

Author: Alejandro Diaz
"""

def generate_heatmap(cleaned_data_path, shapefile_path, output_map_path):
    """
    Generate a heatmap of NYC data.

    Parameters:
    cleaned_data_path (str): Path to the cleaned data CSV file.
    shapefile_path (str): Path to the NYC ZIP code shapefile.
    output_map_path (str): Path to save the output map HTML file.

    Returns:
    None
    """
    # Load cleaned data
    cleaned_data = pd.read_csv(cleaned_data_path)

    # Load shapefile
    nyc_shapefile = gpd.read_file(shapefile_path)

    # Merge cleaned data with the shapefile
    nyc_data_merged = nyc_shapefile.merge(cleaned_data, left_on='ZIPCODE', right_on='Zip Code')

    # Create map
    m = folium.Map(location=[40.693943, -73.985880], zoom_start=10)

    # Add choropleth layer to map
    folium.Choropleth(
        geo_data=nyc_data_merged,
        name='choropleth',
        data=nyc_data_merged,
        columns=['ZIPCODE', 'Total Households'],
        key_on='feature.properties.ZIPCODE',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total Households'
    ).add_to(m)

    # Save to map
    m.save(output_map_path)

if __name__ == '__main__':
    # Define the paths to the cleaned data CSV file, shapefile, and output map HTML file
    CLEANED_DATA_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'
    SHAPEFILE_PATH = '../data/raw/Modified Zip Code Tabulation Areas (MODZCTA)/geo_export_152003af-efec-4038-9b6f-1963116a24c2.shp'
    OUTPUT_MAP_PATH = '../maps/nyc_heatmap.html'

    # Generate the heatmap
    generate_heatmap(CLEANED_DATA_PATH, SHAPEFILE_PATH, OUTPUT_MAP_PATH)