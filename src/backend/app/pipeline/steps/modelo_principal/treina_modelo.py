from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score
import os
import pandas as pd


def preparacao_dados(df):
    # Separando as features (X) e o target (y)
    X = df.drop(columns=["FALHA", "KNR"], errors='ignore')
    y = df["FALHA"]

    # Convert all feature columns to numeric, coercing errors to NaN
    X = X.apply(pd.to_numeric, errors='coerce')

    # Handle missing values by imputing or dropping
    # Here, we'll fill NaNs with 0. Adjust as needed
    X = X.fillna(0)
    y = y.fillna(0)  # Ensure target has no NaNs

    # Ensure target is binary (0 and 1)
    y = y.apply(lambda x: 1 if x > 0 else 0)

    # Separando em dados de treino e teste
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # Converte X_train e X_test para arrays NumPy com dtype float32
    X_train = np.array(X_train).astype(np.float32)
    X_test = np.array(X_test).astype(np.float32)

    # Converte y_train e y_test para arrays NumPy com dtype float32
    y_train = np.array(y_train).astype(np.float32)
    y_test = np.array(y_test).astype(np.float32)

    # Reestrutura X_train e X_test para ter 3 dimensões.
    # A nova forma do array será (n_samples, n_features, 1)
    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    return X_train, X_test, y_train, y_test


def execute(df_merged):
    '''
    Script to build the GRU model for classification and train it.

    Parameters:
    df_merged: pandas DataFrame

    Returns:
    Sequential: Trained Keras model.
    '''
    print(df_merged)
    X_train, X_test, y_train, y_test = preparacao_dados(df_merged)
    # Building the GRU model
    model = Sequential()
    model.add(
        GRU(
            50,
            activation="relu",
            return_sequences=True,
            input_shape=(X_train.shape[1], 1),
        )
    )
    model.add(GRU(50, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))

    model.compile(optimizer="adam", loss="binary_crossentropy")

    # Training the model
    model.fit(
        X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test)
    )

    y_pred = model.predict(X_test)

    y_pred = (y_pred > 0.5).astype(int).flatten()

    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)

    model_path = os.path.join(os.getcwd(), 'app', 'pipeline', 'model.h5')

    model.save(model_path)

    return {
        "model_name": "GRUOII",
        "type_model": "type0",
        "metrics": {
            "accuracy": float(accuracy),  
            "recall": float(recall),     
            "f1_score": float(f1),
            "precision": float(precision),           
        }
    }