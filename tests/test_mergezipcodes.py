import unittest
import pandas as pd
import geopandas as gpd
from ..scripts.mergezipcodes import merge_data_with_geocodes

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