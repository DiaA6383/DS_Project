import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import contextily as ctx

SHAPEFILE_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/raw/Modified Zip Code Tabulation Areas (MODZCTA)/geo_export_152003af-efec-4038-9b6f-1963116a24c2.shp'
CLEANED_DATA_PATH = '/Users/alejandrodiaz/Documents/GitHub/DS_Project/data/processed/cleaned_data.csv'

def load_shapefile(shapefile_path):
    """
    Load a shapefile using geopandas.

    Args:
        shapefile_path (str): The path to the shapefile.

    Returns:
        geopandas.GeoDataFrame: The loaded shapefile as a GeoDataFrame.
    """
    return gpd.read_file(shapefile_path)

def load_cleaned_data(data_path):
    """
    Load cleaned data from a CSV file.

    Args:
        data_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: The loaded cleaned data as a DataFrame.
    """
    data = pd.read_csv(data_path)
    print(data.columns)
    return data

def merge_data(gdf, cleaned_data):
    """
    Merge a GeoDataFrame with cleaned data.

    Args:
        gdf (geopandas.GeoDataFrame): The GeoDataFrame to merge.
        cleaned_data (pandas.DataFrame): The cleaned data DataFrame.

    Returns:
        pandas.DataFrame: The merged DataFrame.
    """
    gdf['zcta'] = gdf['zcta'].astype(str)
    cleaned_data['Zip Code'] = cleaned_data['Zip Code'].astype(str)
    merged = gdf.merge(cleaned_data, left_on='zcta', right_on='Zip Code')
    merged['Median Income of all Families'] = pd.to_numeric(merged['Median Income of all Families'], errors='coerce')
    merged['Median Income of all Families'].fillna(merged['Median Income of all Families'].median(), inplace=True)
    merged['Income Level'] = pd.cut(merged['Median Income of all Families'], bins=4, labels=["Low", "Medium", "High", "Very high"])
    return merged

def plot_data(merged):
    """
    Plot the merged data as a heatmap.

    Args:
        merged (pandas.DataFrame): The merged DataFrame.
    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    merged.plot(column='Income Level', ax=ax, legend=True, cmap='Reds', categorical=True)
    leg = ax.get_legend()
    leg.set_title('Income Levels')
    ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=merged.crs.to_string())
    ax.set_axis_off()
    plt.title('Heatmap of Median Family Income by Zip Code')
    plt.show()
    
def main():
    """
    Main function to execute the visualization process.
    """
    gdf = load_shapefile(SHAPEFILE_PATH)
    print(gdf.columns)  # print the columns of the GeoDataFrame
    cleaned_data = load_cleaned_data(CLEANED_DATA_PATH)
    merged = merge_data(gdf, cleaned_data)
    plot_data(merged)

if __name__ == '__main__':
    main()

