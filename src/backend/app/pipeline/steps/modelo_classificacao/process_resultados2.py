# process_resultados_step2.py
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def drop_colunas(df):
    colunas = ["UNIT", "VALUE_ID", "VALUE"]
    df.drop(columns=colunas, axis=1, inplace=True, errors='ignore')

def agregar_por_id(df, id_value):
    subset = df[df["ID"] == id_value]
    if subset.empty:
        columns = {
            f"ID{id_value}NAME": [0],
            f"ID{id_value}SOK": [0],
            f"ID{id_value}SNOK": [0],
            f"ID{id_value}DATA": [0]
        }
        data = pd.DataFrame(columns)
        data["KNR"] = df["KNR"].iloc[0] if not df.empty else None
        return data.set_index("KNR")
    else:
        return (
            subset.groupby("KNR")
            .agg(
                NAME=("NAME", "count"),
                SOK=("STATUS", lambda x: (x == 10).sum()),
                SNOK=("STATUS", lambda x: (x == 13).sum()),
                DATA=("DATA", lambda x: (x.max() - x.min()).total_seconds() / (3600 * 24) if len(x) > 1 else 0),
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
    colunas_normalizacao = [
        "ID1NAME", "ID1SOK", "ID1SNOK", "ID1DATA",
        "ID2NAME", "ID2SOK", "ID2SNOK", "ID2DATA",
        "ID718NAME", "ID718SOK", "ID718SNOK", "ID718DATA",
    ]
    scaler = MinMaxScaler()
    df[colunas_normalizacao] = scaler.fit_transform(df[colunas_normalizacao])
    return df

def execute(df_resultados_processed_1):
    df = df_resultados_processed_1.copy()
    drop_colunas(df)

    id1 = agregar_por_id(df, 1)
    id2 = agregar_por_id(df, 2)
    id718 = agregar_por_id(df, 718)

    df_combined = (
        id1.join(id2, on="KNR", how="outer")
        .join(id718, on="KNR", how="outer")
        .reset_index()
    )

    df_combined = df_combined.fillna(0)

    df_combined = normalizacao(df_combined)

    return df_combined
