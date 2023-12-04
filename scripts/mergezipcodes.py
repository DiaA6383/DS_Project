import unittest
import geopandas as gpd
import pandas as pd

def merge_data_with_geocodes(data, gdf):
    """
    Merge the given data DataFrame with geocodes based on the Zip Code.

    Args:
        data (pandas.DataFrame): The main data DataFrame.
        gdf (geopandas.GeoDataFrame): The GeoDataFrame containing latitude and longitude.

    Returns:
        pandas.DataFrame: The merged DataFrame.
    """
    return data.merge(gdf[['ZCTA5CE10', 'latitude', 'longitude']], left_on='Zip Code', right_on='ZCTA5CE10')

# Path to the shapefile containing geographic data
shapefile_path = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/tl_2016_us_zcta510/tl_2016_us_zcta510.shp'

# Read the shapefile into a GeoDataFrame
gdf = gpd.read_file(shapefile_path)

# Convert the geometries to a projected CRS (Coordinate Reference System) before calculating the centroids
gdf_projected = gdf.to_crs(epsg=2163)

# Calculate centroids in the projected CRS
gdf_projected['centroid'] = gdf_projected.geometry.centroid

# Convert centroids back to geographic CRS to obtain latitude and longitude
centroids_geo = gdf_projected['centroid'].to_crs(epsg=4326)
gdf['latitude'] = centroids_geo.y
gdf['longitude'] = centroids_geo.x

# Path to the existing data file
data_path = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'

# Read the existing data into a DataFrame
data = pd.read_csv(data_path)

# Convert Zip Code column to string type for consistency
data['Zip Code'] = data['Zip Code'].astype(str)

# Merge the dataframes on the Zip Code
merged_data = merge_data_with_geocodes(data, gdf)

# Check if 'ZCTA5CE10' column exists and drop it if it does
if 'ZCTA5CE10' in merged_data.columns:
    merged_data = merged_data.drop(columns='ZCTA5CE10')

# Save the merged data to a CSV file
merged_data.to_csv('/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/merged_data.csv', index=False)

# Unit tests
class TestMergeDataWithGeocodes(unittest.TestCase):
    def setUp(self):
        # Set up a sample DataFrame and GeoDataFrame for testing
        self.data = pd.DataFrame({
            'Zip Code': ['90210', '10001', '94123'],
            'Other Data': ['data1', 'data2', 'data3']
        })

        self.gdf = gpd.GeoDataFrame({
            'ZCTA5CE10': ['90210', '10001', '94123'],
            'latitude': [34.103, 40.750, 37.800],
            'longitude': [-118.41, -73.997, -122.44]
        })

    def test_merge_data_with_geocodes(self):
        # Test the merge_data_with_geocodes function
        merged_data = merge_data_with_geocodes(self.data, self.gdf)

        # Check for correct columns in the merged data
        self.assertIn('Zip Code', merged_data.columns)
        self.assertIn('Other Data', merged_data.columns)
        self.assertIn('latitude', merged_data.columns)
        self.assertIn('longitude', merged_data.columns)

        # Check for the correct number of rows in the merged data
        self.assertEqual(len(merged_data), 3)

        # Check for the correct data in the merged data
        self.assertEqual(merged_data.loc[0, 'Zip Code'], '90210')
        self.assertEqual(merged_data.loc[0, 'Other Data'], 'data1')
        self.assertEqual(merged_data.loc[0, 'latitude'], 34.103)
        self.assertEqual(merged_data.loc[0, 'longitude'], -118.41)

if __name__ == '__main__':
    unittest.main()
