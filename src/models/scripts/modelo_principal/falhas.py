import pandas as pd

def executable (file_path):
    df = pd.read_csv(file_path)
    df['FALHA'] = df['FALHA'].str.upper()
    # Remove todas as linhas com KNR repetido
    df = df.drop_duplicates(subset=['KNR'])
    df['FALHA'] = 1

    return df


# Exemplo de chamada da função
if __name__ == "__main__":
    file_path = 'nome_do_arquivo.csv'  # Caminho do arquivo de entrada
    df_falhas_trat1 = executable(file_path)
    df_falhas_trat1.to_csv("df_falhas_trat1", index=False)