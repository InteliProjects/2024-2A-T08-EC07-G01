# preprocess_data.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def execute(df_resultados, df_merged2):

    
    # Remove rows where 'UNIT' is empty

    print("aqui eh merged", df_merged2['S_GROUP_ID'].unique())
    df_resultados = df_resultados[df_resultados["UNIT"] != '          ']
    
    # Strip whitespace from 'UNIT'
    df_resultados["UNIT"] = df_resultados["UNIT"].str.strip()
    
    # Clean and convert 'VALUE' to numeric
    df_resultados["VALUE"] = df_resultados["VALUE"].str.strip()
    df_resultados["VALUE"] = df_resultados["VALUE"].replace('', pd.NA)
    df_resultados["VALUE"] = df_resultados["VALUE"].str.replace(',', '.', regex=False)
    df_resultados["VALUE"] = pd.to_numeric(df_resultados["VALUE"], errors='coerce')
    
    # Group by 'KNR' and 'UNIT', calculate mean of 'VALUE'
    df_grouped = df_resultados.groupby(['KNR', 'UNIT'])['VALUE'].mean().reset_index()
    
    # Pivot the dataframe
    df_pivot = df_grouped.pivot(index='KNR', columns='UNIT', values='VALUE').reset_index()
    
    # Fill NaN with 0
    df_pivot = df_pivot.fillna(0)
    
    # Convert columns to uppercase
    df_pivot.columns = df_pivot.columns.str.upper()
    
    # Exclude 'KNR' from normalization
    columns_to_exclude = ['KNR']
    # Columns to normalize
    columns_to_normalize = df_pivot.columns.difference(columns_to_exclude)
    
    # Ensure the columns to normalize are numeric
    numeric_columns = df_pivot[columns_to_normalize].select_dtypes(include=[float, int]).columns
    
    # Normalize the columns
    scaler = MinMaxScaler()
    df_pivot[numeric_columns] = scaler.fit_transform(df_pivot[numeric_columns])
    
    # Merge with df_merged2
    df_final = df_pivot.merge(df_merged2, on='KNR', how='left')

    print("aqui eh antes", df_final['S_GROUP_ID'].unique())

    # One Hot Encoding for 'S_GROUP_ID'
    df_final = pd.get_dummies(df_final, columns=['S_GROUP_ID'])
    
    # Drop unnecessary columns
    df_final = df_final.drop(columns=[
        'COR_0Q0Q', 'COR_0QA1', 'COR_2R2R', 'COR_2RA1',
        'COR_5T5T', 'COR_5TA1', 'COR_6K6K', 'COR_6KA1',
        'COR_6UA1', 'COR_A1A1', 'COR_K2A1', 'COR_K2K2',
        'MOTOR_CWL', 'MOTOR_CWS', 'MOTOR_DHS', 'MOTOR_DRP',
        'S_GROUP_ID_-2', 'KNR', 'index', 'UNNAMED: 5'  # Remove this only if not relevant anymore after encoding
    ], errors='ignore')
    
    # Fill NaN values with 0
    df_final = df_final.fillna(0)
    
    return df_final
