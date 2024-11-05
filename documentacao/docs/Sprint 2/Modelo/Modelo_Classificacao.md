# Modelo de Classificação por S_Group_ID

## Ideia Inicial 

Após a Sprint 1 a Volkswagen enviou uma tabela de falhas contendo a coluna S_GROUP_ID, a qual representa a classe de um determinado tipo de falha. Com isso, o grupo percebeu a oportunidade de prever tanto se haverá falha, como em que categoria de falha ela se encaixaria. Dessa forma, foram discutidas diferentes abordagens para a realização do problema. A primeira solução que o grupo imaginou foi a criação de dois modelos, um prevendo o acontecimento de falhas e outro que preveria o S_GROUP_ID, caso o resultado do primeiro seja de falha.

Todavia, essa ideia foi descartada após perceber que seria complexo acertar exatamente a classe que a falha pertenceria, além disso, um mesmo KNR pode ter mais de um tipo de falha, algo que esse modelo não conseguiria classificar.

## Modelo

Para conseguir prever de maneira correta e abranger todos os tipos de falhas possíveis, o grupo optou por agrupar as falhas por KNR e utilizar a técnica do OneHotEncode. Além da criação de um modelo para cada coluna gerada. Dessa maneira, para cada valor único do S_GROUP_ID há uma coluna com valores entre 0 e o número de registros de falha daquele S_Group_ID naquele KNR. Portanto, esse processamento foi feito para poder haver vários modelos, com cada modelo tendo como alvo uma coluna diferente. Assim, possibilitaria prever os diferentes tipos de falha existentes, além de possivelmente garantir mais estabilidade nas previsões.

## Pré-processamento 

Como tratamento inicial, utilizou-se de comandos como o `describe`, `info`, entre outros para compreender a situação do dataframe. Assim, foram removidas as linhas com valores nulos, resultando numa diminuição de aproximadamente 0,2% dos dados. 

### S_GROUP_ID 

Na tabela enviada, a variável S_GROUP_ID possui 19 registros únicos, porém diversos deles eram idênticos, mas com diferenças de tipo. Dessa forma o grupo visou tratar e colocar todos em `lowercase` para conseguir ter um melhor controle da tabela.

![Valores únicos S_Group_ID](/img/s_group_id.png)

Além disso, pela pouca quantidade e destoar do resto das informações, foram removidas todas as linhas que possuiam "MultiValue" como valor atribuído.


### Motor 

Foram removidos valores que constavam como apenas tabs ou espaços, sem trazer valor verdadeiro na coluna "Motor". 

### Remoção de Colunas 

Para a criação de uma versão inicial do modelo, foram removidas do dataframe as colunas: "Falha", "Modelo", "Estação" e "Halle". Suas justificativas a seguir:

- "Falha" não é importante por conter uma especificação da falha que ocorreu, de maneira mais específica do que o modelo planeja prever. Sendo assim, o modelo não pode ter acesso à informação de qual falha ocorreu visto que essa coluna descreve algo que ainda não é conhecido. 

- "Modelo" deve ser descartada, devido a sua repetição de valores, sendo todos do tipo "T-cross".

- "Estação" não será utilizada porque antes da falha ser identificada, ainda não sabemos em qual estação o carro está.
  
- "Halle" não será utilizada porque, assim como a estação, ainda não sabemos em qual halle o carro está.

- Por fim, "Usuário" que cadastrou a falha é irrelevante para a predição, visto que não tem impacto no output.

## União de tabelas

Para que pudesse dar início aos modelos, era necessário unir a tabela de falhas com a de resultados, através do agrupamento por KNR. Dessa forma, foram utilizado os seguintes códigos:

```python
# Agrupar por KNR, mantendo a primeira ocorrência de COR e MOTOR (já que o carro é o mesmo então essas informações se repetem em todos os registros) e somando as colunas S_GROUP_ID, para termos a noção de quantas repeitções de cada tipo de falha ocorreram para cada carro.

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

# Exibir o DataFrame agrupado
grouped_df.head()
``` 

Após isso, foi feito o merge do dataframe de falhas com o dataframe de resultados [já tratado no arquivo `main.ipynb`](../../Sprint%201/Primeiro%20Modelo%20de%20Predição/modelo.md)
