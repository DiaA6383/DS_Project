import geopandas as gpd
import folium
import pandas as pd

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

    # Convert 'modzcta' to int
    nyc_shapefile['modzcta'] = nyc_shapefile['modzcta'].astype(int)

    # Convert 'Zip Code' to int
    cleaned_data['Zip Code'] = cleaned_data['Zip Code'].astype(int)

    # Now merge
    nyc_data_merged = nyc_shapefile.merge(cleaned_data, left_on='modzcta', right_on='Zip Code')
    # Create map
    m = folium.Map(location=[40.693943, -73.985880], zoom_start=10)

    # Add choropleth layer to map
    folium.Choropleth(
        geo_data=nyc_data_merged,
        name='choropleth',
        data=nyc_data_merged,
        columns=['modzcta', 'Total Households'],
        key_on='feature.properties.modzcta',
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Total Households'
    ).add_to(m)

    # Save to map
    m.save(output_map_path)

if __name__ == '__main__':
    # Define the paths to the cleaned data CSV file, shapefile, and output map HTML filenyc_data_merged = nyc_shapefile.merge(cleaned_data, left_on='zcta', right_on='Zip Code')
    CLEANED_DATA_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'
    SHAPEFILE_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/Modified Zip Code Tabulation Areas (MODZCTA)/geo_export_152003af-efec-4038-9b6f-1963116a24c2.shp'
    OUTPUT_MAP_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/maps/nyc_heatmap.html'

    # Generate the heatmap
    generate_heatmap(CLEANED_DATA_PATH, SHAPEFILE_PATH, OUTPUT_MAP_PATH)
    nyc_shapefile = gpd.read_file(SHAPEFILE_PATH)
    print(nyc_shapefile.columns)