import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
import os

def load_data(data_path):
    """
    Load the data from the specified file path.

    Args:
        data_path (str): The file path of the data.

    Returns:
        pandas.DataFrame: The loaded data.
    """
    data = pd.read_csv(data_path)
    return data

def preprocess_data(data):
    """
    Preprocess the data by converting the 'Median Income of all Families' column to numeric,
    replacing '250,000+' with '250000', and creating a new column 'Purchase_Likelihood'
    based on the income threshold.

    Args:
        data (pandas.DataFrame): The input data.

    Returns:
        pandas.DataFrame: The preprocessed data.
    """
    data['Median Income of all Families'] = data['Median Income of all Families'].astype(str)
    data['Median Income of all Families'] = data['Median Income of all Families'].replace('250,000+', '250000')
    data['Median Income of all Families'] = pd.to_numeric(data['Median Income of all Families'], errors='coerce')
    income_threshold = 80000
    data['Purchase_Likelihood'] = (data['Median Income of all Families'] > income_threshold).astype(int)
    data.dropna(subset=['Median Income of all Families'], inplace=True)
    return data

def train_model(X_train, y_train):
    """
    Train a logistic regression model using the training data.

    Args:
        X_train (numpy.ndarray): The features of the training data.
        y_train (numpy.ndarray): The labels of the training data.

    Returns:
        sklearn.linear_model.LogisticRegression: The trained logistic regression model.
    """
    model = LogisticRegression()
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, X_test, y_test):
    """
    Evaluate the trained model on the test data and calculate the accuracy, ROC AUC score,
    and predicted probabilities.

    Args:
        model (sklearn.linear_model.LogisticRegression): The trained logistic regression model.
        X_test (numpy.ndarray): The features of the test data.
        y_test (numpy.ndarray): The labels of the test data.

    Returns:
        float: The accuracy of the model.
        float: The ROC AUC score of the model.
        numpy.ndarray: The predicted probabilities of the test data.
    """
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    accuracy = accuracy_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_pred_proba)
    return accuracy, roc_auc, y_pred_proba

def plot_results(X_test, y_test, y_pred_proba):
    """
    Plot the results of the logistic regression model, showing the data points and the
    probability curve.

    Args:
        X_test (numpy.ndarray): The features of the test data.
        y_test (numpy.ndarray): The labels of the test data.
        y_pred_proba (numpy.ndarray): The predicted probabilities of the test data.
    """
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
    """
    The main function that executes the logistic regression pipeline.
    """
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
