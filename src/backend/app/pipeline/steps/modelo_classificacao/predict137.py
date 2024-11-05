# predict_S_GROUP_ID_1.py
import pandas as pd
import joblib
import os

def execute(df_preprocessed_input):
    '''
    Load the model for S_GROUP_ID_1 and make predictions on df_input.

    Parameters:
    df_input: pandas DataFrame

    Returns:
    numpy array: Predictions for S_GROUP_ID_1
    '''
    model_path = os.path.join(os.getcwd(), 'app', 'pipeline', 'S_GROUP_ID_137.joblib')
    model = joblib.load(model_path)

    # Prepare features
    X = df_preprocessed_input.drop(columns=['KNR'], errors='ignore')

    # Make predictions
    y_pred = model.predict(X)

    return y_pred
