# Primeiro modelo de predição
# 1. Método CRISP-DM

O CRISP-DM, acrônimo para "CRoss Industry Standard Process for Data Mining", é um método iterativo utilizado nos processos de ciência de dados. Seis etapas compõem esse método que, aliado a um time Agile, traz expressiva eficiência para o desenvolvimento de um projeto que envolve manusear, analisar e inferir com dados[1].

**As fases do CRISP-DM são:**
1. **Entendimento do negócio(Business Understanding):** levantar as necessidades do cliente, bem como elencar os objetivos do projeto. Trata-se de uma fase importante, não podendo ser tratada com displicência;
2. **Entendimento dos dados(Data Understanding):** tem enfoque em identificar, coletar e analisar os dados que podem ser úteis para alcançar os objetivos do projeto;
3. **Preparação dos dados(Data Preparation):** uma vez identificados os dados que podem ser de valia para o projeto, é importante prepará-los. Isso inclui fazer a limpeza necessária, integrar diferentes tabelas e até formatar o conteúdo de algumas colunas;
4. **Modelagem(Modeling):** essa é a fase em que diferentes modelos existentes são testados com o dataset do projeto. Isso implica dividir de antemão os dados em treino, teste e validação;
5. **Avaliação do modelo(Evaluation):** aqui, o desempenho do modelo é avaliado utilizando métricas como acurácia, precisão e recall. A análise verifica se o modelo alcança os objetivos definidos e se está pronto para ser implementado;
6. Deploy do modelo(Deployment): nessa fase, o modelo é colocado em produção em um ambiente real, integrando-o aos sistemas existentes.

<div align="center">
  
**Fases do CRISP-DM**

![Fases do CRISP-DM](/img/CRISP-DM.png)

**Fonte:** Data Science Process Alliance

</div>

Essa padronização de processos de mineração de dados CRISP-DM foi elegida para ser implementada neste projeto por alguns motivos. Primeiro, porque trata-se de uma padronização que estrutura bem os processos, o que vai ser importante para o desenvolvimento do modelo preditivo que atenda adequadamente as necessidades da Volkswagen. Além disso, esse método dá enfoque na qualidade dos dados, aprimorada sempre que necessário por meio do caráter iterativo do CRISP-DM. Ele também traz bastante flexibilidade, por exemplo permitindo adaptar o projeto à medida que novas ideias de melhoria surgem.

# 2. Da implementação do CRISP-DM no projeto

### 2.1 Entendimento do negócio
O primeiro passo para desenvolver o modelo preditivo de otimização das inspeções de qualidade durante os testes de rodagem de veículos na Volkswagen é compreender profundamente as necessidades e expectativas do negócio. Esta fase é crucial para garantir que o projeto se alinhe aos objetivos estratégicos da empresa, abordando as prioridades mais relevantes e oferecendo soluções práticas.

Desse modo, entre os objetivos do projeto e as necessidades do cliente, figuram:
1. Melhoria na Detecção de Falhas: o modelo preditivo deve aumentar a precisão na identificação de falhas durante os testes de rodagem.

2. Otimização dos Recursos: reduzir o tempo e os recursos necessários para conduzir testes de rodagem, permitindo que mais veículos passem pelo processo de forma eficiente.

3. Redução de Custos: minimizar os custos associados a defeitos não detectados no processo de fabricação, evitando recalls e garantindo que os veículos saiam da linha de produção sem falhas.

4. Satisfação do Cliente: garantir que os veículos entregues ao consumidor final estejam em perfeitas condições, aumentando a confiabilidade e a reputação da Volkswagen.

Esses pontos norteiam todo o desenvolvimento do projeto. Sem levá-los em consideração, não é possível exprimir um sentido para as tarefas desenvolvidas nas próximas fases. Por isso que essa fase de entendimento do negócio deve ser revisitada ao longo do desenvolvimento, em especial antes de colocar o modelo em produção em um ambiente real.

### 2.2 Entendimento dos dados
Aqui, o objetivo é identificar, coletar e analisar dados para construir e treinar o modelo preditivo, garantindo que as informações sejam relevantes e de alta qualidade.

Assim, foram levantadas fontes de dados na Volkswagen sobre fabricação e testes, incluindo históricos de falhas, inspeções, e condições operacionais.

Após isso, o parceiro então disponibilizou tabelas com detalhes do status dos veículos, tempo em cada etapa, e falhas identificadas contidas em duas tabelas principais: Falhas e Resultados.

<div align="center">
  
**Primeiros registros da tabela Falhas**

![Fases do CRISP-DM](/img/tabela-falhas.png)

**Fonte:** Próprios autores

</div>



<div align="center">
  
**Primeiros registros da tabela Resultados**

![Fases do CRISP-DM](/img/tabela-resultados.png)

**Fonte:** Próprios autores

</div>

Entendendo como os dados estavam organizados e como poderiam ser relacionados, é decidido que as colunas KNR e FALHA da tabela Falhas serão utilizadas, enquanto UNIT, VALUE_ID e VALUE da tabela Resultados serão descartadas. Esses dados são cruciais para a detecção de falhas. Para mais informações, acessar a seção [Viabilidade Técnica](../Requisitos_de_Viabilidade_Tecnica/Proposta_Geral_do_Sistema.md)

### 2.3 Preparação dos dados
Nesta fase, os dados foram preparados para garantir que estivessem prontos para a análise e construção do modelo preditivo.

Primeiro, os dados foram integrados em uma única tabela. As colunas de data foram convertidas para o formato datetime do Pandas para facilitar o manuseio e análise temporal. Em seguida, as colunas desnecessárias para a predição foram removidas, e os dados foram salvos no formato "parquet" para otimizar a velocidade de leitura e processamento.

```
# Transformando data em datetime do pandas

df['DATA'] = pd.to_datetime(df['DATA'], errors='coerce')
```

```
# Salvando os dados em "parquet" é mais rápido para leitura

df_resultados.to_parquet('../data/df_resultados.parquet', index=False)
df_resultados2.to_parquet('../data/df_resultados2.parquet', index=False)
df_resultados3.to_parquet('../data/df_resultados3.parquet', index=False)
```

Os DataFrames de resultados foram combinados em um único DataFrame maior. No caso do DataFrame de falhas, as entradas da coluna de falhas foram convertidas para letras maiúsculas para padronização. Também foram removidas as linhas com valores duplicados na coluna KNR, e os valores da coluna de falhas foram transformados em 1, facilitando a identificação das falhas.

Por fim, os DataFrames de falhas e resultados foram combinados em um único DataFrame por meio de um merge, preparando os dados para o treinamento do modelo preditivo.

```
# Realizando o merge dos dataframes df_falhas e final_df com base na coluna 'KNR'
merged_df = pd.merge(final_df, df_falhas_unique, on='KNR', how='left')
```

Para ler um texto complementar da explicação, acessar seção [Viabilidade Técnica](../Requisitos_de_Viabilidade_Tecnica/Proposta_Geral_do_Sistema.md), bem como o notebook python na pasta `src`.

### 2.4 Modelagem
Para esta etapa, o modelo preditivo foi construído e treinado utilizando o algoritmo K-Nearest Neighbors (KNN), escolhido por sua eficácia em problemas de classificação.

Esse algoritmo classifica novos dados com base nas classes dos vizinhos mais próximos, alinhando-se ao objetivo de identificar rapidamente o tipo de inspeção necessária, por exemplo

Inicialmente, foi realizada a normalização. O KNN é sensível à escala das variáveis, portanto, garantir que todas as características contribuam igualmente para a distância calculada é crucial.

```
# Selecionando apenas as colunas específicas para normalização
cols_to_normalize = ['ID1NAME','ID1SOK', 'ID1SNOK', 'ID1DATA', 'ID2NAME', 'ID2SOK', 'ID2SNOK', 'ID2DATA', 'ID718NAME', 'ID718SOK', 'ID718SNOK', 'ID718DATA']

# Inicializando o MinMaxScaler
scaler = MinMaxScaler()

# Aplicando a normalização
merged_df[cols_to_normalize] = scaler.fit_transform(merged_df[cols_to_normalize])
```

Após a normalização, os dados foram divididos em conjuntos de treinamento e teste. Utilizou-se uma divisão de 80% para treinamento e 20% para teste. Isso garante que o modelo aprenda com um conjunto robusto de dados e seja avaliado com dados não vistos.

```
# Separando as features (X) e o target (y)
X = merged_df.drop(columns=['FALHA', 'KNR'])  # 'KNR' é apenas um identificador, então deve ser removido
y = merged_df['FALHA']

# Separar os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

### 2.5 Avaliação do modelo
Por fim, o desempenho do modelo K-Nearest Neighbors (KNN) foi avaliado para garantir que atendesse aos requisitos estabelecidos.

Para medir a eficácia do modelo, foi escolhida como a principal métrica a acurácia, pois é uma medida direta da proporção de previsões corretas entre todas as previsões feitas.

Em um contexto de detecção de falhas, como é o caso desse projeto, essa métrica é adequada porque reflete a capacidade do modelo de identificar corretamente os veículos que precisam de inspeção.

A acurácia obtida foi:
```
Acurácia no Treinamento: 0.8882140678999797
Acurácia no Teste: 0.8575058440898465
```

<div align="center">
  
**Matriz de confusão**

![Fases do CRISP-DM](/img/confusion-matrix.png)

**Fonte:** Próprios autores

</div>

Além disso, para agregar a avaliação do modelo, junto com a acurácia foi plotada uma matriz de confusão. Ela fornece uma visão geral das previsões do modelo, comparando as classes previstas com as classes reais. Sua utilização se dá principalmente por conseguir identificar onde o modelo comete erros, distinguindo entre falsos positivos e falsos negativos.

# Bibliografia
[1]: DATA SCIENCE PROCESS ALLIANCE. What is CRISP DM?. Disponível em: https://www.datascience-pm.com/crisp-dm-2/. Acesso em: 12 ago. 2024.
