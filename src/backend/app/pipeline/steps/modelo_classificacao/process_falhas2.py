# process_falhas_step2.py
import pandas as pd

def execute(df_falhas_processed_1):
    colunas = ["MODELO", "COR", "MOTOR", "ESTACAO", "USUARIO", "HALLE", "DATA"]
    df_falha = df_falhas_processed_1.drop(columns=colunas, axis=1)
    return df_falha
