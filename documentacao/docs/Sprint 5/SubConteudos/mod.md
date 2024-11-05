---
title: "Modelagem e implementação da I.A"
sidebar_position: 5
---

## **1.1** Introdução

Dado o escopo do projeto, de desenvolver um modelo preditivo para detectar falhas nos veículos da Volkswagen, foi escolhido um modelo de **Random Forest**, devido à sua capacidade de lidar com dados de alta dimensionalidade, flexibilidade, e bom desempenho em termos de **acurácia** e **recall**.

Além disso, a pipeline de dados foi implementado de forma robusta para manipular grandes volumes de informações e integrá-las de maneira eficiente ao modelo, permitindo que o sistema fosse flexível e escalável.

:::tip Info
Para ter uma visão melhor de como foi feito o pipeline de dados, veja a documentação de [Engenharia de Dados](/Sprint%205/SubConteudos/eng)
:::

## **1.2** Testes com Modelos para Classificar o Tipo de Falha

Utilizamos diferentes algoritmos de aprendizado de máquina, como Regressão Logística, XGBoost e Random Forest, pois estes são amplamente reconhecidos por sua eficácia em problemas de classificação.

A escolha desses modelos se baseia em sua capacidade de lidar com dados complexos e não-lineares, além de fornecerem uma boa balanceamento entre interpretabilidade e desempenho. A Regressão Logística, por exemplo, é um modelo simples que permite uma fácil interpretação dos coeficientes, enquanto que o XGBoost e o Random Forest são conhecidos por sua alta performance em conjuntos de dados desbalanceados, comuns em problemas de classificação de falhas.

### **1.2.1** Objetivos

Neste notebook ( `src/models/modelo_todas_classes.ipynb`) Focamos em testar esses três modelos para identificar qual deles apresenta o melhor desempenho no conjunto de dados fornecido. A eficácia de cada modelo é medida por meio de métricas como acurácia, **precisão**, **recall** e **F1-Score**, que nos fornecem uma visão abrangente do desempenho do modelo em relação às classes majoritária e minoritária.

### **1.2.2** Metodologia

No notebook localizado em `src/models/modelo_classificacao_falha1.ipynb`, foram realizados testes preliminares utilizando redes neurais. No entanto, para aprofundar nossa análise, neste documento, exploramos o desempenho de modelos de Regressão Logística, XGBoost e Random Forest, com o objetivo de encontrar o modelo mais adequado para classificar os tipos de falha associados ao `S_GROUP_ID_1`.

Durante o desenvolvimento do projeto, foi constatado que não era possível construir uma série temporal válida, pois os dados de data eram lançados todos ao mesmo tempo, dificultando a montagem de uma ordem cronológica coerente. Devido a essa limitação, **redes neurais**, especialmente aquelas que dependem de sequências temporais como as **RNNs** ou **GRUs**, não eram a escolha mais adequada. Por essa razão, optou-se pela utilização do modelo de **Random Forest**, que não depende de informações temporais para realizar boas predições.

#### **1.2.2.1** Detalhes dos Testes

- Carregamento dos Dados: Iniciamos o processo carregando o DataFrame que contém os dados de falhas e torques, assegurando que os dados estejam limpos e prontos para serem utilizados nos modelos.

- Pré-processamento: As colunas foram convertidas para representações binárias para refletir a presença ou ausência de falhas, e colunas com dados faltantes foram removidas para garantir a integridade dos dados.

- Modelo Random Forest: Implementamos o Random Forest como um dos modelos de referência, reconhecido por sua robustez e capacidade de lidar com grandes volumes de dados.

- Modelo XGBoost: Em seguida, utilizamos o XGBoost, um modelo de gradient boosting que tem se mostrado eficaz em competições de ciência de dados devido à sua capacidade de lidar com complexidades no conjunto de dados.

- Modelo de Regressão Logística: Por último, implementamos a Regressão Logística para uma comparação direta com os modelos mais complexos, permitindo uma visão clara das suas diferenças em termos de performance.

- Avaliação do Modelo: As previsões de cada modelo foram avaliadas usando métricas apropriadas, que nos permitiram determinar não apenas a acurácia, mas também a capacidade de cada modelo de identificar corretamente as classes de falhas.

Esses passos garantem que a análise seja não apenas rigorosa, mas também alinhada com as melhores práticas em ciência de dados, visando encontrar a solução mais eficaz para a classificação do tipo de falha.

## **1.3** Lógica da Implementação da Pipeline e Escolha de Features

### **1.3.1** Escolha do Modelo: Random Forest

O **Random Forest** foi escolhido devido à sua robustez em lidar com grandes volumes de dados e sua capacidade de identificar padrões complexos entre as features sem a necessidade de ordenar os dados temporalmente. Esse algoritmo é uma variação do método de árvores de decisão, onde múltiplas árvores são construídas durante o treinamento e cada árvore contribui com uma "votação" para determinar a predição final.

O **Random Forest** se destaca por:

- Redução do Overfitting: Ao combinar as predições de várias árvores, o modelo consegue reduzir o risco de overfitting, o que é comum em modelos baseados em uma única árvore de decisão.
- Flexibilidade: Ele é capaz de lidar com dados de alta dimensionalidade e variáveis categóricas e numéricas sem a necessidade de normalização.
- Resistência a Ruído: A média das predições de várias árvores torna o modelo mais resistente ao ruído presente nos dados.

:::tip Info
**Random Forest** é um algoritmo de aprendizado de máquina baseado em um conjunto de árvores de decisão. Durante o treinamento, várias árvores são construídas a partir de subconjuntos aleatórios dos dados e das features, e a predição final é feita com base na votação da maioria das árvores. Isso o torna robusto, capaz de capturar interações complexas entre as variáveis, e eficiente para lidar com conjuntos de dados onde não há dependências temporais.
:::
A escolha do **Random Forest** garantiu um bom equilíbrio entre acurácia e recall nos testes, permitindo ao modelo minimizar falsos negativos — falhas que não são detectadas. Isso é essencial no contexto da detecção de falhas em veículos, onde a não detecção de problemas pode acarretar em consequências graves..

### **1.3.2** Pipeline de Treinamento

A pipeline de treinamento foi cuidadosamente estruturada para garantir que os dados fossem corretamente manipulados antes de serem usados no modelo. As etapas incluem:

1. **Pré-processamento dos Dados**: Os dados são preparados por meio da função preparacao_dados, que separa as features e o target e transforma os dados em arrays NumPy.
2. **Estruturação do Modelo Random Forest**: O modelo Random Forest é criado com um número especificado de árvores, cada uma treinada em uma amostra aleatória dos dados. O modelo é configurado para realizar a classificação binária (falha ou não).
3. **Treinamento e Avaliação**: Após o treinamento, o modelo é avaliado com base nas métricas de acurácia, recall, f1_score e precisão.

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score

def execute(df_merged):
    X_train, X_test, y_train, y_test = preparacao_dados(df_merged)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred)
    }
```

## **1.4** Consolidação do pipeline de dados com encapsulamento em classes e adequado para um deploy contínuo

Foi feita a consolidação do pipeline de dados em uma classe Python, permitindo que o processo de treinamento e avaliação do modelo GRU seja executado de forma modular e organizada. A classe encapsula as etapas de preparação dos dados, treinamento do modelo e avaliação, facilitando a reutilização e manutenção do código.

### **1.4.1** O Papel do Orquestrador

O **Orchestrator** é a peça central do pipeline de dados, responsável por executar e coordenar dinamicamente cada etapa do processamento de forma organizada e modular. Ele permite a execução de várias fases do pipeline de forma automática, garantindo que o fluxo de dados ocorra sem interrupções.

Um dos principais benefícios do **Orchestrator** é que ele pode carregar scripts de processamento dinamicamente de um sistema de arquivos distribuído, como o **GridFS**, permitindo que as etapas do pipeline sejam atualizadas ou modificadas sem que seja necessário interromper o sistema.

### **1.4.2** Explicação Detalhada do Código do Orquestrador

O **Orchestrator** foi projetado para oferecer flexibilidade e escalabilidade ao pipeline. Suas principais funcionalidades incluem:

- **Configuração Dinâmica**: O pipeline é configurado por meio de um arquivo JSON, que especifica cada etapa de processamento, como o nome dos módulos, os arquivos de script e os DataFrames envolvidos.
- **Execução Modular**: Cada etapa do pipeline é encapsulada em um módulo Python separado. O orquestrador executa esses módulos em sequência, injetando os DataFrames necessários em cada etapa, garantindo a integridade dos dados ao longo do processo.
- **Carregamento de Scripts**: A função `fetch_script_from_gridfs` carrega dinamicamente os scripts do GridFS, permitindo que o pipeline seja atualizado sem interrupções no fluxo.

**Código do Orquestrador:**

```python
class Orchestrator:
    def __init__(self, pipeline_steps, dataframes, mongo_uri, db_name):
        self.pipeline_steps = pipeline_steps
        self.dataframes = dataframes  # Dictionary to store DataFrames
        self.logs = []
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db)

    def run_dynamic_pipeline(self):
        for step in self.pipeline_steps:
            module_name = step["name"]
            file_path = step["file_path"]
            kwargs = step.get("kwargs", {}).copy()

            dataframes_needed = step.get("dataframes", [])
            for df_name in dataframes_needed:
                if df_name in self.dataframes:
                    kwargs[df_name] = self.dataframes[df_name]
                else:
                    raise ValueError(f"DataFrame '{df_name}' not found for step '{module_name}'.")

            script_content = self.fetch_script_from_gridfs(file_path)
            module = self.load_module_from_file(module_name, script_content)

            result = self.execute_step(step["name"], module, **kwargs)

            output_df_name = step.get("output_dataframe")
            if output_df_name:
                self.dataframes[output_df_name] = result

        return self.dataframes
```

### **1.4.3** Exemplo de Execução de Múltiplas Etapas

O pipeline processa e normaliza os dados de entrada antes de serem alimentados no modelo GRU. As principais etapas incluem:

1. **Processamento dos Resultados**: A função `drop_colunas` remove colunas desnecessárias, enquanto a função `agregar_por_id` agrega os dados por identificadores (ID).
2. **Normalização**: As colunas relevantes são normalizadas utilizando o **MinMaxScaler**, preparando os dados para o modelo.
3. **Treinamento e Predição**: O modelo GRU é treinado com os dados processados, e as predições subsequentes são geradas.

O orquestrador garante que cada uma dessas etapas seja executada de forma ordenada e sem interrupções, registrando logs para facilitar a auditoria e o debugging.

:::info

Para saber mais do Orquestrador, clique [aqui](/Sprint%204/Pipelines/Orquestrador)
:::

## **2.1** Conclusão

O pipeline de machine learning para predição de falhas em veículos foi projetado para ser modular, escalável e eficiente. A escolha do modelo **GRU** proporcionou o melhor equilíbrio entre **acurácia** e **recall**, sendo crucial para garantir que falhas não sejam negligenciadas pelo sistema, reduzindo o risco de falsos negativos.

O **Orchestrator** desempenha um papel vital na execução do pipeline, facilitando a orquestração dinâmica de múltiplas etapas de processamento, permitindo atualizações contínuas e assegurando que o sistema esteja sempre operando de forma eficiente. Este pipeline é uma solução robusta e preparada para escala, oferecendo flexibilidade para futuras expansões e melhorias.
