## Estudo da viabilidade

A indústria automotiva está cada vez mais orientada por dados e inteligência artificial, com o objetivo de otimizar processos e melhorar a qualidade dos veículos produzidos. Nesse contexto, a Volkswagen busca inovar em seus processos de controle de qualidade, propondo o desenvolvimento de um modelo preditivo capaz de avaliar, de maneira antecipada, a necessidade de testes de rodagem nos veículos logo após saírem da linha de produção.

Este estudo de viabilidade tem como objetivo principal avaliar se a equipe de desenvolvimento dispõe dos recursos e insumos necessários para construir um modelo robusto e eficiente. Tal modelo preditivo visa identificar a probabilidade de falhas potenciais nos veículos, permitindo a tomada de decisões mais assertivas quanto à necessidade de testes adicionais, garantindo assim a qualidade dos produtos entregues ao consumidor final.

A seguir, será apresentada uma análise detalhada dos dados disponíveis e das variáveis *(features)* selecionadas para treinar o modelo, com o intuito de verificar sua capacidade preditiva e precisão em identificar possíveis falhas.

## Análise exploratória dos dados

Para a primeira versão do modelo preditivo, as bibliotecas utilizadas foram o [pandas](https://pandas.pydata.org/docs/), o [numpy](https://numpy.org/), e o [sklearn](https://scikit-learn.org/stable/). O parceiro disponibilizou uma variedade de tabelas, entre elas as tabelas de resultados (que contém atualizações de status do carro, quanto tempo ele passou em cada procedimento, entre outras coisas que descrevem o que aconteceu ao longo da linha de produção) e de falhas (que contém as falhas encontradas em cada carro). Essas tabelas que serão utilizadas para a construção da nossa solução, pois as informações do que ocorreu na linha de produção impactarão diretamente nas falhas que o modelo encontrará.

Para uma análise mais detalhada do código utilizado para a exploração dos dados, é possível acessar o notebook na pasta **notebooks**, que está localizado dentro da pasta **src** do nosso [GitHub](https://github.com/Inteli-College/2024-2A-T08-EC07-G01/blob/main/src/notebooks/main.ipynb), com o nome **main.ipynb**. 

### Importação das bibliotecas

Primeiramente, é realizada a importação das bibliotecas mencionadas acima, que serão utilizadas para auxiliar a modificação e vizualização dos dados, a fim de melhorar os inputs para o modelo processar. 

### Inicializar os dados e arrumar erros de conversão

Depois, as tabelas são carregadas, e há a necessidade (no caso da tabela de falhas) de arrumar os indexs pois ao converter de xlsx (formato que o parceiro disponibilizou) para csv, algumas colunas com o nome "unnamed" surgem, pois o index não é reconhecido. 

### Preparação dos dados

- **Remoção de linhas com dados nulos:** Como há uma grande quantidade de dados, o drop (método que funciona como um "deletar") das linhas com dados nulos não representa grande perda.

- **Conversão de csv para parquet:** Para um processamento mais rápido, os dados foram convertidos para formato *parquet.

- **Drop de colunas que não serão usadas para treinar o modelo:** Na tabela **Resultados**, as colunas 'UNIT', 'VALUE_ID' e 'VALUE' são apagadas, para diminuir o tamanho da tabela e assim dando mais ênfase para as *features* mais importantes, como o 'KNR' (que é um código que identifica cada carro), o 'STATUS' (que avalia se o carro está "ok" ou "não ok" naquele checkpoint), e a 'DATA' (que representa o momento em que aquela avaliação foi feita). 
Já na tabela de **Falhas**, as colunas retiradas foram todas exceto as que tem os KNRs (para identificar os carros) e as descrições das falhas (com mais de 2000 tipos de falhas únicas).
Importante ressaltar que o KNR não será utilizado para treinar o modelo posteriormente, mas será mantido por enquanto apenas para facilitar a junção das tabelas, tornando possível reunir numa só linha informações a respeito de um mesmo carro.

#### Mudanças nas tabelas de resultados

- **Concatenar tabelas de resultados:** Para termos mais volume de dados, juntamos duas tabelas de resultados referentes a dois meses do ano de 2023.

- **Converter a coluna de datas de *object* para o *datetime* do pandas:** Ao usar a função `describe` do pandas, foi mostrado que todos as colunas estavam com o tipo *object*, o que para uma análise temporal não é a forma mais fácil de se trabalhar. Para facilitar os cálculos temporais usando o pandas, convertemos o tipo da coluna 'DATA' para *datetime*.

- **Feature engineering:** Para facilitar a identificação de padrões entre os carros que possuem falha, houve-se a necessidade de criação de novas *features* para melhor representar nosso conjunto de dados. Na tabela de Resultados, haviam múltiplas linhas de um mesmo KNR (carro), com diferentes status e entradas. Logo, o primeiro desafio foi juntar todas as informações de um mesmo carro numa só linha, modificando a tabela.
Dessa forma, a tabela Resultados ficou com as seguintes features:

    **- KNR:** Como mencionado anteriormente, é o código único que cada carro possui.

    **- ID1NAME, ID2NAME, ID718NAME:** Há três tipos diferentes de IDs, sendo cada um deles uma representação de um grupo da linha de produção, sendo o 1 para as máquinas, 2 para o parafusamento e 718 para os eletrônicos. As colunas 'NAME' nesse caso representam a quantidade de ocorrências de um mesmo ID, ou seja, se há cinco aparições do ID1 em um certo carro, o ID1NAME será 5.

    **- ID1SOK,ID2SOK, ID718SOK:** Para cada tipo de ID, as colunas 'SOK' representam quantos resultados estão ok, ou seja, bons.

    **- ID1SNOK, ID2SNOK, ID718SNOK:** De maneira semalhante (porém oposta) às colunas citadas acima, as colunas 'SNOK' representam a quantidade de IDs que não estão bons, ou seja, que tiveram alguma intercorrência.

    **- ID1DATA, ID2DATA, ID718DATA:** Anteriormente realizamos a conversão da coluna 'DATA' para datetime justamente para facilitar essa visualização - nessas colunas, utilizamos o pandas para calcular o tempo gasto em cada ID, ou seja, a diferença de tempo entre o último registro e o primeiro. Dessa forma, conseguimos mapear se o tempo gasto interfere numa maior quantidade de falhas (ou não).

Com essa manipulação dos dados, conseguimos com apenas uma linha ter uma noção de todos os procedimentos da linha de produção de um carro, sem precisar olhar para vários registros.

#### Mudanças na tabela de falhas

Um desafio que enfrentamos ao observar a tabela de Falhas é o fato de termos encontrado mais de 2.000 falhas únicas, o que dificulta o desenvolvimento de um modelo classificatório mais específico. Por essa razão, na primeira Sprint, optamos por focar primeiramente numa resposta binária: se há uma grande possibilidade de falha (True), ou não (False). Por essa razão, como o tipo de falha especificamente não era o nosso alvo, fizemos algumas modificações na tabela que serão explicadas a seguir:

- **Remover os KNRs repetidos:**  Um mesmo carro pode apresentar múltiplos tipos de falhas. Todavia, como decidimos inicialmente apenas apontar a possibilidade de falha de forma geral, não importa quantos tipos um carro teve, e sim se ele teve ou não. Por essa razão, removemos todas as linhas que possuíam KNRs repetidos.

- **Mudar as especificações das falhas para 1:** Como todos os carros da tabela de Falhas apresentam falhas, substituímos a coluna que especificava a mesma por 1, representando o nosso "True". Dessa forma, ao juntar com a tabela de Resultados, todos os KNRs que possuem falhas irão ter 1, enquanto os que não aparecerem na tabela terão 0.

#### Juntando a tabela de resultados com a de falhas

Após as manipulações nas duas tabelas, chegou o momento de juntar ambas. 

- **Representar as falhas de forma binária:** Como explicado anteriormente, todos os carros que aparecem na tabela de falhas possuem 1 na coluna 'FALHA', o que ao juntar com a tabela de Resultados deixa espaços vazios, que representam os carros que não tiveram problemas. Esses espaços vazios foram preenchidos com 0, para representar a falta de falhas.

- **Normalização dos dados:** Para melhorar a performance do modelo, também aplicamos o método de normalizar os dados, ou seja, padronizar todos as informações numéricas entre 0 e 1.

- **Drop das colunas KNR e Falha (que é o target):** Após finalizar todas essas manipulações com os dados, finalmente removemos as colunas 'KNR' (que foi mantida apenas para a junção das tabelas) e 'FALHA', que é a nossa feature alvo (ou seja, é o que queremos que o nosso modelo preveja).

#### Primeiro modelo utilizado 

O primeiro modelo que utilizamos foi um **KNN (K-Nearest Neighbors)**, que é um modelo de aprendizado supervisionado de classificação. Esse modelo separa as entradas de aprendizado em grupos (clusters) e avalia em qual grupo uma determinada entrada melhor pertence. Avaliamos que seria um bom modelo para começar justamente pela característica de identificar padrões e agrupá-los, podendo observar se o processo de produção de um carro o deixa mais próximo do grupo que possui falhas ou não.

- **Métricas avaliadas:** Nesse primeiro momento, avaliamos apenas a acucária, que é uma medida da proporção de todas as previsões corretas (verdadeiros positivos e verdadeiros negativos), ou seja, queremos apenas avaliar o quanto o modelo está acertando. Os números que obtivemos foram:

``` 
Acurácia do treinamento : 88%

Acurácia do teste 85.7% 
```

Com esses dados podemos inferir, por exemplo, que não obtivemos um caso de overfitting, que é quando o modelo se ajusta perfeitamente ao conjunto de dados de aprendizado - o que é um ponto positivo, apesar de ainda não representar o melhor modelo possível. 

Para prosseguir o projeto, iremos analisar como podemos melhorar esse modelo e como poderemos lidar com o dilema das +2000 categorias de falhas, a fim de conseguir prever com maior especificidade onde há a possibilidade de dar problemas na linha de produção.

 Além disso, para modelos futuros, faz-se necessário observar outras métricas para a avaliação do modelo, pois pela natureza do nosso projeto, é preferível que nosso modelo dê "alarmes falsos" do que acertar muito  e deixar passar algum caso de falha. Em outras palavras, é preferível que ele pegue todos os verdadeiros positivos do que acertar uma boa quantidade de verdadeiros positivos e negativos mas deixar alguns passarem (e uma das métricas que analisa exatamente isso é o recall, que será uma das formas que nos ajudará a avaliar o modelo futuramente).



