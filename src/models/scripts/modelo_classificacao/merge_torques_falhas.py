import pandas as pd
import numpy as np

def merge(df_torques, df_falhas):
    """Realiza o merge dos DataFrames de torques e falhas."""
    df_merged = df_torques.merge(df_falhas, on='KNR', how='left')
    return df_merged