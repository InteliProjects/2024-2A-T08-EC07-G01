from sklearn.preprocessing import MinMaxScaler


def drop_colunas(df):
    '''
    Function to drop unused columns from the DF.

    Parameters:
    df: pandas DataFrame
    '''
    colunas = ["UNIT", "VALUE_ID", "VALUE"]
    df = df.drop(columns=colunas, axis=1)


def agregar_por_id(df, id_value):
    '''
    Function to aggregate the data by ID.

    Parameters:
    df: pandas DataFrame
    id_value: int
    '''
    subset = df[df["ID"] == id_value]
    return (
        subset.groupby("KNR")
        .agg(
            NAME=("NAME", "count"),  # Conta total de NAME
            SOK=("STATUS", lambda x: (x == 10).sum()),
            SNOK=("STATUS", lambda x: (x == 13).sum()),
            DATA=("DATA", lambda x: (x.max() - x.min()).total_seconds() / (3600 * 24)),
        )
        .rename(
            columns={
                "NAME": f"ID{id_value}NAME",
                "SOK": f"ID{id_value}SOK",
                "SNOK": f"ID{id_value}SNOK",
                "DATA": f"ID{id_value}DATA",
            }
        )
    )


def normalizacao(df):
    '''
    Function to normalize the selected columns

    Parameters:
    df: pandas DataFrame
    '''
    # Selecionando apenas as colunas específicas para normalização
    colunas_normalizacao = [
        "ID1NAME",
        "ID1SOK",
        "ID1SNOK",
        "ID1DATA",
        "ID2NAME",
        "ID2SOK",
        "ID2SNOK",
        "ID2DATA",
        "ID718NAME",
        "ID718SOK",
        "ID718SNOK",
        "ID718DATA",
    ]

    # Inicializando o MinMaxScaler
    scaler = MinMaxScaler()

    # Aplicando a normalização
    df[colunas_normalizacao] = scaler.fit_transform(df[colunas_normalizacao])
    return df


def execute(df_resultados_processed_1):
    '''
    Script to preprocess the 'df_resultados_processed_1' DataFrame.

    Parameters:
    df_resultados_processed_1: pandas DataFrame

    Returns:
    pandas DataFrame: Processed DataFrame.
    '''
    df = df_resultados_processed_1.copy()
    drop_colunas(df)

    id1 = agregar_por_id(df, 1)
    id2 = agregar_por_id(df, 2)
    id718 = agregar_por_id(df, 718)

    # Combining results into a single DataFrame
    df_combined = (
        id1.join(id2, on="KNR", how="outer")
        .join(id718, on="KNR", how="outer")
        .reset_index()
    )

    # Reordering columns to desired format
    df_combined = df_combined[
        [
            "KNR",
            "ID1NAME",
            "ID1SOK",
            "ID1SNOK",
            "ID1DATA",
            "ID2NAME",
            "ID2SOK",
            "ID2SNOK",
            "ID2DATA",
            "ID718NAME",
            "ID718SOK",
            "ID718SNOK",
            "ID718DATA",
        ]
    ]

    df_combined = normalizacao(df_combined)

    df_combined = df_combined.fillna(0)

    return df_combined

# Exemplo de chamada da função
if __name__ == "__main__":
    df = "df_resultados_trat1.csv"  # Caminho do arquivo de entrada
    df_resultados_trat2 = execute(df)
    df_resultados_trat2.to_csv("df_resultado_trat2", index=False)
