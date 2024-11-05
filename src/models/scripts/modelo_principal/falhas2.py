import pandas as pd

def executable(df):
    colunas = ['MODELO', 'COR', 'MOTOR', 'ESTACAO', 'USUARIO', 'HALLE', 'DATA']
    df = df.drop(columns=colunas, axis=1)
    return df


# Exemplo de chamada da função
if __name__ == "__main__":
    df = 'df_falhas_trat1.csv'  # Caminho do arquivo de entrada
    df_falhas_trat2 = executable(df)
    df_falhas_trat2.to_csv("df_falhas_trat2", index=False)