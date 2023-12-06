"""
Name: Alejandro Diaz
Email: alejandro.diaz60@myhunter.cuny.edu
Resources: OpenDataNYC
"""
#!MOST OF THIS IS JUST FOR AUTOMATIC GRADING PURPOSES!
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import plotly.graph_objs as go
from plotly.offline import iplot
from scipy.integrate import odeint
import numpy as np

# Define data paths
CLEANED_DATA_PATH = 'data/processed/cleaned_data.csv'
SHAPERAW_DATA_PATH = (
    'data/raw/Modified Zip Code Tabulation Areas (MODZCTA)/'
    'geo_export_152003af-efec-4038-9b6f-1963116a24c2.shp'
)
RAW_DATA_PATH = 'data/raw/ACSST5Y2021.S1903_2023-11-14T204901/data.csv'
META_DATA_PATH = 'data/raw/ACSST5Y2021.S1903_2023-11-14T204901/metadata.csv'


def load_and_preprocess_data(data_path):
    """
    Load and preprocess the data.

    Parameters:
    data_path (str): Path to the data file.

    Returns:
    DataFrame: Preprocessed data.
    """
    df = pd.read_csv(data_path)
    df['Median Income of all Families'] = pd.to_numeric(
        df['Median Income of all Families'], errors='coerce'
    )
    imputer = SimpleImputer(strategy='median')
    df['Median Income of all Families'] = imputer.fit_transform(
        df[['Median Income of all Families']]
    )
    df.dropna(subset=['longitude', 'latitude', 'Median Income of all Families'],
              inplace=True)
    df['Scaled_Income'] = df['Median Income of all Families'] / 1000
    return df


def perform_clustering(df):
    """
    Perform clustering on the dataframe if 'Cluster' column does not exist.

    Parameters:
    df (DataFrame): Data to cluster.

    Returns:
    DataFrame: Data with added 'Cluster' column.
    """
    if 'Cluster' not in df.columns:
        features = df[['longitude', 'latitude', 'Median Income of all Families']]
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        kmeans = KMeans(n_clusters=4, random_state=42)
        df['Cluster'] = kmeans.fit_predict(features_scaled)
    return df


def create_location_plot(df):
    """
    Create a location-based plot.

    Parameters:
    df (DataFrame): Data to plot.

    Returns:
    None
    """
    scaling_factor = df['Median Income of all Families'].max() / 100
    df['Scaled_Income'] = df['Median Income of all Families'] / scaling_factor
    data = [{
        'x': df["longitude"],
        'y': df["latitude"],
        'text': df.apply(
            lambda row: f'ZIP: {row["Zip Code"]}<br>Income: ${row["Median Income of all Families"]}',
            axis=1
        ),
        'mode': 'markers',
        'marker': {
            'color': df["Cluster"],
            'size': df['Scaled_Income'],
            'opacity': 0.5,
            'showscale': True,
            'colorscale': 'Portland'
        }
    }]
    layout = go.Layout(
        title='New York ZIP Code Clusters (Median Income of all Families)',
        xaxis={'title': 'Longitude', 'range': [-74.3, -73.8]},
        yaxis={'title': 'Latitude', 'range': [40.5, 40.9]},
        hovermode='closest'
    )
    fig = go.Figure(data=data, layout=layout)
    iplot(fig)

def run_sir_for_cluster(cluster_id, initial_infected, beta, gamma, steps, data):
    """
    Run the SIR model for a specific cluster.

    Parameters:
    cluster_id (int): The ID of the cluster to run the model for.
    initial_infected (int): The initial number of infected individuals.
    beta (float): The contact rate.
    gamma (float): The recovery rate.
    steps (int): The number of simulation steps.
    data (DataFrame): The data containing the cluster information.

    Returns:
    None
    """
    # Filter data for the current cluster
    cluster_data = data[data['Cluster'] == cluster_id]

    # Calculate the total number of households for the current cluster
    total_households = cluster_data['Number of Households'].sum()

    # Create an SIRDiagram instance for the current cluster
    sir_model = SIRDiagram(
        n=total_households,
        i=initial_infected,
        r=0,
        beta=beta,
        gamma=gamma,
        steps=steps
    )

    # Create a subplot for the current cluster
    fig, ax = plt.subplots()
    sir_model.plot(ax)

    # Set plot title and labels specific to the current cluster
    ax.set_title(f"SIR Model: Cluster {cluster_id}")
    ax.set_xlabel("Time /days")
    ax.set_ylabel("Number")
    ax.legend()
    plt.show()

class SIRDiagram:
    """
    Class representing the SIR (Susceptible, Infected, Recovered) model.
    """

    def __init__(self, total_population, initial_infected, initial_recovered,
                 contact_rate, recovery_rate, simulation_steps):
        """
        Initialize the SIRDiagram instance.

        Parameters:
        total_population (int): Total population.
        initial_infected (int): Initial number of infected individuals.
        initial_recovered (int): Initial number of recovered individuals.
        contact_rate (float): Contact rate.
        recovery_rate (float): Recovery rate.
        simulation_steps (int): Number of simulation steps.
        """
        self.total_population = total_population
        self.initial_infected = initial_infected
        self.initial_recovered = initial_recovered
        self.contact_rate = contact_rate
        self.recovery_rate = recovery_rate
        self.simulation_steps = simulation_steps

    def susceptible(self):
        """
        Calculate the number of susceptible individuals.

        Returns:
        int: Number of susceptible individuals.
        """
        return self.total_population - self.initial_infected - self.initial_recovered

    def plot(self, ax):
        """
        Plot the SIR diagram.

        Parameters:
        ax (matplotlib.axes.Axes): The axes to plot on.
        """
        t = np.linspace(0, self.simulation_steps, self.simulation_steps)
        y0 = self.susceptible(), self.initial_infected, self.initial_recovered
        ret = odeint(deriv, y0, t, args=(self.total_population, self.contact_rate, self.recovery_rate))
        S, I, R = ret.T

        ax.plot(t, S, "b", alpha=0.5, lw=2, label="Potential Customer")
        ax.plot(t, I, "r", alpha=0.5, lw=2, label="Informed")
        ax.plot(t, R, "g", alpha=0.5, lw=2, label="Decided Not to Buy")


def deriv(y, t, total_population, contact_rate, recovery_rate):
    """
    Calculate the derivatives of S, I, R in SIR model.

    Parameters:
    y (tuple): Tuple containing S, I, R values.
    t (int): Time step.
    total_population (int): Total population.
    contact_rate (float): Contact rate.
    recovery_rate (float): Recovery rate.

    Returns:
    tuple: Derivatives of S, I, R.
    """
    S, I, R = y
    dSdt = -contact_rate * S * I / total_population
    dIdt = contact_rate * S * I / total_population - recovery_rate * I
    dRdt = recovery_rate * I
    return dSdt, dIdt, dRdt
# Load and preprocess the data
data = load_and_preprocess_data(CLEANED_DATA_PATH)

# Perform clustering
data = perform_clustering(data)

# Create and display the interactive location-based plot
create_location_plot(data)

# Load the shapefile data
gdf = gpd.read_file(SHAPERAW_DATA_PATH)

# Merge the shapefile data with the cleaned data
gdf['zcta'] = gdf['zcta'].astype(str)
data['Zip Code'] = data['Zip Code'].astype(str)
merged = gdf.merge(data, left_on='zcta', right_on='Zip Code')

# Handle missing values in the merged data
merged['Median Income of all Families'] = pd.to_numeric(
    merged['Median Income of all Families'], errors='coerce'
)
merged['Median Income of all Families'].fillna(
    merged['Median Income of all Families'].median(), inplace=True
)

# Create income level categories
merged['Income Level'] = pd.cut(
    merged['Median Income of all Families'], bins=4, 
    labels=["Low", "Medium", "High", "Very high"]
)

# Plot the merged data
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
merged.plot(column='Income Level', ax=ax, legend=True, cmap='Reds', categorical=True)
leg = ax.get_legend()
leg.set_title('Income Levels')
ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik, crs=merged.crs.to_string())
ax.set_axis_off()
plt.title('Heatmap of Median Family Income by Zip Code')
plt.show()

# Define SIR model parameters
initial_infected = 10
beta = 0.3
gamma = 0.1
steps = 200

# Run SIR model for each cluster
for cluster_id in range(4):
    run_sir_for_cluster(cluster_id, initial_infected, beta, gamma, steps, data)