import pandas as pd


def executable(df):
    # excluir registros com valores nulos
    df_brute = df.dropna()

    #Retira os valores MULTIVALUE
    df = df_brute.drop(df_brute[df_brute['S_GROUP_ID'] == '#MULTIVALUE'].index)

    #Define o tipo da coluna S_GROUP_ID como inteiro
    df['S_GROUP_ID'] = df['S_GROUP_ID'].astype(int)

    #Retira as colunas que não serão utilizadas
    df = df.drop(['USUARIO', 'FALHA', 'MODELO', 'ESTACAO', 'HALLE'], axis=1)

    #Retira os registros que possuem MOTOR vazio
    df = df.drop(df[df['MOTOR'] == '   '].index)

    ################################################
    # One Hot Encoding da coluna de tipos de falha #
    ################################################

    df_one_hot = pd.get_dummies(df, columns=['S_GROUP_ID'])
    columns = ['S_GROUP_ID_-2','S_GROUP_ID_1','S_GROUP_ID_2','S_GROUP_ID_4','S_GROUP_ID_5','S_GROUP_ID_133','S_GROUP_ID_137','S_GROUP_ID_140','S_GROUP_ID_9830946']
    for column in columns:
        df_one_hot[column] = df_one_hot[column].map({True: 1 ,  False: 0 })
    grouped_df = df_one_hot.groupby('KNR').agg({
    'COR': 'first',
    'MOTOR': 'first',
    'S_GROUP_ID_-2': 'sum',
    'S_GROUP_ID_1': 'sum',
    'S_GROUP_ID_2': 'sum',
    'S_GROUP_ID_4': 'sum',
    'S_GROUP_ID_5': 'sum',
    'S_GROUP_ID_133': 'sum',
    'S_GROUP_ID_137': 'sum',
    'S_GROUP_ID_140': 'sum',
    'S_GROUP_ID_9830946': 'sum'
    }).reset_index()

    #############################################
    #One Hot Encoding das Colunas de Cor e Motor#
    #############################################

    df_final = pd.get_dummies(grouped_df, columns=['COR','MOTOR'])

    columns_to_convert = [
    'COR_0Q0Q', 'COR_0QA1', 'COR_2R2R', 'COR_2RA1', 'COR_5T5T', 
    'COR_5TA1', 'COR_6K6K', 'COR_6KA1', 'COR_6UA1', 'COR_A1A1',
    'COR_K2A1', 'COR_K2K2', 'MOTOR_CWL', 'MOTOR_CWS', 'MOTOR_DHS', 'MOTOR_DRP'
    ]   

    # Converter as colunas de booleano para 0 e 1
    df_final[columns_to_convert] = df_final[columns_to_convert].astype(int)   

    # Convertendo os dados das colunas S_GROUP_ID para booleano
    df_final['S_GROUP_ID_-2', 'S_GROUP_ID_1', 'S_GROUP_ID_2', 'S_GROUP_ID_4', 'S_GROUP_ID_5', 'S_GROUP_ID_133', 'S_GROUP_ID_137', 'S_GROUP_ID_140', 'S_GROUP_ID_9830946'] = df_final['S_GROUP_ID_-2', 'S_GROUP_ID_1', 'S_GROUP_ID_2', 'S_GROUP_ID_4', 'S_GROUP_ID_5', 'S_GROUP_ID_133', 'S_GROUP_ID_137', 'S_GROUP_ID_140', 'S_GROUP_ID_9830946'].astype(bool)

    return df_final  

    