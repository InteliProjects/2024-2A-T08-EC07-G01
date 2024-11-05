---
title: "Fluxos da aplicação"
sidebar_position: 1
---

## **0.** Introdução

Este documento detalha a arquitetura completa do fluxo de treinamento do modelo na aplicação, abordando desde a coleta de dados até a fase de predição. Cada etapa do processo é fundamental para garantir a precisão do modelo, começando pela aquisição de dados relevantes e de alta qualidade. A coleta eficaz de dados é o alicerce para qualquer sistema de aprendizado de máquina e é essencial para o desempenho futuro do modelo.

Além disso, será abordado o processo de retreinamento, que assegura que o modelo mantenha sua relevância diante de mudanças nos dados ou novos padrões identificados. O retreinamento é parte integrante do ciclo de vida do modelo, garantindo que ele continue a fornecer previsões precisas e atualizadas, refletindo as condições atuais do conjunto de dados.

Por fim, o documento explora os critérios de seleção do modelo mais adequado entre os treinados e como os resultados serão exibidos ao usuário. A escolha do modelo correto influencia diretamente a eficiência e precisão do sistema, enquanto a forma de apresentação dos resultados visa proporcionar uma experiência clara e intuitiva para o usuário final.

## **1.** Fluxos

Abaixo serão apresentados os fluxos de treinamento e predição do modelo, bem como o processo de retreinamento e seleção do modelo mais adequado.

Todos eles estarão divididos em etapas, que detalham as atividades realizadas em cada fase do processo, as mesmas também serão documentadas aqui.

:::warning Atenção

Por esta documentação não ter sido feita no fim do projeto, algumas coisas podem estar sucessíveis a **mudanças**. Caso esteja lendo este documento **após** a data de **entrega do projeto** (`11/10/2024`), recomendamos que verifique a documentação mais atualizada no repositório do projeto.

:::

### **1.1** Fluxo de treinamento

A imagem apresentada retrata um fluxo de treinamento de modelo envolvendo interações entre vários componentes, incluindo Volkswagen, BackEnd, MongoDB e **GridFS**. A seguir, será descrito o processo visualizado:

![Fluxo de treinamento](/img/flux-de-treino.png)

#### **1.1.1** Recebimento e coleta de dados

O fluxo começa com o envio de um arquivo CSV por parte da Volkswagen para o BackEnd. Esse arquivo contém os dados necessários para o treinamento do modelo. O BackEnd, então, consulta o banco de dados MongoDB para obter a "receita" do modelo ativo, ou seja, as instruções e parâmetros que orientarão o processo de treinamento. Após a consulta, a receita é coletada e enviada de volta ao BackEnd.

:::tip Info
A receita é um conjunto de instruções que orientam o processo de treinamento do modelo, incluindo os parâmetros a serem utilizados, a arquitetura da rede neural, entre outros detalhes relevantes.
:::

:::danger Atenção

Em nosso caso, estamos levando em consideração que será enviado para a aplicação um arquivo `CSV`, todavia futuramente a mesma poderá ser ligada **diretamente** a uma `API` da Volkswagen, que enviará os dados **diretamente** para o BackEnd. Sem necessidade de intervenção de um operador

:::

#### **1.1.2** Execução do Script de Treinamento

Com a receita em mãos, o BackEnd entra em um loop de execução. Nesse estágio, o script de treinamento é coletado e executado conforme as especificações da receita. O processo de execução do script se repete até que o modelo seja treinado com base nos dados fornecidos. Assim que o treinamento é concluído, o modelo treinado é salvo no banco de dados MongoDB, utilizando o **GridFS** para gerenciar o armazenamento eficiente de grandes volumes de dados.

:::tip Info

**GridFS** é um sistema de arquivos distribuído que permite armazenar e recuperar arquivos de grande volume no MongoDB. Ele divide os arquivos em partes menores, chamadas de `"chunks"`, facilitando o armazenamento e recuperação eficiente de dados.

:::

#### **1.1.3** Testes em Background e Armazenamento de Resultados

Em segundo plano, o sistema continua ativo testando modelos antigos para validar ou atualizar sua eficiência. Os resultados desses testes também são salvos no MongoDB, garantindo um ciclo contínuo de monitoramento e otimização dos modelos treinados. Esse processo em background visa garantir que o sistema esteja sempre utilizando o modelo mais eficiente disponível, conforme as informações coletadas ao longo do tempo.

#### **1.1.4** Conclusão

Ao final do processo, o modelo treinado é disponibilizado para uso na aplicação, permitindo a realização de previsões com base nos dados fornecidos. O modelo é integrado ao sistema, permitindo que os usuários façam consultas e recebam previsões precisas e atualizadas. Além disso, pretendemos fornecer uma comparação entre diferentes modelos, destacando os cinco com as melhores métricas de desempenho, para que os usuários possam escolher a opção mais adequada para suas necessidades.

### **1.2** Fluxo de predição

A imagem abaixo ilustra o fluxo de predição do modelo, que envolve a interação entre o FrontEnd, BackEnd e MongoDB. A seguir, será descrito o processo visualizado:

![Fluxo de predição](/img/flux-de-predicao.png)

#### **1.2.1** Recepção e Armazenamento de Dados

O processo começa com o envio de um arquivo `CSV` contendo o **"KNR"** (chave de identificação dos veículos) pela Volkswagen para o BackEnd. O BackEnd armazena as informações do **"KNR"** no MongoDB, garantindo que os dados estejam disponíveis para futuras referências. Uma vez que o arquivo é salvo, o BackEnd consulta a receita do modelo ativo no MongoDB, que contém os parâmetros necessários para a predição.

#### **1.2.2** Execução da Predição

Após obter a receita do modelo ativo, o BackEnd entra em um loop para executar o script de predição. A receita do modelo inclui a lógica necessária para coletar o script correto e executá-lo de acordo com os dados fornecidos. Durante esse estágio, o BackEnd realiza o processamento dos dados com base na pipeline definida, aplicando o modelo treinado para gerar a predição desejada.

Afim de descobrir como consultar os **KNRs** após serem enviados, cheque a parte abaixo sobre o **Fluxo de Consulta do KNR**.

:::tip Info
Afim de analisar a pipeline definida para realizar o ETL (Extração, Transformação e Carga) dos dados e o tratamento e preparação dos dados, acesse o documento `Pipelines` presente nesta mesma seção.
:::

#### **1.2.3** Armazenamento dos Resultados

Após a execução do script de predição, os resultados gerados são salvos no MongoDB, especificamente na `collection` de **predictions**. Essa abordagem permite que as predições sejam facilmente acessadas para análises posteriores ou consultas futuras. Ao utilizar uma collection dedicada, os dados de predição são organizados de forma eficiente, facilitando operações como filtragem, agregação e busca. Essa estrutura é adequada para armazenar dados estruturados ou semiestruturados, garantindo rápida recuperação e armazenamento otimizado. Isso melhora a performance e a eficiência do banco ao lidar com as predições.

### **1.3** Fluxo de Consulta do KNR

A imagem abaixo ilustra o fluxo de consulta do **KNR** (chave de identificação dos veículos), que envolve a interação entre o FrontEnd, BackEnd e MongoDB.

![Fluxo de consulta do KNR](/img/flux-de-consulta.png)

O fluxo de consulta do KNR, ilustrado na imagem, descreve o processo pelo qual o FrontEnd solicita uma predição específica baseada no identificador KNR, com a comunicação passando pelo BackEnd e o banco de dados MongoDB. A seguir está a descrição detalhada desse fluxo:

#### **1.3.1** Solicitação de Consulta do KNR pelo FrontEnd

O processo se inicia quando o FrontEnd, realiza uma solicitação para consultar um determinado **"KNR"**. Relembrando, o KNR é a chave unica de cada veículo produzido. A solicitação é então enviada ao BackEnd para processamento.

#### **1.3.2** Consulta e Recuperação da Predição pelo BackEnd

Assim que o BackEnd recebe a solicitação do FrontEnd, ele realiza uma consulta no MongoDB. O objetivo é buscar a predição associada ao KNR requisitado, recuperando os resultados de predições armazenadas no banco de dados. O MongoDB processa a consulta e retorna os dados referentes à predição do KNR.

#### **1.3.3** Retorno dos Resultados ao FrontEnd

Após o BackEnd receber a predição do KNR a partir do MongoDB, ele encaminha esses resultados de volta ao FrontEnd. O FrontEnd, por sua vez, exibe as informações para o usuário final, completando o ciclo de consulta de maneira eficiente. Esse fluxo garante que as predições anteriormente calculadas possam ser acessadas e visualizadas a qualquer momento por meio da interface

:::tip Info

A interface pode ser visualizada na seguinte documentação: [Interface](../../Sprint%203/Frontend/Telas/PrincipaisTelas.md).
:::

Este fluxo de consulta reflete a integração harmoniosa entre as camadas de interface, processamento e armazenamento de dados, permitindo uma experiência de usuário ágil e eficaz para acessar predições específicas por meio do KNR.

### **1.4** Fluxo de Análise dos Modelos

A imagem abaixo ilustra o fluxo de análise dos modelos, que envolve a interação entre o FrontEnd, BackEnd e MongoDB.

![Fluxo de análise dos modelos](/img/flux-de-analise.png)

O fluxo de análise de modelos, conforme representado na imagem, descreve o processo em que o FrontEnd solicita a análise dos modelos de machine learning ao BackEnd, que realiza a coleta e comparação dos resultados. A seguir está a descrição detalhada desse processo:

#### **1.4.1** Solicitação de Análise pelo FrontEnd

O processo inicia-se quando o FrontEnd solicita uma análise dos modelos. Ele envia essa solicitação ao BackEnd. A análise dos modelos é fundamental para avaliar o desempenho de cada um e determinar qual deles está oferecendo as melhores predições ou resultados.

#### **1.4.2** Coleta de Dados e Comparação pelo BackEnd

Assim que o BackEnd recebe a solicitação, ele inicia a coleta dos dados do teste mais recente armazenado no MongoDB. Esses dados incluem métricas de desempenho e resultados de predições referentes apenas ao último teste realizado. O BackEnd então procede com a análise dessas informações, comparando diferentes modelos e avaliando seus resultados com base nas métricas coletadas do teste mais recente.

#### **1.4.3** Envio das Análises para o FrontEnd

Após concluir a comparação e análise dos modelos, o BackEnd envia os resultados dessa análise de volta ao FrontEnd. O FrontEnd, por sua vez, exibe esses resultados para o usuário final. Esse processo permite que o sistema identifique quais modelos estão performando melhor e garante que o modelo mais eficiente seja selecionado para uso futuro.

:::tip Info
Foi **optado** por escolher está abordagem do usuário poder escolher o melhor modelo, afim de garantir a transparência e confiança no sistema. **Contudo**, futuramente, poderá ser implementado um sistema de seleção automática do modelo mais eficiente, baseado em métricas de desempenho e precisão.

**OBS:** Não foi implementado o modelo de seleção automática devido ao desconhecimento do processo interno da Volkswagen, logo optamos por deixar a escolha com eles.
:::

### **1.5** Fluxo de Escolha do Modelo

A imagem abaixo ilustra o fluxo de retreinamento do modelo, que envolve a interação entre o FrontEnd, BackEnd e MongoDB.

![Fluxo de escolha do modelo](/img/fluxo-de-escolha.png)

O fluxo de escolha do modelo, conforme apresentado na imagem, descreve o processo de seleção e atualização do modelo de machine learning ativo com base na comparação de desempenho entre os modelos disponíveis. A seguir está a descrição detalhada desse processo:

#### **1.5.1** Solicitação de Comparação de Modelos pelo FrontEnd

O fluxo começa com o FrontEnd solicitando uma comparação dos modelos disponíveis. O usuário pode iniciar essa ação para determinar qual modelo está apresentando o melhor desempenho. O pedido é então enviado ao BackEnd, que gerencia a execução dessa análise comparativa.

#### **1.5.2** Consulta e Comparação de Modelos pelo BackEnd

Ao receber a solicitação, o BackEnd consulta os modelos disponíveis e seus resultados no MongoDB. Esses dados incluem informações sobre o desempenho recente de cada modelo. O BackEnd entra em um loop de comparação, analisando o desempenho dos diferentes modelos com base em métricas predefinidas, como acurácia, precisão, e outras métricas relevantes.

#### **1.5.3** Exibição dos Resultados e Atualização do Modelo Ativo

Uma vez que a comparação dos modelos é concluída, o BackEnd envia os resultados de volta ao FrontEnd, que exibe a comparação para o usuário. Com base nesses resultados, o usuário ou o sistema pode decidir qual modelo deve ser definido como o modelo ativo. Assim que a escolha é feita, o BackEnd atualiza a coleção de `"active models"` no MongoDB, garantindo que o novo modelo selecionado será utilizado nas próximas predições.

:::tip Info
Uma coleção no MongoDB é equivalente a uma tabela em um banco de dados relacional. Ela armazena documentos, que são os registros de dados, e pode ser acessada e consultada por meio de consultas específicas.
:::

Esse fluxo garante que o sistema utilize sempre o modelo com o melhor desempenho, ajustando-se automaticamente ou permitindo que o usuário faça essa escolha de forma informada e otimizada.

## **2.0** Conclusão

Este documento apresentou de forma detalhada os principais fluxos da aplicação, desde o treinamento e predição de modelos até a análise e escolha do modelo mais adequado para utilização. Através de uma arquitetura bem definida, a aplicação garante a integração eficiente entre coleta de dados, execução de scripts de machine learning e armazenamento dos resultados. Além disso, os mecanismos de retreinamento e comparação de modelos asseguram que o sistema esteja sempre atualizado e utilizando o modelo mais eficaz, oferecendo previsões confiáveis e precisas para os usuários.

O fluxo contínuo de avaliação dos modelos e a capacidade de comparar e selecionar automaticamente o melhor modelo ativo demonstram a robustez e a adaptabilidade da solução. Isso permite que a aplicação atenda às necessidades dinâmicas do ambiente de produção, otimizando seu desempenho ao longo do tempo. A combinação entre o FrontEnd, BackEnd e MongoDB proporciona uma interface intuitiva para o usuário, ao mesmo tempo que mantém a complexidade de processamento oculta e eficiente.

Em resumo, a arquitetura apresentada oferece uma solução escalável e eficiente para o gerenciamento de modelos de machine learning, garantindo que o sistema esteja sempre operando com base nas melhores práticas e resultados disponíveis, proporcionando valor agregado ao negócio e aos usuários finais.