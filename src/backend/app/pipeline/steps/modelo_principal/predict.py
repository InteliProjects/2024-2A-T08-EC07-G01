import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
import os

def drop_colunas(df):
    '''
    Function to drop unused columns from the DataFrame.

    Parameters:
    df: pandas DataFrame
    '''
    colunas = ["UNIT", "VALUE_ID", "VALUE"]
    df.drop(columns=colunas, axis=1, inplace=True)

def agregar_por_id(df, id_value):
    '''
    Function to aggregate the data by ID.

    Parameters:
    df: pandas DataFrame
    id_value: int

    Returns:
    DataFrame
    '''
    subset = df[df["ID"] == id_value]
    if subset.empty:
        # Create a DataFrame with zeros
        columns = [
            f"ID{id_value}NAME",
            f"ID{id_value}SOK",
            f"ID{id_value}SNOK",
            f"ID{id_value}DATA",
        ]
        data = {col: [0] for col in columns}
        data["KNR"] = df["KNR"].iloc[0]
        df_empty = pd.DataFrame(data)
        return df_empty.set_index("KNR")
    else:
        agg_df = (
            subset.groupby("KNR")
            .agg(
                NAME=("NAME", "count"),
                SOK=("STATUS", lambda x: (x == 10).sum()),
                SNOK=("STATUS", lambda x: (x == 13).sum()),
                DATA=("DATA", lambda x: (x.max() - x.min()).total_seconds() / (3600 * 24) if len(x) > 1 else 0),
            )
            .rename(
                columns={
                    "NAME": f"ID{id_value}NAME",
                    "SOK": f"ID{id_value}SOK",
                    "SNOK": f"ID{id_value}SNOK",
                    "DATA": f"ID{id_value}DATA",
                }
            )
        )
        return agg_df

def execute(df_input):
    '''
    Receives a DataFrame 'df_input' and returns the prediction.

    Parameters:
    df_input: pandas DataFrame

    Returns:
    int: Prediction (0 or 1)
    '''
    # Process through 'df_resultados_processed_1'
    df_processed_1 = df_input.dropna()
    df_processed_1["DATA"] = pd.to_datetime(df_processed_1["DATA"], errors="coerce")

    # Process through 'df_resultados_processed_2'
    df = df_processed_1.copy()
    drop_colunas(df)

    id1 = agregar_por_id(df, 1)
    id2 = agregar_por_id(df, 2)
    id718 = agregar_por_id(df, 718)

    # Combining results into a single DataFrame
    df_combined = (
        id1.join(id2, on="KNR", how="outer")
        .join(id718, on="KNR", how="outer")
        .reset_index()
    )

    # Ensure all necessary columns are present and fill missing values
    required_columns = [
        "ID1NAME", "ID1SOK", "ID1SNOK", "ID1DATA",
        "ID2NAME", "ID2SOK", "ID2SNOK", "ID2DATA",
        "ID718NAME", "ID718SOK", "ID718SNOK", "ID718DATA"
    ]
    for col in required_columns:
        if col not in df_combined.columns:
            df_combined[col] = 0

    df_combined = df_combined.fillna(0)

    # Prepare input features
    X = df_combined[required_columns]
    X = np.array(X)

    # Reshape to (n_samples, n_features, 1)
    X = X.reshape((X.shape[0], X.shape[1], 1))

    # Load the model
    model_path = os.path.join(os.getcwd(), 'app', 'pipeline', 'model.h5')
    model = load_model(model_path)

    # Make prediction
    y_pred = model.predict(X)

    # Convert prediction to 0 or 1
    y_pred = (y_pred > 0.5).astype(int).flatten()

    # Return the prediction
    return int(y_pred[0])
