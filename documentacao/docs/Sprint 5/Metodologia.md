---

title: "Documentação Geral"
sidebar_position: 1

---


## Índice

- [1.1 Introdução](#11-introdução)  

- [2.1 Soluções Implementadas](#21-soluções-implementadas)  

- [3.1 Principais Mudanças](#31-principais-mudanças)  

- [4.1 Próximos Passos](#41-próximos-passos)  

- [5.1 Conclusão](#51-conclusão)  

## **1.1 Introdução**

Este documento oferece uma visão abrangente sobre o desenvolvimento do sistema, destacando as principais etapas do processo e fornecendo um detalhamento das metodologias e ferramentas utilizadas. Nosso objetivo é garantir que qualquer pessoa, independentemente de seu conhecimento técnico, possa compreender o que foi realizado, como o sistema evoluiu, e quais foram os principais marcos atingidos durante as diferentes fases do projeto.

O projeto foi desenvolvido em sprints, que são ciclos curtos de trabalho, geralmente com duração de duas semanas. Cada sprint tem um objetivo específico, que pode envolver o desenvolvimento de uma nova funcionalidade, a correção de problemas ou a melhoria da interface do sistema. Ao final de cada sprint, são entregues funcionalidades testadas e documentadas, o que possibilita um processo de evolução contínua do sistema.

A cada nova iteração, a equipe revisou suas abordagens e adaptou metodologias para atender às demandas em mudança. Isso inclui a adoção de novas tecnologias, a revisão de processos de desenvolvimento e a atualização contínua da documentação. Este documento reflete o esforço contínuo da equipe em garantir que o sistema permaneça alinhado com os requisitos do projeto e que toda a informação necessária esteja devidamente registrada e organizada.

### **1.2 Descrição do Problema**

Atualmente, a Volkswagen realiza uma série de testes de rodagem em todos os veículos que saem da linha de montagem, com o objetivo de identificar possíveis falhas. No entanto, essa abordagem padronizada não é a mais eficiente, pois todos os veículos passam pelos mesmos testes, independentemente das condições específicas de sua montagem. Isso resulta em um aumento considerável nos custos operacionais e no tempo necessário para validar a qualidade, já que não há uma forma de identificar previamente possíveis defeitos.

O desafio é antecipar, logo após a montagem, quais veículos têm maior probabilidade de apresentar defeitos e em quais áreas específicas. Isso pode ser feito analisando dados específicos do processo de montagem, como o torque aplicado nos parafusos e o tempo gasto em diferentes etapas da linha de produção, entre outros fatores. Com base nessa análise preditiva, é possível orientar a equipe responsável pelos testes de rodagem para realizar verificações direcionadas, focadas nas potenciais inconsistências apontadas pelos modelos preditivos.

Essa solução tem o potencial de otimizar o processo de testes, reduzindo custos e tempo. Além disso, melhora a eficácia na detecção de defeitos, garantindo que os recursos sejam aplicados de maneira mais inteligente e eficiente.

### **1.3 Objetivo do Projeto**

O principal objetivo deste projeto foi criar um sistema preditivo baseado em **machine learning** capaz de antecipar falhas em veículos da Volkswagen antes que eles fossem enviados para o teste de rodagem. Isso não apenas proporcionaria uma previsão das falhas, mas também ofereceria aos operadores informações valiosas sobre o desempenho esperado dos veículos, permitindo uma análise proativa. Dessa forma, a empresa poderia reduzir custos e aumentar a eficiência no processo de inspeção e teste dos veículos.

A ideia central foi processar e analisar dados históricos de falhas e inspeções para treinar um modelo preditivo. Este modelo seria capaz de prever se um veículo falharia antes mesmo de ser testado em campo. Além disso, o projeto visava oferecer uma interface web amigável e intuitiva, permitindo que os usuários pudessem facilmente visualizar as previsões geradas pelo modelo e interagir com os dados.

O segundo objetivo do projeto foi garantir que a aplicação fosse acessível remotamente. Para isso, optamos por hospedar a aplicação na nuvem utilizando a plataforma **AWS (Amazon Web Services)**, o que proporcionou maior flexibilidade e facilidade de acesso. Esse modelo de deploy eliminou a necessidade de instalar a aplicação localmente nos dispositivos dos usuários, garantindo que a solução pudesse ser utilizada em qualquer lugar, sem complicações.

Por fim, o projeto visava não só melhorar a experiência do usuário final, mas também garantir que o sistema fosse escalável e flexível, permitindo futuras adaptações e a integração de novos dados ou modelos de machine learning sem necessidade de grandes mudanças na infraestrutura existente.

### **1.4 Metodologia**

O desenvolvimento do projeto foi guiado por metodologias ágeis, focadas em entregas contínuas e melhorias incrementais. A principal metodologia adotada foi o **Scrum**, que organiza o trabalho em sprints. Cada sprint tem uma duração fixa (duas semanas, neste caso), durante as quais a equipe define um conjunto de tarefas a serem concluídas. Ao final de cada sprint, realizamos uma revisão para verificar se os objetivos foram atingidos e para planejar as etapas seguintes.

Além do Scrum, também utilizamos **Kanban** como uma ferramenta visual para monitorar o fluxo de trabalho. No Kanban, as tarefas são organizadas em colunas (por exemplo, "a fazer", "em andamento" e "concluído"), o que facilita a visualização do progresso de cada atividade. Isso permitiu à equipe identificar gargalos ou tarefas que estavam demorando mais do que o esperado, e ajustar o planejamento de acordo.

O **Code Review** foi outra prática importante implementada durante o desenvolvimento. Cada membro da equipe revisou o código de outros desenvolvedores para garantir a qualidade do software. Essas revisões não só ajudaram a identificar erros, mas também promoveram a troca de conhecimentos, incentivando a aplicação de boas práticas de programação.

A **documentação** foi elaborada ao longo do projeto para garantir que todas as funcionalidades fossem devidamente registradas. Além de documentação técnica, também criamos guias para auxiliar no uso do sistema, com o objetivo de facilitar sua adoção por parte de novos usuários e desenvolvedores que se envolverão com o projeto no futuro.

### **1.5 Ferramentas Utilizadas**

Durante o desenvolvimento do projeto, várias ferramentas tecnológicas foram utilizadas para garantir a eficiência e qualidade do sistema. Cada uma dessas ferramentas desempenhou um papel fundamental em diferentes partes do processo. Aqui está uma visão geral das principais ferramentas:

- **Python:** A linguagem de programação Python foi a base para o desenvolvimento do modelo de machine learning. Python oferece bibliotecas robustas para análise de dados e aprendizado de máquina, como **pandas**, **scikit-learn** e **TensorFlow**, que foram essenciais para manipular os dados e treinar o modelo. Além disso, Python também foi utilizado no desenvolvimento do backend da aplicação, responsável por gerenciar a lógica de negócios e a comunicação com o banco de dados.

- **Nuxt.js:** Para o desenvolvimento da interface do usuário (frontend), optamos por utilizar o **Nuxt.js**, uma framework baseada em **Vue.js**. O Nuxt permitiu criar páginas dinâmicas e estáticas com facilidade, garantindo uma experiência fluida e interativa para os usuários. A escolha dessa ferramenta também facilitou a implementação de práticas de SEO (Search Engine Optimization), garantindo que a aplicação fosse otimizada para os motores de busca.

- **Docker:** O **Docker** foi utilizado para encapsular a aplicação em containers, o que simplificou o processo de deploy (implantação) na nuvem. Com o Docker, conseguimos garantir que o sistema funcionasse de forma consistente em diferentes ambientes, eliminando problemas de compatibilidade e facilitando a escalabilidade do projeto.

- **AWS (Amazon Web Services):** Utilizamos a AWS para hospedar a aplicação na nuvem, proporcionando acesso remoto e a escalabilidade necessária para o projeto. Com a AWS, foi possível criar uma instância EC2, que permitiu que a aplicação rodasse de forma eficiente e estivesse disponível a qualquer momento para os usuários.

- **GitHub:** Para versionamento do código, utilizamos o **GitHub**, uma plataforma que permite a colaboração entre os membros da equipe. O GitHub facilitou o controle de versões, garantindo que todas as alterações fossem registradas e que o histórico do projeto estivesse disponível para consultas futuras.

- **Bruno:** Utilizamos o **Bruno** para documentar a API do sistema. O Bruno possibilitou a visualização e interação com os endpoints de forma simples e intuitiva, permitindo que os desenvolvedores compreendessem como se comunicar com o backend da aplicação.

- **MongoDB:** O **MongoDB** foi escolhido como o banco de dados principal para armazenar e consultar os dados do projeto. A escolha de um banco de dados NoSQL foi estratégica, pois o MongoDB oferece flexibilidade na manipulação de grandes volumes de dados, além de permitir que o sistema armazene diferentes tipos de dados de forma eficiente. Ele também atuou como **Data Lake**, centralizando a coleta de dados para análises futuras.

---

## **2.1 Soluções Implementadas**

Durante o ciclo de desenvolvimento, implementamos uma série de soluções técnicas e funcionais que ajudaram a moldar o sistema em sua forma atual. A seguir, detalhamos as principais soluções e mudanças realizadas ao longo das sprints.

### **2.2 Sprint 1: Análise Exploratória e Primeiro Modelo**

A primeira sprint foi dedicada à **análise exploratória dos dados** disponíveis. Essa fase inicial foi crucial para compreendermos a estrutura dos dados e para identificar padrões que poderiam ser utilizados no treinamento do modelo preditivo. A análise envolveu o estudo de várias colunas do dataset, como históricos de falhas, inspeções e características dos veículos.

Além disso, nesta sprint, desenvolvemos o **primeiro modelo preditivo** utilizando uma rede neural **LSTM (Long Short-Term Memory)**. O modelo foi projetado para prever se um veículo falharia ou não antes de ser enviado para o teste de rodagem. Esse primeiro modelo tinha como foco principal a construção de uma base sólida para previsões futuras, e foi alimentado com os dados disponíveis após o processamento inicial.

Paralelamente, também realizamos uma **análise financeira** do projeto, verificando sua viabilidade econômica, e uma **análise de UX (User Experience)**, para entender como seria a interface do sistema, visando garantir uma boa usabilidade para os operadores.

Principais entregas da Sprint 1:
- Análise exploratória dos dados disponíveis.
- Desenvolvimento do primeiro modelo preditivo (LSTM).
- Definição do escopo e metas iniciais do projeto.
- Realização de análises financeira e de UX.

:::tip Sprint 1

A documentação completa da primeira Sprint pode ser encontrada [aqui](/Sprint%201/Entendimento%20do%20Neg%C3%B3cio/An%C3%A1lise%20Financeira).
:::

### **2.3 Sprint 2: Integração de Backend, Frontend e Melhorias no Modelo**

Na segunda sprint, avançamos significativamente com a **definição da interface do projeto**, criando protótipos detalhados no Figma. A equipe trabalhou na construção da arquitetura do sistema, integrando o **backend** com o modelo de machine learning e estabelecendo a conexão com o banco de dados **MongoDB**. Esse trabalho permitiu que o sistema começasse a funcionar como um todo integrado.

Também foi durante essa sprint que iniciamos o desenvolvimento de um novo modelo preditivo, focado em prever não apenas **se** um veículo falharia, mas também **quais categorias de falhas** poderiam ocorrer. Esse segundo modelo tinha o objetivo de oferecer previsões mais detalhadas, fornecendo aos operadores informações mais granulares para análise.

O que foi feito:
- Definição detalhada da interface no Figma.
- Desenvolvimento da arquitetura do backend e sua integração com o modelo.
- Conexão com o banco de dados MongoDB.
- Início do desenvolvimento do frontend.
- Continuação do desenvolvimento do modelo preditivo, com foco em prever categorias de falhas.

Essa sprint foi marcada pela continuidade do aprimoramento do modelo preditivo, que apresentou resultados mais estáveis e com menor risco de overfitting. O modelo de categorias de falhas, embora promissor, ainda estava em fase inicial e exigiu ajustes posteriores para melhorar a precisão de suas previsões.

:::tip Sprint 2

A documentação completa da segunda Sprint pode ser encontrada [aqui](/Sprint%202/Descricao%20do%20Problema).
:::

### **2.4 Sprint 3: Desenvolvimento do Frontend e Dockerização**

Na terceira sprint, o foco principal foi finalizar o desenvolvimento do **frontend** da aplicação. Utilizando o **Nuxt.js**, a equipe criou as páginas e componentes necessários para a interface do usuário, garantindo uma experiência amigável e intuitiva. Ao longo desta Sprint, o frontend foi mockado afim de simular a interação com o backend.

Também foi desenvolvido durante a Sprint a `Dockerização` da aplicação, que consistiu em encapsular a aplicação em containers Docker. Essa etapa foi fundamental para garantir a portabilidade e escalabilidade do sistema, permitindo que ele fosse facilmente implantado em diferentes ambientes.

Além disto tudo, também foi seguida a análise de dados e aprimoramento do modelo preditivo, com foco em melhorar a precisão das previsões e a robustez do sistema como um todo. Focando no modelo de classificação de falhas, que na sprint anterior apresentou resultados ruins, e precisava ser melhorado.

Por fim, também foi criado um sistema de Health Check para monitorar a saúde da aplicação, garantindo que ela estivesse sempre disponível e funcionando corretamente. O mesmo monitoriraria o backend, frontend e o banco de dados. Mostrando as informações dos mesmos em uma outra aplicação web, feita em **Nuxt.js**.

Principais entregas da Sprint 3:

- Finalização do desenvolvimento do frontend.
- Dockerização da aplicação.
- Análise de dados e aprimoramento do modelo preditivo.
- Implementação de um sistema de Health Check para monitorar a saúde da aplicação.
- Continuação do desenvolvimento do Backend afim de agregar as novas funcionalidades.

Está Sprint foi marcada principalmente pela Dockerização da aplicação, que foi um grande marco para o projeto, pois permitiu que a aplicação fosse facilmente implantada em diferentes ambientes, garantindo a portabilidade e escalabilidade do sistema.

:::tip Sprint 3

A documentação completa da terceira Sprint pode ser encontrada [aqui](/Sprint%203/HealthCheck/).
:::

### **2.5 Sprint 4: Integração do Backend com o Frontend e Pipeline**

Na quarta sprint, o foco principal foi integrar o **backend** com o **frontend**, assegurando que a comunicação entre as duas partes do sistema fosse eficiente, segura e rápida. A equipe trabalhou na criação de **endpoints de API** que permitiram ao frontend consultar o backend e acessar os dados necessários para exibir as previsões geradas pelo modelo de machine learning. Esse processo foi vital para que a interface pudesse fornecer informações atualizadas e precisas para os usuários.

Para que essa integração funcionasse de maneira otimizada, foi desenvolvida uma **pipeline** de dados juntamente com um processo de **ETL** (Extract, Transform, Load). O ETL foi responsável por garantir que os dados fossem corretamente extraídos, transformados e carregados no sistema de forma automatizada. A pipeline, por sua vez, orquestrou o fluxo de dados entre o banco de dados, o modelo preditivo e a interface do usuário. Isso permitiu que os dados fossem constantemente atualizados, possibilitando uma experiência em **tempo real** para os operadores.

Além da integração, a equipe também refinou o **modelo de classificação de falhas**, que já vinha sendo desenvolvido. Durante essa sprint, melhorias no modelo trouxeram resultados mais precisos, aumentando a confiabilidade das previsões. Os códigos do modelo foram refatorados em scripts mais organizados e simplificados, facilitando tanto a manutenção quanto a execução contínua dos modelos. Essa abordagem garantiu que o sistema fosse escalável e de fácil manutenção no futuro.

**Principais entregas da Sprint 4:**

- Integração completa do backend com o frontend via API.
- Implementação de endpoints de API para comunicação eficiente entre as partes do sistema.
- Desenvolvimento de uma pipeline de dados e processo ETL para garantir a integridade e atualização dos dados.
- Refinamento do modelo de classificação de falhas, com aumento da precisão.
- Refatoração dos códigos dos modelos em scripts únicos e organizados.

O marco principal desta Sprint foi o desenvolvimento e integração da pipeline de dados e do processo ETL, que permitiram que o sistema funcionasse de forma eficiente e em tempo real. A integração do backend com o frontend também foi um passo importante para garantir que a aplicação fornecesse informações precisas e atualizadas para os usuários.

:::tip Sprint 4

A documentação completa da quarta Sprint pode ser encontrada [aqui](/Sprint%204/Backend/).
:::

### **2.6 Sprint 5: Deploy e Documentação**

Na quinta sprint, a prioridade foi o **deploy** da aplicação para a **AWS** (Amazon Web Services), permitindo que o sistema estivesse disponível de maneira remota e acessível de qualquer local. A equipe configurou uma instância EC2 na AWS e utilizou **Docker** para gerenciar os containers da aplicação, garantindo que todos os serviços estivessem funcionando de maneira consistente. O deploy na nuvem eliminou a necessidade de instalação local, facilitando a utilização pelos operadores e tornando o sistema escalável e flexível.

Além da implementação na nuvem, esta sprint também focou na produção de uma documentação completa do sistema. A equipe elaborou **guias detalhados** que cobriam todos os aspectos do desenvolvimento, desde a escolha das ferramentas até as metodologias utilizadas. A documentação incluiu também tutoriais para uso da aplicação e instruções para manutenção, garantindo que futuros desenvolvedores ou operadores pudessem entender e trabalhar com o sistema de maneira eficiente.

A última sprint também envolveu a conclusão de pequenas melhorias no backend e frontend, bem como os ajustes finais no modelo preditivo. Essas otimizações garantiram que o sistema estivesse funcionando de forma robusta e eficiente. A combinação do deploy bem-sucedido e da documentação clara e detalhada concluiu o projeto com êxito, deixando o sistema pronto para ser utilizado e expandido conforme necessário.


**Principais entregas da Sprint 5:**

- Deploy completo da aplicação na AWS, com configuração de instância EC2 e containers Docker.
- Documentação detalhada do projeto, cobrindo processos, metodologias e ferramentas utilizadas.
- Criação de guias de uso e manutenção, facilitando a adoção do sistema por novos usuários.
- Finalização das integrações e ajustes no backend e frontend.
- Ajustes finais no modelo de classificação de falhas, garantindo alta precisão.

Por fim está ultima Sprint teve como foco o deploy da aplicação na AWS, que  permitiu que o sistema fosse acessível remotamente e escalável. A documentação detalhada também foi um ponto crucial, garantindo que o conhecimento acumulado ao longo do desenvolvimento fosse registrado e disponível para futuras referências.


## **3.1** Principais Mudanças

Durante o desenvolvimento do projeto, várias mudanças foram realizadas para garantir que o sistema atendesse aos requisitos e expectativas da Volkswagen. Algumas das principais mudanças incluíram:

- **Refinamento do Modelo Preditivo:** O modelo de classificação de falhas passou por várias iterações para melhorar sua precisão e robustez. Foram realizados ajustes nos hiperparâmetros, na arquitetura da rede neural e na seleção de features, resultando em previsões mais confiáveis e consistentes.

- **Alteração do método para salvar os scripts de treino:** Originalmente os códigos de treino dos modelos seriam salvos no GridFS do MongoDB. Todavia foi decidido que os mesmos seriam por hora salvos localmente, pela falta de tempo. Todavia o backend está pronto para receber os scripts de treino e armazená-los no GridFS.


## **4.1 Próximos Passos**

Com a conclusão do projeto atual, a equipe identifica várias oportunidades para continuar aprimorando o sistema e aumentar seu impacto no processo de detecção de falhas em veículos. Esses próximos passos não apenas melhorarão a precisão e a eficiência do modelo, mas também expandirão as funcionalidades da aplicação, tornando-a uma ferramenta mais completa e valiosa para a Volkswagen. As sugestões a seguir visam garantir a evolução contínua do sistema, mantendo-o atualizado e relevante para as necessidades futuras.

- **Aprimoramento do Modelo Preditivo:** É essencial continuar refinando o modelo de classificação de falhas, explorando novas técnicas de machine learning e algoritmos mais avançados. Técnicas como aprendizado profundo (deep learning), ou até mesmo a combinação de modelos, podem ser consideradas para melhorar ainda mais a precisão das previsões. Além disso, o desempenho do modelo em produção deve ser monitorado regularmente, ajustando seus parâmetros conforme necessário para manter a eficácia e evitar possíveis quedas de desempenho.

- **Integração de Novos Tipos de Dados:** Para enriquecer as previsões do modelo, a equipe sugere integrar novas fontes de dados, como informações de sensores dos veículos ou registros de manutenções. Esses dados adicionais podem fornecer insights mais profundos sobre o estado dos veículos e ajudar a detectar padrões que não foram capturados com os dados existentes. Essa integração pode aumentar significativamente a capacidade do sistema de prever falhas com maior precisão e fornecer recomendações mais úteis aos operadores.

- **Implementação de Novas Funcionalidades:** O desenvolvimento de novas funcionalidades pode melhorar a usabilidade e ampliar o impacto da aplicação. Entre essas funcionalidades, destacam-se a criação de um **sistema de alertas em tempo real** para notificar os operadores sobre falhas iminentes, a geração de **relatórios personalizados** que agreguem valor aos gestores e engenheiros, e a implementação de uma **interface administrativa** para facilitar a gestão de dados e usuários. Essas melhorias proporcionariam uma experiência mais rica e eficiente para os diferentes perfis de usuários da aplicação.

- **Implementação do GridFS para Armazenamento Seguro:** Para garantir que os scripts de treino dos modelos sejam armazenados de maneira segura e acessível para futuras referências e modificações, recomenda-se a implementação do **GridFS**. Essa solução possibilita o armazenamento eficiente de arquivos de grande porte, como os scripts de machine learning, diretamente no banco de dados MongoDB, garantindo a segurança e a facilidade de acesso para futuras execuções ou revisões.

- **Desenvolvimento de Testes Automatizados:** A criação de uma suíte de **testes automatizados** é fundamental para garantir a qualidade contínua do sistema à medida que novas funcionalidades são desenvolvidas. Testes de unidade, integração e aceitação devem ser implementados para cobrir as principais funcionalidades do sistema e detectar possíveis erros ou regressões durante o ciclo de desenvolvimento. A automação de testes contribui para a estabilidade do projeto e reduz a probabilidade de falhas em produção.

A implementação dessas ações fortalecerá o sistema, permitindo que ele se mantenha robusto e adaptável diante de novas demandas. À medida que o modelo for aprimorado e o sistema receber novas funcionalidades, a Volkswagen poderá aproveitar ao máximo essa solução preditiva, otimizando ainda mais seus processos de manutenção e análise de dados. Com essas melhorias, a aplicação estará preparada para atender a uma variedade maior de cenários e para evoluir junto com as necessidades da empresa e do mercado.

## **5.1 Conclusão**

O projeto foi concluído com sucesso, atingindo todos os objetivos inicialmente propostos e entregando uma solução preditiva robusta, escalável e acessível para a Volkswagen. A equipe enfrentou diversos desafios técnicos e organizacionais ao longo do desenvolvimento, mas foi capaz de superá-los graças à dedicação e colaboração entre todos os membros. O resultado final é um sistema que fornece previsões confiáveis sobre falhas em veículos, permitindo que a Volkswagen tome decisões proativas, melhorando seus processos de inspeção e testes.

A solução desenvolvida representa uma importante ferramenta para a Volkswagen, uma vez que otimiza os processos internos e reduz custos operacionais. O sistema é flexível o suficiente para ser expandido ou adaptado conforme novas necessidades surgirem, como a integração de novos modelos de machine learning ou a incorporação de novos tipos de dados. Isso garante que a aplicação possa evoluir junto com as demandas da empresa e do mercado.

Para a equipe, este projeto foi uma oportunidade significativa de aprendizado e crescimento. O desenvolvimento envolveu o uso de tecnologias avançadas e a aplicação de metodologias ágeis, proporcionando uma experiência enriquecedora. Cada membro da equipe aprimorou suas habilidades técnicas e colaborativas, aprendendo a lidar com problemas complexos e a desenvolver soluções inovadoras. O sucesso do projeto é um reflexo do esforço conjunto, da criatividade e da resiliência da equipe, que se uniu para superar todos os desafios e entregar uma solução de alta qualidade.

---
