import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import os

def load_data(data_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    """
    data = pd.read_csv(data_path)
    return data

def create_proxy_variable(data):
    """
    Create a proxy variable for purchase likelihood based on median income.
    """
    income_threshold = 80000
    data['Purchase_Likelihood'] = (data['Median Income of all Families'] > income_threshold).astype(int)
    return data

def preprocess_data(data):
    """
    Preprocess the data by filling in missing values.
    """
    data['Median Income of all Families'] = data['Median Income of all Families'].fillna(data['Median Income of all Families'].median())
    
    return data

def train_model(X_train, y_train):
    """
    Train a linear regression model.
    """
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the trained linear regression model.
    """
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    return mse, r2, y_pred

def plot_results(X_test, y_test, y_pred):
    """
    Plot the results of the linear regression.
    """
    plt.scatter(X_test, y_test, color='blue', label='Data Points')
    plt.plot(X_test, y_pred, color='red', label='Regression Line')
    plt.xlabel('Median Income of all Families')
    plt.ylabel('Purchase Likelihood')
    plt.title('Linear Regression of Purchase Likelihood vs Median Income')
    plt.legend()
    plt.show()

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    CLEANED_DATA_PATH = os.path.join(current_dir, '../data/processed/cleaned_data.csv')

    data = load_data(CLEANED_DATA_PATH)
    data = create_proxy_variable(data)
    data = preprocess_data(data)

    X = data[['Median Income of all Families']]
    y = data['Purchase_Likelihood']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    mse, r2, y_pred = evaluate_model(model, X_test, y_test)

    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")

    plot_results(X_test, y_test, y_pred)

if __name__ == '__main__':
    main()
