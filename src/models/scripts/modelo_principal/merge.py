import pandas as pd


def merge(df_resultados, df_falhas):
    resultados = pd.read_csv(df_resultados)
    falhas = pd.read_csv(df_falhas)
    merged_df = pd.merge(resultados, falhas, on='KNR', how='left')
    # Adiciona 0 em todos os NaN
    merged_df = merged_df.fillna(0)
    return merged_df
    
# Exemplo de chamada da função
if __name__ == "__main__":
    df_resultados = 'df_resultados_trat2.csv'  # Caminho do arquivo de entrada
    df_falhas = "df_falhas_trat2.csv"
    merged_df= merge(df_resultados, df_falhas)
    merged_df.to_csv("df_merge", index=False)