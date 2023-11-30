import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
import os

def load_data(data_path):
    """
    Load data from a CSV file into a pandas DataFrame.
    """
    data = pd.read_csv(data_path)
    return data

def preprocess_data(data):
    """
    Preprocess the data by handling missing values and creating a binary outcome.
    """
    # Convert the column to string to ensure the .str methods work
    data['Median Income of all Families'] = data['Median Income of all Families'].astype(str)
    
    # Handle the special case where income is represented as '250,000+'
    data['Median Income of all Families'] = data['Median Income of all Families'].replace('250,000+', '250000')
    
    # Convert the column to numeric, coercing errors to NaN
    data['Median Income of all Families'] = pd.to_numeric(data['Median Income of all Families'], errors='coerce')

    # Assume an arbitrary income threshold to simulate purchase likelihood
    income_threshold = 80000  # Adjust this threshold based on your understanding of the data
    data['Purchase_Likelihood'] = (data['Median Income of all Families'] > income_threshold).astype(int)

    # Handle missing values by dropping them
    data.dropna(subset=['Median Income of all Families'], inplace=True)

    return data

def train_model(X_train, y_train):
    """
    Train a logistic regression model.
    """
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the trained logistic regression model.
    """
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1] # Get the probability of the positive class
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba) # AUC score is a good performance metric for binary classifiers
    return accuracy, roc_auc, y_pred_proba

def plot_results(X_test, y_test, y_pred_proba):
    """
    Plot the results of the logistic regression.
    """
    # Sort the values to ensure a continuous line plot for probabilities
    sorted_indices = X_test.argsort(axis=0).flatten()
    X_test_sorted = X_test[sorted_indices]
    y_pred_proba_sorted = y_pred_proba[sorted_indices]

    plt.scatter(X_test, y_test, color='blue', label='Data Points')
    plt.plot(X_test_sorted, y_pred_proba_sorted, color='red', label='Probability Curve')
    plt.xlabel('Median Income of all Families')
    plt.ylabel('Probability of Purchase')
    plt.title('Logistic Regression of Purchase Probability vs Median Income')
    plt.legend()
    plt.show()

def main():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    CLEANED_DATA_PATH = os.path.join(current_dir, '../data/processed/cleaned_data.csv')

    data = load_data(CLEANED_DATA_PATH)
    data = preprocess_data(data)

    X = data[['Median Income of all Families']].values.reshape(-1, 1)
    y = data['Purchase_Likelihood']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = train_model(X_train, y_train)
    accuracy, roc_auc, y_pred_proba = evaluate_model(model, X_test, y_test)

    print(f"Accuracy: {accuracy}")
    print(f"ROC AUC Score: {roc_auc}")

    plot_results(X_test, y_test, y_pred_proba)

if __name__ == '__main__':
    main()
