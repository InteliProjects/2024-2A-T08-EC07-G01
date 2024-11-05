---
title: "Orquestrador de Scripts"
sidebar_position: 1
---

## **1.1** - Introdução

Este documento apresenta a estrutura e funcionalidades do **Orchestrator**, um componente desenvolvido para gerenciar e executar pipelines dinâmicos de scripts Python. A principal finalidade do orquestrador é coordenar diferentes etapas de processamento, facilitando a execução de scripts armazenados no sistema de arquivos do MongoDB, GridFS, extraindo resultados e manipulando DataFrames, além de gerenciar logs de execução.

O **Orchestrator** foi projetado para receber uma lista de etapas (`pipeline_steps`) e DataFrames (`dataframes`), que são processados de forma ordenada. Cada etapa define um script a ser executado, seu local de armazenamento, os DataFrames necessários para sua execução, além de argumentos adicionais, garantindo a flexibilidade na execução de diferentes tarefas de processamento de dados. Ao longo da execução do pipeline, o orquestrador lida com o carregamento dinâmico dos scripts, a execução de funções específicas em cada módulo, e o gerenciamento de resultados, armazenando novos DataFrames e model metadata conforme necessário.

Além disso, o orquestrador possui funcionalidades para registro de logs, assegurando o rastreamento de informações importantes durante a execução do pipeline. Cada execução gera logs detalhados que são salvos tanto em arquivos locais quanto na base de dados MongoDB, facilitando o monitoramento e a análise de eventuais problemas. Com esta abordagem modular e escalável, o **Orchestrator** facilita a integração de diferentes processos de dados, oferecendo um ambiente flexível e controlado para a execução de pipelines complexos.

## **2.1** - Script principal do Orquestrador

O script principal do **Orchestrator** foi desenvolvido para gerenciar a execução de diferentes etapas de um pipeline dinâmico. Ele foi organizado de forma modular para facilitar o entendimento e manutenção, oferecendo uma sequência de etapas bem definidas para coordenar o carregamento, execução de scripts e manipulação de DataFrames. A seguir, vamos dividir o script em partes específicas e detalhar o funcionamento de cada uma delas.

### **2.1.1** - Inicialização e configuração do Orquestrador

```python
class Orchestrator:
    def __init__(self, pipeline_steps, dataframes, mongo_uri, db_name):
        self.pipeline_steps = pipeline_steps
        self.dataframes = dataframes  # Dictionary to store DataFrames
        self.logs = []
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db)
```

Nesta seção, o orquestrador é inicializado com uma série de parâmetros essenciais para seu funcionamento:

- **`pipeline_steps`**: Lista de etapas a serem executadas, onde cada etapa define um script e suas configurações necessárias.
- **`dataframes`**: Dicionário que armazena DataFrames, utilizados como entrada ou saída para as diferentes etapas do pipeline.
- **`mongo_uri` e `db_name`**: Dados de conexão ao banco MongoDB para que os scripts e logs sejam gerenciados adequadamente.
- **`logs`**: Lista que armazena informações sobre a execução do pipeline, útil para rastreamento e depuração.

Após a inicialização, o **Orchestrator** cria uma conexão com o banco MongoDB e inicializa o sistema de arquivos GridFS para recuperar scripts diretamente do banco de dados.

### **2.1.2** - Log e manipulação de scripts

```python
def log(self, message, error=False):
    log_type = "ERROR" if error else "INFO"
    self.logs.append(f"[{log_type}] {message}")
    if error:
        self.save_logs()
```

- **`log`**: O método de logging captura informações e mensagens de erro durante a execução do pipeline. Logs de erro são salvos imediatamente para garantir que qualquer falha seja registrada e analisada posteriormente.

```python
def fetch_script_from_gridfs(self, file_path):
    try:
        with open(file_path, "rb") as grid_out:
            script_content = grid_out.read()
        self.log(f"Script '{file_path}' successfully fetched.")
        return script_content
    except Exception as e:
        self.log(f"Error fetching script from GridFS: {e}", error=True)
        raise
```

- **`fetch_script_from_gridfs`**: Este método faz a leitura de scripts armazenados no GridFS, garantindo que cada etapa do pipeline tenha o código necessário para ser executada. Em caso de erro, uma mensagem de log é registrada.

```python
def load_module_from_file(self, module_name, script_content):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
    temp_file.write(script_content)
    temp_file.close()

    try:
        spec = importlib.util.spec_from_file_location(module_name, temp_file.name)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        self.log(f"Module '{module_name}' successfully loaded from {temp_file.name}.")
        return module
    except Exception as e:
        self.log(f"Error loading module '{module_name}' from file: {e}", error=True)
        raise
    finally:
        os.remove(temp_file.name)
```

- **`load_module_from_file`**: Após obter o conteúdo do script, ele é salvo em um arquivo temporário para ser carregado dinamicamente como um módulo Python. Isso permite que funções contidas no script sejam acessadas e executadas pelo **Orchestrator**. Após o uso, o arquivo temporário é excluído para manter a integridade do ambiente de execução.

### **2.1.3** - Execução de etapas e pipeline dinâmico

```python
def execute_step(self, step_name, module, **kwargs):
    try:
        func_name = "execute"
        func = getattr(module, func_name)
        self.log(f"Executing '{step_name}'...")
        result = func(**kwargs)  # Pass any needed arguments
        self.log(f"'{step_name}' completed successfully.")
        return result
    except AttributeError as e:
        self.log(f"Function '{func_name}' not found in module '{module.__name__}': {e}", error=True)
        raise
    except Exception as e:
        self.log(f"Error during '{step_name}': {e}", error=True)
        raise
```

- **`execute_step`**: A execução de cada etapa do pipeline é realizada por este método. A função `execute` é esperada em todos os scripts, que são carregados como módulos. Caso a função não seja encontrada ou ocorra algum erro durante a execução, isso será registrado nos logs.

```python
def run_dynamic_pipeline(self):
    model_metadata = None
    for step in self.pipeline_steps:
        module_name = step["name"]
        file_path = step["file_path"]
        kwargs = step.get("kwargs", {}).copy()

        print(f"[DEBUG] Available DataFrames before '{step['name']}': {list(self.dataframes.keys())}")

        dataframes_needed = step.get("dataframes", [])
        for df_name in dataframes_needed:
            if df_name in self.dataframes:
                kwargs[df_name] = self.dataframes[df_name]
            else:
                print(f"[ERROR] DataFrame '{df_name}' not found for step '{module_name}'.")
                raise ValueError(f"DataFrame '{df_name}' not found for step '{module_name}'.")

        script_content = self.fetch_script_from_gridfs(file_path)
        module = self.load_module_from_file(module_name, script_content)

        # Execute the function and get the result
        result = self.execute_step(step["name"], module, **kwargs)

        output_df_name = step.get("output_dataframe")
        if output_df_name:
            self.dataframes[output_df_name] = result

        print(f"[DEBUG] Step '{module_name}' executed successfully. Output DataFrame: {output_df_name}")

        # Capture model metadata if the step is 'treina_modelo'
        if module_name == "treina_modelo":
            model_metadata = result
            print(model_metadata)

    print("[INFO] Pipeline completed successfully.")
    return model_metadata
```

- **`run_dynamic_pipeline`**: Este é o principal método do **Orchestrator**, responsável por coordenar a execução do pipeline. Cada etapa definida em `pipeline_steps` é processada em sequência:
  - **Carregamento de parâmetros**: Os parâmetros definidos em `kwargs` e os DataFrames necessários são preparados.
  - **Leitura de script**: O script para a etapa é carregado a partir do GridFS.
  - **Execução de etapa**: A função `execute` do script é chamada, passando os parâmetros necessários.
  - **Armazenamento de resultados**: Caso a etapa produza um DataFrame de saída, ele é armazenado no dicionário `dataframes`.

  Ao final do pipeline, o método retorna os metadados do modelo, se forem gerados durante a execução de alguma etapa específica (como a etapa `treina_modelo`).

### **2.1.4** - Salvamento de logs

```python
def save_logs(self):
    logs_dir = os.path.join(os.getcwd(), 'app', 'pipeline', 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_path = os.path.join(logs_dir, f"logs_{timestamp}.txt")

    with open(log_file_path, "a") as f:
        for log in self.logs:
            f.write(log + "\n")

    self.db.logs.insert_one({"timestamp": timestamp, "logs": self.logs})
    self.logs.clear()
```

- **`save_logs`**: O método `save_logs` salva os registros do pipeline em dois locais:
  - **Arquivo de log local**: Cria um arquivo `.txt` com os registros de log em um diretório específico.
  - **Banco de dados MongoDB**: Adiciona os registros ao banco de dados, permitindo o monitoramento centralizado dos logs de execução.

Este processo garante que todas as informações relevantes, sejam de sucesso ou erro, sejam registradas e armazenadas para futuras análises.

---

Com essa estrutura modular e eficiente, o **Orchestrator** coordena a execução de scripts dinâmicos, garantindo a integração de diferentes processos, tratamento de dados com DataFrames, e registro de logs para análise de desempenho e eventuais erros.

:::danger
Atualmente estamos utilizando tudo localmente, todavia a **ideia** é que o orquestrador seja capaz de **puxar** tanto os **scripts**, quanto o **dataframe** de resultados do **GridFS**, além de salvar as logs no MongoDB. Tornando a aplicação facilmente modificável e escalável.
:::

## **3.1** - Execução do Orquestrador

Para executar o **Orchestrator** e processar um pipeline de scripts, é necessário definir certos arquivos e configurações. A seguir, apresentamos um exemplo de como o **Orchestrator** pode ser utilizado para executar um pipeline de processamento de dados.

### **3.1.1** - JSON da pipeline


```json
{
    "model_path": "./pipeline/models/principal",
    "model_name": "principal",
    "prediction_steps": [
        {
            "name": "processa_falhas_1",
            "file_path": "/app/app/pipeline/steps/modelo_principal/processa_falhas_1.py",
            "dataframes": ["df_falhas"],
            "output_dataframe": "df_falhas_processed_1"
        },
        {
            "name": "processa_falhas_2",
            "file_path": "/app/app/pipeline/steps/modelo_principal/processa_falhas_2.py",
            "dataframes": ["df_falhas_processed_1"],
            "output_dataframe": "df_falhas_processed_2"
        },
        {
            "name": "processa_resultados_1",
            "file_path": "/app/app/pipeline/steps/modelo_principal/processa_resultados_1.py",
            "dataframes": ["df_resultados"],
            "output_dataframe": "df_resultados_processed_1"
        },
        {
            "name": "processa_resultados_2",
            "file_path": "/app/app/pipeline/steps/modelo_principal/processa_resultados_2.py",
            "dataframes": ["df_resultados_processed_1"],
            "output_dataframe": "df_resultados_processed_2"
        },
        {
            "name": "junta_falhas_resultados",
            "file_path": "/app/app/pipeline/steps/modelo_principal/junta_falhas_resultados.py",
            "dataframes": ["df_resultados_processed_2", "df_falhas_processed_2"],
            "output_dataframe": "df_merged"
        }
    ],
    "training_steps": [
        {
            "name": "treina_modelo",
            "file_path": "/app/app/pipeline/steps/modelo_principal/treina_modelo.py",
            "dataframes": ["df_merged"],
            "output_dataframe": "trained_model"
        }
    ]
}
```

Esse JSON representa a configuração de um pipeline de processamento de dados e treinamento de modelo no **Orchestrator**. Ele está dividido em duas principais seções: **`prediction_steps`** e **`training_steps`**, cada uma delas contendo etapas (`steps`) específicas para manipulação e processamento de dados. Vamos detalhar o que cada parte significa.

#### **3.1.1.1** model_path e model_name

- **`model_path`**: Define o caminho para o modelo que será gerenciado pelo pipeline, neste caso, `"./pipeline/models/principal"`. Este caminho é onde o modelo será salvo ou carregado para uso futuro.
  
- **`model_name`**: O nome do modelo, aqui especificado como `"principal"`. Isso facilita a identificação e a referência ao modelo durante as etapas de execução e no armazenamento dos metadados.

#### **3.1.1.2** prediction_steps

Esta seção contém uma lista de etapas relacionadas à manipulação de dados e preparação dos DataFrames necessários para o treinamento do modelo.

Cada etapa possui os seguintes campos:

- **`name`**: Nome descritivo da etapa, usado para identificação no pipeline. Exemplos incluem `"processa_falhas_1"`, `"processa_falhas_2"`, etc.

- **`file_path`**: Caminho do script Python que executa a lógica dessa etapa específica. Por exemplo, `"/app/app/pipeline/steps/modelo_principal/processa_falhas_1.py"` é o script que realiza a primeira etapa de processamento de falhas.

- **`dataframes`**: Lista de nomes de DataFrames que são necessários como entrada para essa etapa. Esses DataFrames devem já estar disponíveis no orquestrador antes da execução da etapa. Por exemplo, `"df_falhas"` é utilizado na primeira etapa `"processa_falhas_1"`.

- **`output_dataframe`**: O nome do DataFrame gerado como saída dessa etapa. Ele será armazenado no dicionário de DataFrames do orquestrador para uso em etapas subsequentes. Por exemplo, `"df_falhas_processed_1"` é o resultado da etapa `"processa_falhas_1"` e é utilizado como entrada para `"processa_falhas_2"`.

#### **3.1.1.3** Etapas do prediction_steps detalhadas

1. **`processa_falhas_1`**: 
   - Caminho do script: `"/app/app/pipeline/steps/modelo_principal/processa_falhas_1.py"`.
   - Usa o DataFrame de entrada `"df_falhas"` e gera `"df_falhas_processed_1"` como saída.

2. **`processa_falhas_2`**: 
   - Caminho do script: `"/app/app/pipeline/steps/modelo_principal/processa_falhas_2.py"`.
   - Processa o DataFrame `"df_falhas_processed_1"` e gera `"df_falhas_processed_2"`.

3. **`processa_resultados_1`**: 
   - Caminho do script: `"/app/app/pipeline/steps/modelo_principal/processa_resultados_1.py"`.
   - Usa `"df_resultados"` como entrada e produz `"df_resultados_processed_1"`.

4. **`processa_resultados_2`**: 
   - Caminho do script: `"/app/app/pipeline/steps/modelo_principal/processa_resultados_2.py"`.
   - Processa `"df_resultados_processed_1"` e produz `"df_resultados_processed_2"`.

5. **`junta_falhas_resultados`**: 
   - Caminho do script: `"/app/app/pipeline/steps/modelo_principal/junta_falhas_resultados.py"`.
   - Usa como entrada os DataFrames `"df_resultados_processed_2"` e `"df_falhas_processed_2"`.
   - Gera um DataFrame combinado chamado `"df_merged"`.

#### **3.1.1.4** training_steps

Esta seção define a etapa de treinamento do modelo. Ela contém as seguintes informações:

- **`name`**: Nome da etapa de treinamento, neste caso `"treina_modelo"`.
  
- **`file_path`**: Caminho para o script Python que realizará o treinamento do modelo, `"/app/app/pipeline/steps/modelo_principal/treina_modelo.py"`.

- **`dataframes`**: Lista de DataFrames necessários para o treinamento. Aqui, `"df_merged"` é o DataFrame combinado gerado pela última etapa de `prediction_steps`.

- **`output_dataframe`**: Nome dado ao modelo treinado resultante, `"trained_model"`.

Esta etapa executa o treinamento do modelo usando o DataFrame `df_merged` e produz um modelo treinado, que pode ser armazenado e utilizado em previsões futuras.

---

#### **3.1.1.5** Resumo do Fluxo

1. **Preparação dos DataFrames**: As etapas de `"processa_falhas_1"` a `"junta_falhas_resultados"` transformam os DataFrames brutos (`df_falhas` e `df_resultados`) em um DataFrame consolidado, `"df_merged"`.
  
2. **Treinamento do Modelo**: A etapa `"treina_modelo"` utiliza `"df_merged"` para treinar um modelo, cujo resultado é armazenado como `"trained_model"`.

Este JSON, portanto, configura todo o fluxo do pipeline, desde a preparação de dados até o treinamento do modelo final, oferecendo um caminho claro para o orquestrador executar e gerenciar as etapas necessárias para o processamento e aprendizado do modelo.

:::info
**Observação**: O JSON acima é um exemplo simplificado e pode ser adaptado conforme a necessidade de cada pipeline de processamento de dados.
Além disso, é essencial ajustar o nome dos DataFrames de saída e input. Atualmente o File_path é um caminho bruto local, a ideia é que seja um caminho do GridFS.
:::

### **3.1.2** - Exemplo script de treinamento

Segue abaixo um exemplo de script de treinamento que poderia ser utilizado em uma das etapas do pipeline, o mesmo até a Sprint 4 é o script utilizado afim de treinar nosso modelo principal, o qual é utilizado para prever se tem ou não falhas nos veículos.

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score


def preparacao_dados(df):
    '''
    Function to prepare the data for training the GRU model.

    Parameters:
    df: pandas DataFrame
    '''
    X = df.drop(
        columns=["FALHA", "KNR"]
    )
    y = df["FALHA"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    X_train = np.array(X_train)
    X_test = np.array(X_test)

    X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
    X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

    return X_train, X_test, y_train, y_test

def execute(df_merged):
    '''
    Script to build the GRU model for classification and train it.
    Parameters:
    df_merged: pandas DataFrame
    Returns:
    Sequential: Trained Keras model.
    '''
    X_train, X_test, y_train, y_test = preparacao_dados(df_merged)
    model = Sequential()
    model.add(
        GRU(
            50,
            activation="relu",
            return_sequences=True,
            input_shape=(X_train.shape[1], 1),
        )
    )
    model.add(GRU(50, activation="relu"))
    model.add(Dense(1, activation="sigmoid"))

    model.compile(optimizer="adam", loss="binary_crossentropy")

    model.fit(
        X_train, y_train, epochs=100, batch_size=32, validation_data=(X_test, y_test)
    )

    y_pred = model.predict(X_test)

    y_pred = (y_pred > 0.5).astype(int).flatten()

    accuracy = accuracy_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)

    model.save("./pipeline/model.h5")

    return {
        "model_name": "GRU",
        "type_model": "Main Model",
        "metrics": {
            "accuracy": float(accuracy),  
            "recall": float(recall),     
            "f1_score": float(f1),
            "precision": float(precision),           
        }
    }
```

No código, é possível ver um exemplo da função principal, chamada `execute`, que é a função utilizada pelo Orquestrador. Neste caso, o script é responsável por treinar um modelo de rede neural recorrente (GRU) para classificação de falhas em veículos. O modelo é treinado com base nos dados fornecidos no DataFrame `df_merged`, e ao final da execução, o modelo é salvo em um arquivo `model.h5` e as métricas de desempenho são retornadas.

É absolutamente necessário que o nome da função seja `execute`, pois é o nome que o Orquestrador procura para executar o script. Caso o nome da função seja algo diferente disto, o Orquestrador não conseguirá executar o script.

### **3.1.3** - Execução do Orquestrador

Atualmente, o Orquestrador já está integrado no Backend, como dito na parte da documentação relacionada ao mesmo. Para executar o mesmo, basta bater ou na rota `/api/train/` ou `/api/train/retrain` do Backend, passando o DF de falhas como parâmetro. O Orquestrador irá executar o pipeline de acordo com as etapas definidas, processando os DataFrames e scripts conforme necessário.

É necessário ter o DF de resultados dentro da pasta pipeline, tanto quanto o JSON de configuração do pipeline. O Orquestrador irá processar o pipeline de acordo com as etapas definidas, processando os DataFrames e scripts conforme necessário.

---

## **3.2** - Fluxo de Processos do Orquestrador

Nesta seção, apresentamos uma série de diagramas que ilustram o fluxo de processos de análise, consulta, e execução de receitas no orquestrador. Eles mostram como as diferentes partes do sistema, como o **FrontEnd**, **BackEnd**, **MongoDB**, e **Volkswagen**, interagem para processar dados e realizar análises.

### **3.2.1** - Análise de Modelos
O diagrama abaixo descreve o fluxo de trabalho relacionado à análise de modelos pelo orquestrador. Neste cenário, o **FrontEnd** inicia o processo ao solicitar uma análise dos modelos disponíveis ao **BackEnd**. O **BackEnd** atua como um intermediário, conectando-se ao **MongoDB** para coletar dados de testes recentes e iniciar o processo de análise.

Durante a análise, o **BackEnd** executa uma série de operações em loop, processando os modelos disponíveis e comparando os resultados em tempo real. Essa etapa é crítica para garantir que a performance dos modelos seja constantemente verificada e aprimorada com base em novos dados. Ao finalizar o processo de análise, os resultados são enviados de volta ao **FrontEnd**, que os apresenta ao usuário final.

![Análise de Modelos](/img/dia1.png)

Neste fluxo, o **MongoDB** serve como a principal fonte de dados para a análise, enquanto o **BackEnd** realiza o processamento pesado de comparar e analisar os modelos em um loop contínuo. O **FrontEnd** permanece responsável por iniciar a análise e apresentar os resultados aos usuários, mantendo uma interface amigável e informativa.

### **3.2.2** - Consulta de KNR
O segundo diagrama ilustra o fluxo de consulta de KNR (número identificador único para cada veículo). Quando um usuário deseja verificar uma previsão associada a um veículo específico, o **FrontEnd** envia uma solicitação ao **BackEnd** para obter informações sobre o KNR desejado. O **BackEnd**, por sua vez, consulta a predição correspondente ao KNR no banco de dados **MongoDB**.

Uma vez que os dados de predição são recuperados, eles são enviados de volta ao **FrontEnd**, que então exibe os resultados ao usuário. Este processo é importante para fornecer informações rápidas e precisas sobre o status de um veículo específico, permitindo que decisões sejam tomadas com base em dados atualizados.

![Consulta de KNR](/img/dia2.png)

Este fluxo reflete a capacidade do sistema de fornecer dados em tempo real. A comunicação eficiente entre o **FrontEnd** e o **BackEnd** é fundamental para manter uma experiência de usuário responsiva. O **MongoDB** atua como a base de armazenamento que contém todas as previsões associadas aos diferentes KNRs, tornando-se uma peça central para consultas rápidas e precisas.

### **3.2.3** - Fluxo de Execução de Receita com Volkswagen
O terceiro diagrama mostra um fluxo mais complexo, envolvendo o processamento de dados da Volkswagen e a execução de receitas para análises detalhadas. O processo se inicia quando a Volkswagen envia um arquivo `.csv` contendo dados de KNR ao **BackEnd**. Esses dados são fundamentais para que o sistema possa identificar e analisar cada veículo.

Uma vez que o **BackEnd** recebe o arquivo, ele salva as informações de KNR no **MongoDB** para que sejam processadas posteriormente. Em seguida, ele consulta a receita ativa associada ao modelo, buscando informações no banco de dados para coletar a lógica de processamento necessária para esse fluxo. A receita ativa é um conjunto de instruções de processamento que determina como os dados do KNR serão tratados e analisados.

Para executar essa receita, o **BackEnd** coleta o script necessário diretamente do **GridFS**. O **GridFS** funciona como um sistema de arquivos armazenado no **MongoDB**, contendo scripts e outros arquivos essenciais para o processo de análise. Uma vez coletado, o script é executado em loop pelo **BackEnd** até que todo o processamento necessário seja concluído. Finalmente, os resultados da predição são salvos no **MongoDB**, completando o ciclo de processamento.

![Fluxo de Execução](/img/dia3.png)

Este diagrama destaca a importância de uma integração fluida entre todas as partes do sistema. A comunicação com a Volkswagen fornece os dados necessários para o início do processamento, enquanto o **MongoDB** e o **GridFS** atuam como repositórios centrais para armazenamento de dados e scripts. O **BackEnd** executa o processamento em tempo real, garantindo que a análise dos dados ocorra de forma rápida e eficiente.

Esses diagramas fornecem uma visão geral de como o **Orchestrator** coordena as diferentes etapas de análise, consulta, e processamento de dados. Eles mostram as interações e o fluxo de informações entre o **FrontEnd**, **BackEnd**, **MongoDB**, e outras entidades externas, destacando a flexibilidade e a capacidade de processamento dinâmico oferecidas pelo sistema.

## **4.1** - Conclusão

O Orquestrador é uma solução robusta e flexível para gerenciar a execução de pipelines de scripts Python, proporcionando uma integração eficiente entre o processamento de dados, o treinamento de modelos, e o armazenamento de logs. Sua estrutura modular permite a execução sequencial de etapas, onde scripts são carregados dinamicamente do GridFS, executados, e seus resultados manipulados em DataFrames. Dessa forma, o orquestrador garante uma abordagem dinâmica e escalável para o processamento de dados, ao mesmo tempo em que possibilita o fácil monitoramento e análise de logs em tempo real.

Com a configuração de pipeline definida por meio de um JSON, o Orquestrador pode ser adaptado a diferentes cenários de processamento de dados, seja para treinar modelos de Machine Learning, transformar dados ou executar processos complexos de forma automatizada. A separação de etapas facilita a manutenção e permite uma rápida implementação de novas funcionalidades, promovendo uma experiência flexível tanto para desenvolvedores quanto para operadores do sistema.

Por fim, a arquitetura do Orquestrador abre caminho para futuras melhorias, como a integração completa com o GridFS para manipulação de scripts e DataFrames remotamente, e a otimização do armazenamento de logs no MongoDB. Essas evoluções tornarão o sistema ainda mais modular e escalável, permitindo a fácil expansão para atender às necessidades de projetos em crescimento e operações cada vez mais complexas.