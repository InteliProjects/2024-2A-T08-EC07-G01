# process_falhas_step1.py
import pandas as pd

def execute(df_falhas):
    df_falhas["FALHA"] = df_falhas["FALHA"].str.upper()
    df_falha = df_falhas.drop_duplicates(subset=["KNR"])
    df_falha["FALHA"] = 1
    return df_falha
