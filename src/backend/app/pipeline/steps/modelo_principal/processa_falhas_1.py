import pandas as pd

def execute(df_falhas):
    '''
    Processes the 'df_falhas' DataFrame by converting 'FALHA' column to uppercase,
    removing duplicates based on 'KNR', and setting 'FALHA' values to 1.

    Parameters:
    df_falhas: pandas DataFrame

    Returns:
    pandas DataFrame: Processed DataFrame.
    '''
    df_falhas["FALHA"] = df_falhas["FALHA"].str.upper()
    df_falha = df_falhas.drop_duplicates(subset=["KNR"])
    df_falha["FALHA"] = 1
    return df_falha

if __name__ == "__main__":
    df_falhas = pd.read_csv("df_falhas.csv")
    df_falhas_processed_1 = execute(df_falhas)
    df_falhas_processed_1.to_csv("df_falhas_trat1.csv", index=False)
