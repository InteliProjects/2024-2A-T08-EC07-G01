## 1. Estrutura de Pastas e Documentação dos Scripts

Para a automatização da preparação dos dados, foram desenvolvidos dois diretórios principais, cada um contendo scripts relacionados ao pré-processamento de dados e construção de modelos, além de um script global, que depois serão chamados numa pipeline orquestradora. A seguir, uma explicação de cada pasta e o que cada arquivo faz.

### 1.1. Estrutura de Pastas

:::tip Info
Esses diretórios podem ser encontrados em ```src/models/scripts```!
:::

```bash
- modelo_classificacao
    |_ falhas.py
    |_ merge_torques_falhas.py
    |_ modelo.py
    |_ torques.py
- modelo_principal
    |_ falhas.py
    |_ falhas2.py
    |_ merge.py
    |_ modelo.py
    |_ resultado.py
    |_ resultado2.py
- preparacao.py 
```

## 2. Descrição dos Arquivos

### 2.1. Pasta `modelo_classificacao`:

- **2.1.1. Falhas.py**
    - Este script realiza o pré-processamento dos dados de falhas, removendo registros nulos, aplicando a codificação one-hot e agregando colunas para posterior uso nos modelos. Ele inclui tratamento específico para a coluna `S_GROUP_ID` (que é a coluna que armazena o tipo de falha) e gera um DataFrame pronto para análise e modelagem, como é possível observar no código abaixo:  
ㅤㅤㅤㅤ
    ```python
    import pandas as pd

    def execute(df):
        '''
        Function to prepare the data for the classification model, uses the fails dataset, AKA the dataset after main model is ran.

        Parameters:
        df: pandas DataFrame 
        '''
        df_brute = df.dropna()

        df = df_brute.drop(df_brute[df_brute['S_GROUP_ID'] == '#MULTIVALUE'].index)

        df['S_GROUP_ID'] = df['S_GROUP_ID'].astype(int)

        df = df.drop(['USUARIO', 'FALHA', 'MODELO', 'ESTACAO', 'HALLE', 'COR', 'MOTOR'], axis=1)

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

        df_final[columns_to_convert] = df_final[columns_to_convert].astype(int)   

        df_final['S_GROUP_ID_-2', 'S_GROUP_ID_1', 'S_GROUP_ID_2', 'S_GROUP_ID_4', 'S_GROUP_ID_5', 'S_GROUP_ID_133', 'S_GROUP_ID_137', 'S_GROUP_ID_140', 'S_GROUP_ID_9830946'] = df_final['S_GROUP_ID_-2', 'S_GROUP_ID_1', 'S_GROUP_ID_2', 'S_GROUP_ID_4', 'S_GROUP_ID_5', 'S_GROUP_ID_133', 'S_GROUP_ID_137', 'S_GROUP_ID_140', 'S_GROUP_ID_9830946'].astype(bool)

        return df_final
    ```

- **2.1.2. Torques.py**
    - Este script realiza o pré-processamento dos dados de torque, incluindo a limpeza dos valores, agregação por `KNR` e `UNIT`, e normalização dos dados numéricos. Ele também implementa um pipeline completo de pré-processamento para uso em modelos de classificação. A função abaixo é a ```execute()```, que é responsável por chamar as funções auxiliares que são responsáveis por realizar cada uma das tarefas mencionadas.  
    ㅤㅤㅤㅤㅤ
    ```python
    def execute(df):

        df = df[df["UNIT"] != '          ']  # Remove onde UNIT tem espaços
        df["UNIT"] = df["UNIT"].str.strip() 

        #faz o pré-processamento dos torques
        df = preprocess_torque(df)

        #Agrupar os dados por KNR e UNIT
        df_pivot = aggregate_by_knr_unit(df)

        #Todos as colunas com letras maiúsculas para a padronização.
        df_pivot.columns = df_pivot.columns.str.upper()

        #Normalização dos dados
        df_pivot = normalize_columns(df_pivot, exclude_columns=['KNR', 'UNIT'])

        # Exemplo de como pode ser feito um merge, caso precise
        # df_resultados_final = df_merged.merge(df_pivot, on='KNR', how='left')

        return df_pivot
    ```

- **2.1.3. Merge_torques_falhas.py**
    - Realiza a junção (merge) dos dados de falhas com os dados de torque a partir de uma chave comum (`KNR`). O objetivo é ter todas as informações a respeito dos KNRS que possuem falhas em um único DataFrame para os modelos de classificação de falha.  

```python
import pandas as pd
import numpy as np

def execute(df_torques, df_falhas):
    '''
    Merges both the torques and fails datasets, using the KNR column as the key.

    Parameters:
    df_torques: pandas DataFrame of torques
    df_falhas: pandas DataFrame of fails
    '''
    df_merged = df_torques.merge(df_falhas, on='KNR', how='left')
    return df_merged
```

- **2.1.4. Modelo.py**
    - Contém a lógica para a construção e treinamento de um modelo de rede neural recorrente (GRU). Ele utiliza dados preparados para treinamento e validação, definidos no arquivo `preparacao.py`, e constrói um modelo sequencial com camadas GRU e uma camada final densa com ativação sigmoide.  

```python
def execute(df):
    '''
    Script to build the GRU model for classification and train it.

    Parameters:
    df: pandas DataFrame
    '''
    X_train, X_test, y_train, y_test = preparacao.preparacao_dados(df)
    model = Sequential()

    model.add(GRU(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(GRU(50, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy')

    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

    return model
```  

### 2.2. Pasta `modelo_principal`:

- **2.2.1. Falhas.py**
    - Faz a leitura de um arquivo CSV de falhas e aplica transformações, como remoção de registros duplicados baseados na coluna `KNR` e conversão da coluna `FALHA` para valores binários.

    ```python
    def execute (file_path):
    '''
    Reads a CSV file and returns a DataFrame with the 'FALHA' column converted to 1 and all duplicates removed.

    Parameters:
    file_path: str
    '''
    df = pd.read_csv(file_path)
    df['FALHA'] = df['FALHA'].str.upper()
    # Remove todas as linhas com KNR repetido
    df = df.drop_duplicates(subset=['KNR'])
    df['FALHA'] = 1

    return df
    ```

- **2.2.2. Falhas2.py**
    - Remove colunas irrelevantes para a análise de falhas e retorna o DataFrame simplificado.

    ```python
    def execute(df):
    # TODO: Change the function, to also input the columns to remove
    '''
    Remove columns from the DataFrame that are not present in vehicles that don't have failures.

    Parameters:
    df: pandas DataFrame
    '''
    colunas = ['MODELO', 'COR', 'MOTOR', 'ESTACAO', 'USUARIO', 'HALLE', 'DATA']
    df = df.drop(columns=colunas, axis=1)
    return df
    ```

- **2.2.3. Merge.py**
    - Faz o merge entre dois arquivos CSV: um contendo resultados e outro contendo falhas, unindo as informações a partir da coluna `KNR` e preenchendo valores nulos com zero.

    ```python
    def execute(df_resultados, df_falhas):
    '''
    Script to merge the results and failures DataFrames.

    Parameters:
    df_resultados: str
    df_falhas: str
    '''
    resultados = pd.read_csv(df_resultados)
    falhas = pd.read_csv(df_falhas)
    merged_df = pd.merge(resultados, falhas, on='KNR', how='left')
    # Adiciona 0 em todos os NaN
    merged_df = merged_df.fillna(0)
    return merged_df
    ```

- **2.2.4. Modelo.py**
    - Similar ao script de `modelo_classificacao`, este arquivo também constrói um modelo de rede neural GRU para previsão, utilizando os dados já processados e prontos para modelagem.

    ```python
    def execute(df):
    '''
    Script to build the GRU model for classification and train it.

    Parameters:
    df: pandas DataFrame
    '''
    X_train, X_test, y_train, y_test = preparacao.preparacao_dados(df)
    # Construção do modelo com GRU
    model = Sequential()

    model.add(GRU(50, activation='relu', return_sequences=True, input_shape=(X_train.shape[1], 1)))
    model.add(GRU(50, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer='adam', loss='binary_crossentropy')

    # Treinamento do modelo
    model.fit(X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test))

    return model
    ```

- **2.2.5. Resultado.py**
    - Realiza o pré-processamento dos dados de resultados, removendo valores nulos e convertendo a coluna `DATA` para o tipo datetime. O resultado é salvo em um novo arquivo CSV.


    ```python
    def execute(file_path):
    '''
    Script to read a CSV file and return a DataFrame with the 'DATA' column converted to datetime and all NaN values removed.

    Parameters:
    file_path: str
    '''
    df = pd.read_csv(file_path)
    df= df.dropna() 
    df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')
    return df
    ```

- **2.2.6. Resultado2.py**
    - Faz o pré-processamento adicional dos dados, agregando-os por ID e aplicando normalização. As colunas de interesse são calculadas a partir de valores específicos de `ID`, e o resultado final é um DataFrame com essas informações normalizadas e agregadas.

    ```python
    def execute(df):
    '''
    Script to preprocess the whole DataFrame.

    Parameters:
    df: pandas DataFrame
    '''
    drop_colunas(df)
    
    id1 = agregar_por_id(df, 1)
    id2 = agregar_por_id(df, 2)
    id718 = agregar_por_id(df, 718)

    # Combinando os resultados em um único DataFrame
    df = id1.join(id2, on='KNR', how='outer').join(id718, on='KNR', how='outer').reset_index()

    # Reordenando as colunas para o formato desejado
    df = df[['KNR','ID1NAME', 'ID1SOK', 'ID1SNOK', 'ID1DATA', 'ID2NAME', 'ID2SOK', 'ID2SNOK', 'ID2DATA', 'ID718NAME', 'ID718SOK', 'ID718SNOK', 'ID718DATA']]

    df = normalizacao(df)

    df = df.fillna(0)

    return df
    ```

### 2.3 Script global `preparacao.py`

- **2.3.1. preparacao.py**
    - Este script contém uma função para preparar os dados antes de serem utilizados nos modelos. Ele realiza a separação entre features (`X`) e target (`y`), e faz a divisão dos dados em conjuntos de treino e teste. Além disso, ele reestrutura os dados de entrada para o formato adequado para redes neurais recorrentes (3 dimensões: `n_samples`, `n_features`, `1`).

    ```python
    def preparacao_dados(df):
        # Separando as features (X) e o target (y)
        X = df.drop(columns=['FALHA', 'KNR'])  # 'KNR' é apenas um identificador, então deve ser removido
        y = df['FALHA']
        # Separando em dados de treino e teste
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        # Converte X_train e X_test para arrays NumPy, caso ainda não sejam.
        X_train = np.array(X_train)
        X_test = np.array(X_test)

        # Reestrutura X_train e X_test para ter 3 dimensões.
        # A nova forma do array será (n_samples, n_features, 1)
        X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
        X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

        return X_train, X_test, y_train, y_test 

    ```
# 3. Conclusão

A estrutura de Scripts oferece uma abordagem organizada para a preparação de dados e desenvolvimento de modelos de classificação. Os scripts são distribuídos entre dois diretórios principais, cada um focado em aspectos diferentes do pipeline: pré-processamento de dados de falhas e torques, construção de modelos de classificação, e integração dos dados por meio de merges. 

Cada arquivo tem uma função clara e bem definida, desde a limpeza e normalização dos dados até a construção e treinamento de modelos baseados em redes neurais recorrentes (GRU). Esse nível de organização e modularização garante a flexibilidade e reutilização de código, permitindo que cada componente seja mantido e atualizado de forma independente. Além disso, o script global de preparação de dados (`preparacao.py`) centraliza a função de separação e transformação de dados, garantindo que o pipeline siga uma estrutura consistente e otimizada para redes neurais.

Com essa abordagem, o projeto está pronto para ser expandido ou ajustado conforme necessário, mantendo a integridade e clareza na organização dos scripts e suas respectivas funções.