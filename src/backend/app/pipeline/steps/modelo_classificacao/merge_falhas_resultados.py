# merge_falhas_resultados.py
import pandas as pd

def execute(df_resultados_processed_2, df_falhas_processed_2):
    df_falhas_processed_2['S_GROUP_ID'] = df_falhas_processed_2['S_GROUP_ID'].astype(str)

    merged_df = pd.merge(df_resultados_processed_2, df_falhas_processed_2, on="KNR", how="left")
    merged_df = merged_df.fillna(0)
    return merged_df
