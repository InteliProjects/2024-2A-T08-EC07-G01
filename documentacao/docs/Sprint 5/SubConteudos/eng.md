---
title: "Engenharia de Dados"
sidebar_position: 5
---

## **1.1** Introdução

A **Engenharia de Dados** é um campo fundamental para garantir que grandes volumes de informações possam ser processados, transformados e analisados de forma eficiente. Neste documento, será aboradado o processo de construção da pipeline de dados do projeto, para desenvolver um modelo de detecção de falhas em veículos. A pipeline inclui as etapas de extração, transformação, normalização e carregamento de dados, além da criação, treinamento e avaliação de um modelo de rede neural do tipo **GRU (Gated Recurrent Unit)**.

### **1.2** Ferramentas Utilizadas

Ao longo da pipeline foram utilizadas certas ferramentas essenciais para o desenvolvimento do projeto. Entre elas estão:

- **TensorFlow**: Uma biblioteca de código aberto para aprendizado de máquina e aprendizado profundo.
- **Pandas**: Uma biblioteca de software escrita como extensão da linguagem de programação Python para manipulação e análise de dados.
- **Sklearn**: Uma biblioteca de software para aprendizado de máquina e mineração de dados.

Entre outras principais do Python, como **Numpy**, etc.

## **2.1** ETL (Extração, Transformação e Carregamento)

A pipeline de ETL é composta por diversas etapas que visam preparar os dados para a modelagem preditiva. A seguir, detalhamos cada uma dessas etapas e como elas são implementadas. Vale lembrar que no caso deste projeto, cada parte da pipeline ficou dividida em Scripts separados com uma função principal chamada `execute` que é chamada no **Orquestrador**.

:::tip
Em relação à como elas são chamadas e funcionam, olhe a documentação do **Orquestrador** [aqui](/Sprint%204/Pipelines/Orquestrador)
:::

### **2.2** Processamento Inicial dos Resultados

Nesta etapa, a função `processar_resultados` remove valores nulos (NaN) e converte a coluna `DATA` para o formato de datetime, permitindo que operações temporais possam ser realizadas.

```python
import pandas as pd

def processar_resultados(df_resultados):
    df = df_resultados.dropna()
    df["DATA"] = pd.to_datetime(df["DATA"], errors="coerce")
    return df
```

### **2.3** Merge dos Resultados e Falhas

A função `merge_dados` realiza o merge entre os resultados e os dados de falhas. A junção é feita com base na coluna `KNR`, garantindo que todas as informações estejam disponíveis em um único DataFrame, facilitando a análise posterior e o treinamento.

```python
def merge_dados(df_resultados, df_falhas):
    merged_df = pd.merge(df_resultados, df_falhas, on="KNR", how="left")
    merged_df = merged_df.fillna(0)
    return merged_df
```

### **2.4** Transformação e Normalização dos Dados

Antes de alimentar o modelo com os dados, algumas etapas de transformação e normalização são realizadas. A função `drop_colunas` remove colunas que não são necessárias para a modelagem. Já a função `agregar_por_id` agrega os dados por ID, agrupando-os por `KNR` e calculando diversas estatísticas, como o total de `NAME` e a soma de estados específicos de `STATUS`.

A normalização é feita utilizando `MinMaxScaler`, que ajusta os dados para uma escala entre 0 e 1. Isso é importante para garantir que todas as variáveis tenham o mesmo peso durante o treinamento do modelo.

```python
from sklearn.preprocessing import MinMaxScaler

def drop_colunas(df):
    colunas = ["UNIT", "VALUE_ID", "VALUE"]
    df.drop(columns=colunas, axis=1, inplace=True)

def agregar_por_id(df, id_value):
    subset = df[df["ID"] == id_value]
    return subset.groupby("KNR").agg({
        "NAME": "count",
        "STATUS": lambda x: (x == 10).sum()
    })

def normalizacao(df):
    scaler = MinMaxScaler()
        colunas_normalizacao = ["ID1NAME", "ID1SOK", "ID1SNOK", "ID1DATA"]
    df[colunas_normalizacao] = scaler.fit_transform(df[colunas_normalizacao])
    return df
```

### **2.5** Preparação de Dados

A função `preparacao_dados` é a etapa final do ETL no pipeline de dados. Aqui, as features (variáveis independentes) são separadas da variável alvo (target), que neste caso é a coluna `FALHA`. O `KNR`, que é um identificador único para cada veículo, é removido das features, pois não possui relevância para o modelo preditivo. Os dados são então divididos em conjuntos de treino e teste.

```python
from sklearn.model_selection import train_test_split
import numpy as np

def preparacao_dados(df):
    X = df.drop(columns=["FALHA", "KNR"])
    y = df["FALHA"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = np.array(X_train).reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = np.array(X_test).reshape((X_test.shape[0], X_test.shape[1], 1))
    # highlight-next-line
    return X_train, X_test, y_train, y_test
```

## **3.1** Modelagem e Treinamento

Após a etapa de ETL, o próximo passo é construir e treinar o modelo preditivo.

## **3.2** Construção do Modelo Random Forest

O modelo Random Forest é um conjunto de árvores de decisão que é utilizado para realizar a classificação binária (se tem ou não falha). A função execute (função que é chamada no Orquestrador) constrói o modelo Random Forest, configurando-o para realizar a classificação. O modelo é treinado com os dados processados.

```python
from sklearn.ensemble import RandomForestClassifier

def execute(df_merged):
X_train, X_test, y_train, y_test = preparacao_dados(df_merged)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
return model
```

### **3.3** Avaliação do Modelo

:::tip Info
Para ter uma visão melhor de como foi escolhido o modelo a ser utilizado, veja a documentação de **[Modelagem e implementação da I.A](/Sprint%205/SubConteudos/mod)**
:::

Após o treinamento, o modelo é avaliado com base em várias métricas importantes, como a **acurácia** (accuracy), **recall**, **f1_score** e **precisão** (precision). Essas métricas permitem avaliar a performance do modelo em diferentes aspectos, como a proporção de predições corretas e a capacidade de identificar corretamente as classes positivas (falhas).

:::warning
Dado o escopo do projeto, focamos em trabalhar para adquirir a melhor taxa de **recall** e **precisão**, levando em conta que é mais importante detectar as falhas **SEMPRE** do que acertar as não falhas **SEMPRE**.
:::

```python
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score

def evaluate_model(model, X_test, y_test):
    y_pred = (model.predict(X_test) > 0.5).astype(int).flatten()
    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    # highlight-next-line
    return {"accuracy": accuracy, "recall": recall, "f1_score": f1, "precision": precision}
```

### **3.4** Execução Final e Salvamento do Modelo

Após todas as transformações, o modelo é treinado e salvo em um arquivo `.h5`. Isso permite que o modelo seja reutilizado posteriormente sem a necessidade de retreinamento. O modelo é armazenado no diretório especificado no código.

:::warning IMPORTANTE

Atualmente o modelo é salvo localmente pelo limite de tempo, todavia, há toda a lógica no **Backend** para salvá-lo no GridFS do MongoDB, melhorando a alocação de espaço.
:::

```python
import os

def save_model(model):
    model_path = os.path.join(os.getcwd(), 'app', 'pipeline', 'model.h5')
    model.save(model_path)
```

## **4.1** Orquestração de Pipeline

Para garantir que todo o pipeline seja executado de forma organizada e com logs apropriados, é utilizada a classe `Orchestrator`. Ela realiza a orquestração de todos os passos do pipeline de forma dinâmica, registrando logs em caso de sucesso ou erro, e permitindo que novos scripts sejam carregados dinamicamente a partir de um sistema de arquivos distribuído (GridFS).

```python
class Orchestrator:
    def __init__(self, pipeline_steps, mongo_uri, db_name):
        self.pipeline_steps = pipeline_steps
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.logs = []

    # highlight-start
    def run_dynamic_pipeline(self):
        for step in self.pipeline_steps:
            module = self.load_module(step["name"], step["file_path"])
            result = module.execute(**step["kwargs"])
            self.save_logs()
        return "Pipeline executado com sucesso!"
    # highlight-end
```

## **5.1** Conclusão

A pipeline apresentada demonstra as etapas fundamentais para a construção de uma solução completa de processamento e análise de dados, focada na detecção de falhas em veículos. Ao combinar etapas de **extração, transformação e carregamento de dados** (ETL) com o uso de redes neurais para classificação, é possível construir uma solução robusta e escalável. O modelo treinado e salvo pode ser utilizado para inferências futuras, e a estrutura de logs permite um acompanhamento detalhado da execução do pipeline. Este exemplo também demonstra a importância da normalização dos dados e da organização modular do código para facilitar a manutenção e a escalabilidade da solução.

Além disso, o código para treinamento e análise de dados pode ser facilemente mudável futuramente, graças a lógica presente no Backend que permite facil alteração entre os códigos. Para saber mais veja a parte referente ao **Orquestrador** [aqui](/Sprint%204/Pipelines/Orquestrador)
