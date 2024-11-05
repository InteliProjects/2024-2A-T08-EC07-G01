---
title: "Modelos da Base de Dados"
sidebar_position: 1
---

## **0.1** Introdução

A base de dados MongoDB é amplamente utilizada por sua flexibilidade no armazenamento de dados e escalabilidade. Estruturada em formato de documentos, ela permite que os dados sejam armazenados em coleções que, por sua vez, contêm registros chamados de documentos. Cada coleção pode armazenar dados de diferentes tipos, proporcionando uma estrutura não relacional eficiente, especialmente para sistemas que exigem grandes volumes de informações e acesso rápido. No nosso contexto, utilizamos três coleções principais, cada uma com uma função específica e bem definida.

:::tip Info

Uma coleção no MongoDB é equivalente a uma tabela em um banco de dados relacional. Cada coleção contém documentos, que são registros individuais que armazenam os dados.
:::

Essas três coleções ou modelos desempenham papéis distintos dentro de nossa aplicação. A primeira é responsável pelo armazenamento dos dados de cada KNR `inputados` no sistema. A segunda coleção tem a função de gerenciar os modelos de inteligência artifical criados, afim de manter rastreabilidade. Por fim, a terceira coleção lida com as respostas geradas pelo modelo de IA sobre os dados dos KNRs `inputados`, armazenando-as para futuras consultas.

Entender como cada uma dessas coleções opera é fundamental para a gestão e manutenção do banco de dados. Compreender as características únicas de cada uma delas permite otimizar o desempenho da aplicação e garantir que os dados sejam processados de maneira eficiente e segura. Neste documento, serão abordadas as especificidades de cada coleção, suas estruturas e as principais funcionalidades que oferecem ao sistema como um todo.

## **1.1** Estrutura das Coleções

Como dito anteriormente, nosso banco de dados MongoDB é composto por três coleções principais: **KNR**, **Model** e **Prediction**. Cada uma dessas coleções tem uma função fundamental dentro do sistema, armazenando informações necessárias para o gerenciamento, análise e previsão de dados. A seguir, detalharemos a estrutura de cada coleção, suas funções e exemplos de documentos em formato JSON.

## **2.1** Coleção KNR

A coleção **KNR** armazena dados sobre objetos individuais que estão sendo monitorados e analisados dentro do sistema. No contexto deste projeto, os objetos são veículos produzidos pela Volkswagen em meio a linha de produção. Cada documento nesta coleção contém informações que identificam o objeto e suas características específicas.

:::tip Info
Para mais informações a respeito do projeto em geral, acesse a documentação presente na [Intro](../../intro.md).
:::

### **2.1.1** Estrutura dos Campos

- **KNR (str):** Identificação do veículo.

- **NAME (str):** Identificação do resultado no sistema.

- **ID (int):** É a identificação de qual grupo aquele resultado pertence.
    - 1: Máquinas. ( Fluídos, Regulagem de freio e teste de pedal ).
    - 2: Parafusamento. ( Torques e ângulos dos apertos realizados ).
    - 718: Eletrônicos. ( Testes de componentes elétricos e eletrônicos ).

- **STATUS (int):** O status do veículo, se tem ou não falhas
    - 10: Sem falhas.
    - 13: Com falhas.

- **UNIT (str):** Tipo do valor. ( VALUE ).
    - Grad: ângulo.
	- Nm: torque.
	- Deg: ângulo.


- **VALUE_ID (str):** É um sub resultado, cada resultado NAME pode ter vários parafusos em sua composição.

- **VALUE (str):** É o valor resultante daquele aperto (Nm), graus ( Grad, Deg ) ou outros resultados 
eletrônicos. 

- **DATA (str):** Data de recebimento deste resultado.

Segue abaixo uma imagem representando a estrutura da coleção **KNR**:

![Estrutura da coleção KNR](/img/knr.png)

### **2.1.2** Exemplo do JSON da coleção

Segue abaixo um exemplo de documento JSON que poderia ser armazenado na coleção **KNR**:

```json
{
    "KNR": "VW-0001",
    "NAME": "Torque",
    "ID": 2,
    "STATUS": 10,
    "UNIT": "Nm",
    "VALUE_ID": "VW-0001-01",
    "VALUE": 10.5,
    "DATA": "2021-10-01"
}
```

:::warning Atenção
Os dados acima são meramente ilustrativos e não fazem parte da base de dados da Volskwagen.
:::

Este exemplo, descreve um documento que armazena informações sobre um veículo específico, identificado como `VW-0001`. O documento registra um resultado de torque de 10.5 Nm, sem falhas, em uma data específica. Cada documento na coleção **KNR** segue um formato semelhante, com campos específicos que armazenam informações sobre o veículo e os resultados obtidos.

## **3.1** Coleção Model

A coleção Model é utilizada para armazenar metadados e o desempenho dos modelos de machine learning que são utilizados nas previsões. Cada modelo é responsável por fazer previsões com base nos dados dos objetos presentes na coleção KNR. Essa coleção contém as métricas de desempenho, o caminho para o armazenamento do modelo, além de outras informações relevantes para rastreamento e gerenciamento dos modelos.

### **3.1.1** Estrutura dos Campos

- **model_name (str):** Nome único que identifica o modelo de machine learning.

- **type_model(str):** Tipo do modelo treinado, se é modelo de classificação ou falha. ( Ex: 1,2,3 )

- **gridfs_path (str):** Caminho onde o modelo está armazenado no `GridFS` (sistema de armazenamento de arquivos do MongoDB).

- **recipe_path (str):** Caminho para a receita ou configuração usada para treinar o modelo.

- **accuracy (float):** Acurácia do modelo, representando a porcentagem de previsões corretas.

- **precision (float):** Precisão do modelo, indicando a proporção de verdadeiros positivos em relação aos resultados positivos.

- **recall (float):** Recall do modelo, mostrando a capacidade do modelo de identificar verdadeiros positivos em relação aos casos reais positivos.

- **f1_score (float):** F1 Score, uma métrica que combina precisão e recall.

- **last_used (datetime):** Data e hora da última vez que o modelo foi utilizado

Segue abaixo uma imagem representando a estrutura da coleção **Model**:

![Estrutura da coleção Model](/img/model.png)

### **3.1.2** Exemplo do JSON da coleção

Segue abaixo um exemplo de documento JSON que poderia ser armazenado na coleção **Model**:

```json
{
    "model_name": "LSTM",
    "gridfs_path": "models/LSTM.pkl",
    "recipe_path": "recipes/LSTM.json",
    "accuracy": 0.85,
    "precision": 0.90,
    "recall": 0.80,
    "f1_score": 0.85,
    "last_used": "2021-10-01T12:00:00"
}
```

O documento acima descreve um modelo de machine learning chamado `LSTM`, que foi treinado com uma acurácia de 85%. O modelo foi treinado com base em uma receita armazenada em `recipes/LSTM.json` e o modelo em si está armazenado em `models/LSTM.pkl`. Além disso, o documento registra as métricas de precisão, recall e F1 Score do modelo, bem como a data e hora da última vez que o modelo foi utilizado.

## **4.1** Coleção Prediction

A coleção **Prediction** armazena os resultados das previsões feitas pelos modelos da coleção **Model**. Cada documento representa uma previsão realizada para um determinado objeto (identificado por **KNR**) e inclui os códigos de falha previstos, os códigos de falha reais e os testes indicados para validar a previsão.

### **4.1.1** Estrutura dos Campos

- **KNR (str):** Identificador do veículo.

- **predicted_fail_codes (List[str]):** Lista de códigos de falha previstos pelo modelo.

- **real_fail_codes (List[str]):** Lista de códigos de falha reais que foram detectados após a previsão.

- **indicated_test (List[str]):** Lista de testes recomendados ou indicados pelo modelo para validar ou investigar as previsões.

Segue abaixo uma imagem representando a estrutura da coleção **Prediction**:

![Estrutura da coleção Prediction](/img/prediction.png)

### **4.1.2** Exemplo do JSON da coleção

Segue abaixo um exemplo de documento JSON que poderia ser armazenado na coleção **Prediction**:

```json
{
    "KNR": "VW-0001",
    "predicted_fail_codes": ["P001", "P002"],
    "real_fail_codes": ["P001"],
    "indicated_test": ["Teste A", "Teste B"]
}
```

O documento acima descreve uma previsão feita para o veículo `VW-0001`. O modelo previu que os códigos de falha `P001` e `P002` seriam detectados no veículo, mas apenas o código `P001` foi detectado na realidade. O modelo indicou os testes `Teste A` e `Teste B` para validar a previsão e investigar a presença do código de falha `P002`.

## **5.1** Conclusão

A estrutura da nossa base de dados MongoDB, composta pelas coleções **KNR**, **Model** e **Prediction**, permite uma gestão eficiente dos objetos, modelos e previsões dentro do sistema. A coleção **KNR** mantém o histórico de cada objeto, a coleção **Model** armazena os metadados e métricas dos modelos preditivos, enquanto a coleção **Prediction** guarda os resultados das previsões, facilitando a comparação entre falhas previstas e reais.

Essa organização não só garante a integridade dos dados como também oferece flexibilidade e escalabilidade, permitindo que o sistema se adapte conforme novos modelos são desenvolvidos e novas previsões são realizadas. Através desse framework, podemos garantir que o desempenho dos modelos seja monitorado continuamente e que as previsões sejam refinadas de acordo com os dados reais.