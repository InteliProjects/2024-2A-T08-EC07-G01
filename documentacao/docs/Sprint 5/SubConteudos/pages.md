---
title: "Visualização de Dados"
sidebar_position: 5
---

## **1.1** Introdução

O sistema de visualização de dados foi desenvolvido utilizando o **Nuxt.js** e serve como a interface central para monitoramento e interação com as previsões de falhas em veículos e métricas de modelos de machine learning. O objetivo é fornecer uma visualização clara e dinâmica dos dados, permitindo ao usuário final tomar decisões informadas com base nos resultados gerados.

A interface conta com múltiplas páginas, cada uma com uma função específica para exibir dados relacionados ao desempenho dos modelos e falhas detectadas. Estas páginas são construídas com componentes dinâmicos e interativos, como gráficos de linha, gráficos de pizza e modais, que facilitam a análise dos dados. Além disso, as páginas fazem requisições a uma API para obter dados em tempo real.

## **2.1** Páginas Principais

Segue abaixo as principais páginas da aplicação web do projeto. Cada página tem uma função específica e oferece uma visão detalhada ao usuário.

### **2.1.1** Página de Dashboard

**Descrição**: O **Dashboard** é a principal página de visualização de dados do sistema. Ele apresenta gráficos interativos que mostram o desempenho dos modelos de machine learning, bem como as falhas detectadas nos veículos ao longo do tempo.

**Funcionamento**: 
- A página oferece dois modos de visualização: **Falhas** e **Modelos**. O usuário pode alternar entre essas visualizações através de botões interativos.
- Na visualização de **Falhas**, são exibidos gráficos de pizza e gráficos de linha que mostram a quantidade de falhas detectadas por veículo, classes de falhas e a evolução das falhas ao longo do tempo.
- Na visualização de **Modelos**, são apresentados gráficos de barras que exibem métricas de desempenho dos modelos, como acurácia e recall.

Segue abaixo as imagens representando a página da **Dashboard**

:::warning

OBS: As duas primeiras imagens são relacionadas as falhas, enquanto a terceira é relacionada ao modelos preditivos
:::

![Dashboard](/img/webapp/dash1.png)

![Dashboard](/img/webapp/dash2.png)

Abaixo segue a parte da **Dashboard** relacionada aos modelos

![Dashboard](/img/webapp/dash3.png)

### **2.1.2** Página de Histórico

**Descrição**: A página de **Histórico** exibe uma tabela interativa com o histórico completo de previsões e resultados anteriores, fornecendo uma visão detalhada dos dados de falhas ao longo do tempo.

**Funcionamento**:
- A tabela lista previsões passadas, incluindo informações como a data da predição, o resultado (falha ou não), e os testes recomendados.
- O usuário pode pesquisar, ordenar e filtrar as informações da tabela para facilitar a análise de dados históricos.

Abaixo é possível ver a página de **Histórico**:

![Página de Histórico](/img/HistoryReal.png)

### **2.1.3** Página de Previsão Diária

**Descrição**: A página de **Previsão Diária** é dedicada a prever o desempenho diário dos veículos em termos de falhas potenciais. O usuário insere o código identificador de um veículo (KNR) e visualiza a previsão de falha para aquele veículo específico.

**Funcionamento**:
- O usuário insere o KNR de um veículo em um campo de texto. Após submeter a informação, o sistema exibe o resultado da previsão: se o veículo tem ou não uma falha prevista, com base no modelo de machine learning selecionado.
- A página também oferece uma visualização detalhada das diferentes falhas que foram previstas, se aplicável.

Abaixo é possível visualizar a página de **Previsão Diária**:

![Página de Previsão Diária](/img/webapp/predictKnr.png)

### **2.1.4** Página de Treinamento Mensal

**Descrição**: A página de **Treinamento Mensal** permite ao usuário fazer o upload de novos datasets para treinar os modelos de machine learning. Este recurso é essencial para garantir que os modelos estejam sempre atualizados com os dados mais recentes e que suas previsões sejam cada vez mais precisas.

**Funcionamento**:
- A página contém uma área de **drag-and-drop** onde o usuário pode arrastar arquivos de dados para fazer o upload.
- Após o upload, o sistema processa os arquivos e treina os modelos com os novos dados, garantindo que os modelos estejam sempre ajustados às condições mais recentes.

Abaixo é possível visualizar a página de **Treinamento Mensal**:

![Página de Treinamento Mensal](/img/Train.png)

E abaixo, há também o Modal presente na página, após treinar o modelo:

![Modal de Treinamento](/img/TrainModal.png)

### **2.1.5** Página de Escolha do Modelo

**Descrição**: A página de escolha do modelo, apresenta ao usuário todos os modelos feitos para cada categoria, junto com as métricas dos mesmos, para que o usuário possa escolher o modelo que deseja utilizar.

**Funcionamento**:
- O usuário pode escolher o modelo que deseja utilizar, clicando no botão de seleção do modelo.

Segue abaixo a imagem da página de **Escolha do Modelo**:

![Escolha do Modelo](/img/webapp/choose2.png)

Segue abaixo a imagem do Modal de **Escolha do Modelo**:

![Escolha do Modelo](/img/webapp/choose1.png)

### **2.1.6** Landing Page

**Descrição**: A **Landing Page** é a página inicial da aplicação, onde o usuário é recebido com uma breve introdução ao sistema e suas funcionalidades. A página oferece uma visão geral do sistema e convida o usuário a explorar as diferentes funcionalidades disponíveis.

**Funcionamento**:
- O usuário pode navegar para as diferentes páginas da aplicação através de botões interativos ou links na página.

Segue abaixo uma imagem da página de **Landing Page**:

![Landing Page](/img/webapp/landing.png)

### **2.1.7** Página de Healthcheck

**Descrição**: A **Healthcheck** é uma página que exibe o status de saúde do sistema, incluindo informações sobre a conexão com a API, a disponibilidade do banco de dados, e a integridade do Frontend. É um sistema adjacente ao sistema principal, que visa garantir que o sistema principal esteja funcionando corretamente. 

:::tip
O mesmo funciona mesmo se o container do Frontend principal da aplicação estiver fora do ar.
:::

**Fuhcionamento**:
- A página exibe informações sobre o status de saúde do sistema, incluindo mensagens de erro ou alertas caso algo esteja fora do normal.

Segue abaixo uma imagem da página de **Healthcheck**:

A imagem abaixo mostra o status de saúde do sistema, com todos os módulo fora do ar:

![Healthcheck](/img/HealthCheckFail.png)

Já a imagem abaixo mostra o status de saúde do sistema, com todos os módulo funcionando corretamente:

![Healthcheck](/img/HealthCheckPositivo.png)

## **3.1** Conclusão

O sistema de visualização de dados desenvolvido em **Nuxt.js** oferece uma interface dinâmica e intuitiva para visualização de dados e resultados de machine learning. Cada página foi projetada para maximizar a interação do usuário com os dados de predição e desempenho de modelos, facilitando a análise e tomada de decisões. 

Através de requisições à API em tempo real e gráficos dinâmicos, o sistema permite que os usuários tenham acesso às informações mais atualizadas e relevantes. O uso de componentes interativos e a navegação fluida entre as diferentes páginas garantem uma experiência de usuário agradável e eficiente.

Para checar os testes de usabilidade recomendados para a aplicação, clique [aqui](/Sprint%205/SubConteudos/testes).