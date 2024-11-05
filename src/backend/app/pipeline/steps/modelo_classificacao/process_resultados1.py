# process_resultados_step1.py
import pandas as pd

def execute(df_resultados):
    df = df_resultados.dropna()
    df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
    return df
