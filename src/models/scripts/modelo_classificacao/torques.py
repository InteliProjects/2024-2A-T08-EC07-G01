import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def preprocess_torque(df):
    """Realiza o pré-processamento na coluna VALUE do DataFrame."""
    df["VALUE"] = df["VALUE"].str.strip()  # Remove espaços em branco
    df["VALUE"] = df["VALUE"].replace('', pd.NA)  # Substitui strings vazias por NaN
    df["VALUE"] = df["VALUE"].str.replace(',', '.', regex=False)  # Substitui vírgulas por pontos
    df["VALUE"] = pd.to_numeric(df["VALUE"], errors='coerce')  # Converte para float e trata erros como NaN
    return df.dropna(subset=["VALUE"])  # Remove linhas com NaN em VALUE

def aggregate_by_knr_unit(df):
    """Agrupa os dados por KNR e UNIT, calculando a média dos valores."""
    df_grouped = df.groupby(['KNR', 'UNIT'])['VALUE'].mean().reset_index()
    return df_grouped.pivot(index='KNR', columns='UNIT', values='VALUE').reset_index()

def normalize_columns(df, exclude_columns):
    """Normaliza as colunas numéricas do DataFrame, excluindo as especificadas."""
    # Atualmente, as colunas a serem excluídas (que serão passadas como parâmetro exclude_columns) são KNR e UNIT, pois não serão usadas para treinamento
    columns_to_normalize = df.columns.difference(exclude_columns)
    numeric_columns = df[columns_to_normalize].select_dtypes(include=[float, int]).columns
    scaler = MinMaxScaler()
    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])
    return df

def executable(df):
    """Pipeline de pré-processamento completo dos dados."""
    # Remover colunas indesejadas e espaços
    df = df[df["UNIT"] != '          ']  # Remove onde UNIT tem espaços
    df["UNIT"] = df["UNIT"].str.strip()  # Remove espaços em UNIT
    df = preprocess_torque(df)  # Preprocessa a coluna VALUE

    # Agrupar e pivotar os dados
    df_pivot = aggregate_by_knr_unit(df)
    
    # Padronizar os nomes das colunas para maiúsculas
    df_pivot.columns = df_pivot.columns.str.upper()

    # Normalizar colunas numéricas, excluindo 'KNR' e 'UNIT'
    df_pivot = normalize_columns(df_pivot, exclude_columns=['KNR', 'UNIT'])

    # Exemplo de como pode ser feito um merge, caso precise
    # df_resultados_final = df_merged.merge(df_pivot, on='KNR', how='left')

    return df_pivot

if __name__ == '__main__':
    file_path = 'resultados.csv'  # Caminho do arquivo de entrada
    df_torques = preprocess_data(file_path)
    df_torques.to_csv("df_torques", index=False)
    

