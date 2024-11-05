import pandas as pd

def execute(df_resultados_processed_2, df_falhas_processed_2):
    '''
    Script to merge the results and failures DataFrames.

    Parameters:
    df_resultados_processed_2: pandas DataFrame
    df_falhas_processed_2: pandas DataFrame

    Returns:
    pandas DataFrame: The merged DataFrame with NaN values filled with 0.
    '''
    merged_df = pd.merge(df_resultados_processed_2, df_falhas_processed_2, on="KNR", how="left")
    merged_df = merged_df.fillna(0)
    return merged_df