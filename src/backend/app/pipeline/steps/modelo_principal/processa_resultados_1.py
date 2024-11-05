import pandas as pd


def execute(df_resultados):
    '''
    Processes the 'df_resultados' DataFrame by dropping NaN values
    and converting 'DATA' column to datetime.

    Parameters:
    df_resultados: pandas DataFrame

    Returns:
    pandas DataFrame: Processed DataFrame.
    '''
    df = df_resultados.dropna()
    df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
    return df


# Exemplo de chamada da função
if __name__ == "__main__":
    file_path = "arquivo_de_entrada.csv"  # Caminho do arquivo de entrada
    df_resultados_trat1 = execute(file_path)
    df_resultados_trat1.to_csv("df_resultados_trat1.csv", index=False)
