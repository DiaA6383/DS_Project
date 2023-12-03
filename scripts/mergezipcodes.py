import unittest
import geopandas as gpd
import pandas as pd

def merge_data_with_geocodes(data, gdf):
    """
    Merge the main data DataFrame with the GeoDataFrame containing latitude and longitude.
    """
    return data.merge(gdf[['ZCTA5CE10', 'latitude', 'longitude']], left_on='Zip Code', right_on='ZCTA5CE10')

# Load the shapefile
shapefile_path = '/path/to/tl_2016_us_zcta510.shp'
gdf = gpd.read_file(shapefile_path)

# Convert the geometries to a projected CRS before calculating the centroids
gdf_projected = gdf.to_crs(epsg=2163)

# Calculate centroids in the projected CRS
gdf_projected['centroid'] = gdf_projected.geometry.centroid

# Convert centroids back to geographic CRS to get latitude and longitude
centroids_geo = gdf_projected['centroid'].to_crs(epsg=4326)
gdf['latitude'] = centroids_geo.y
gdf['longitude'] = centroids_geo.x

# Load your existing data
data_path = '/path/to/cleaned_data.csv'
data = pd.read_csv(data_path)
data['Zip Code'] = data['Zip Code'].astype(str)

# Merge the dataframes on the Zip Code
merged_data = merge_data_with_geocodes(data, gdf)

# Save the merged data
merged_data.to_csv('/path/to/save/merged_data.csv', index=False)

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

        # Check for correct columns
        self.assertIn('Zip Code', merged_data.columns)
        self.assertIn('Other Data', merged_data.columns)
        self.assertIn('latitude', merged_data.columns)
        self.assertIn('longitude', merged_data.columns)

        # Check for correct number of rows
        self.assertEqual(len(merged_data), 3)

        # Check for correct data
        self.assertEqual(merged_data.loc[0, 'Zip Code'], '90210')
        self.assertEqual(merged_data.loc[0, 'Other Data'], 'data1')
        self.assertEqual(merged_data.loc[0, 'latitude'], 34.103)
        self.assertEqual(merged_data.loc[0, 'longitude'], -118.41)

if __name__ == '__main__':
    unittest.main()
