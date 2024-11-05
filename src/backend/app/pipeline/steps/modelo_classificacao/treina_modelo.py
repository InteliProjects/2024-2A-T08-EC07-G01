# train_model.py
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import os
import pandas as pd
import joblib

def execute(df_final):
    """
    Trains models based on the provided DataFrame.

    Parameters:
    df_final (pd.DataFrame): The preprocessed training DataFrame.

    Returns:
    dict: Metadata of all trained models (excluding 'type_model').
    """
    models_metadata = {}
    cols = [
        'S_GROUP_ID_1', 'S_GROUP_ID_2', 'S_GROUP_ID_4', 'S_GROUP_ID_5',
        'S_GROUP_ID_133', 'S_GROUP_ID_9830946'
    ]

    # TODO: Adicionar S_GROUP_ID_137 e 140 dps, arrumar a tabela de ersultados pra abranger todos os S_GROUP_ID

    pd.set_option('display.max_columns', None)

    print(list(df_final.columns))
    print(df_final)

    for col in cols:
        print(f"Training model for {col}")

        # Check if the column exists in the DataFrame
        if col not in df_final.columns:
            print(f"[WARNING] Column '{col}' not found in DataFrame. Skipping.")
            continue

        # Separate features and target
        X = df_final.drop(columns=[col, 'KNR'], errors='ignore')
        y = df_final[col]

        # Check if target variable has both classes
        unique_classes = y.unique()
        if len(unique_classes) < 2:
            print(f"[WARNING] Not enough classes in target '{col}'. Skipping training.")
            continue

        # Handle class imbalance using K-Means clustering
        X_majority = X[y == 0]
        X_minority = X[y == 1]
        n_clusters = min(len(X_majority), len(X_minority))
        if n_clusters == 0:
            print(f"[WARNING] Skipping training for {col} due to insufficient data.")
            continue

        # Ensure n_clusters is at least 1
        n_clusters = max(n_clusters, 1)

        kmeans = KMeans(n_clusters=n_clusters, random_state=1)
        kmeans.fit(X_majority)
        X_majority_centroids = kmeans.cluster_centers_

        # Combine centroids with minority class
        X_balanced = np.vstack((X_majority_centroids, X_minority))
        y_balanced = np.hstack((
            np.zeros(len(X_majority_centroids)),
            np.ones(len(X_minority))
        ))

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X_balanced, y_balanced, test_size=0.2, random_state=42, stratify=y_balanced
        )

        # Train the model
        model = XGBClassifier(use_label_encoder=False, eval_metric='auc')
        model.fit(X_train, y_train)

        # Make predictions
        y_pred = model.predict(X_test)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, zero_division=0)
        recall = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        print(f"Results for column {col}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        print(f"F1-Score: {f1:.4f}")

        # Confusion Matrix and Classification Report
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred, zero_division=0))

        model_path = os.path.join(os.getcwd(), 'app', 'pipeline', f'{col}.joblib')
        joblib.dump(model, model_path)

        # Store metadata without 'type_model'
        models_metadata[col] = {
            "model_name": col,
            "metrics": {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }
        }

    print(models_metadata)

    return models_metadata
