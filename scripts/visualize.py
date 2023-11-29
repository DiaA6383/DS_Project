import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx

SHAPEFILE_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/Modified Zip Code Tabulation Areas (MODZCTA)/geo_export_152003af-efec-4038-9b6f-1963116a24c2.shp'
CLEANED_DATA_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'

def load_shapefile(shapefile_path):
    return gpd.read_file(shapefile_path)

def load_cleaned_data(data_path):
    data = pd.read_csv(data_path)
    print(data.columns)
    return data

def merge_data(gdf, cleaned_data):
    gdf['zcta'] = gdf['zcta'].astype(str)
    cleaned_data['Zip Code'] = cleaned_data['Zip Code'].astype(str)
    return gdf.merge(cleaned_data, left_on='zcta', right_on='Zip Code')

def plot_data(merged):
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    merged.plot(column='Median Income of all Families', ax=ax, legend=True, cmap='coolwarm')
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=merged.crs.to_string())
    ax.set_axis_off()
    plt.title('Heatmap of Median Family Income by Zip Code')
    plt.show()
    
def main():
    gdf = load_shapefile(SHAPEFILE_PATH)
    print(gdf.columns)  # print the columns of the GeoDataFrame
    cleaned_data = load_cleaned_data(CLEANED_DATA_PATH)
    merged = merge_data(gdf, cleaned_data)
    plot_data(merged)
if __name__ == '__main__':
    main()

