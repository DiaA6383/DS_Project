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
    plt.ylabel('Book Price')
    plt.title('Linear Regression of Book Price vs Median Income')
    plt.legend()
    plt.show()

def main():
    # Define file paths
    current_dir = os.path.dirname(os.path.realpath(__file__))
    CLEANED_DATA_PATH = os.path.join(current_dir, '../data/processed/cleaned_data.csv')

    # Load data
    data = load_data(CLEANED_DATA_PATH)

    # Prepare the data
    X = data[['Median Income of all Families']]
    y = data['Book_Price']

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    mse, r2, y_pred = evaluate_model(model, X_test, y_test)

    # Output results
    print(f"Mean Squared Error: {mse}")
    print(f"R-squared: {r2}")
    print("Coefficient (Slope):", model.coef_[0])
    print("Intercept:", model.intercept_)

    # Plot results
    plot_results(X_test, y_test, y_pred)

    # Interpretation
    if model.coef_[0] > 0:
        print("There is a positive relationship between Median Income and Book Price.")
    else:
        print("There is a negative relationship between Median Income and Book Price.")

    print("For every unit increase in Median Income, the Book Price increases by", model.coef_[0])

if __name__ == '__main__':
    main()
