import pandas as pd

def executable(file_path):
    df = pd.read_csv(file_path)
    df= df.dropna() 
    df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')
    return df

# Exemplo de chamada da função
if __name__ == "__main__":
    file_path = 'arquivo_de_entrada.csv'  # Caminho do arquivo de entrada
    df_resultados_trat1 = executable(file_path)
    df_resultados_trat1.to_csv("df_resultados_trat1.csv", index=False)


