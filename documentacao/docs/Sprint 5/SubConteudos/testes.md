---
title: "Testes de Usabilidade"
sidebar_position: 5
---

## **1.1** Introdução

Os testes de usabilidade são fundamentais para assegurar que o sistema proporciona uma experiência de usuário fluida, eficiente e intuitiva. Esses testes ajudam a identificar possíveis pontos de frustração ou confusão para os usuários, como dificuldades de navegação, falta de clareza nas informações ou lentidão na resposta de componentes interativos.

Nesta seção, foram planejados testes de usabilidade específicos para a aplicação de visualização de dados. Esses testes cobrem diversas áreas, incluindo a navegabilidade entre páginas, o entendimento das informações apresentadas, a interação com os componentes, como gráficos e modais, e o desempenho do sistema em diferentes dispositivos.

Os testes ainda não foram implementados, mas a tabela abaixo descreve os cenários que serão testados no futuro. Esses testes serão cruciais para garantir que o sistema ofereça uma experiência de usuário otimizada, além de fornecer insights sobre melhorias necessárias na interface e nas funcionalidades.

## **2.1** Tabela de Testes Propostos

A tabela a seguir descreve os testes de usabilidade que serão realizados na aplicação. Ela está organizada em colunas que representam:

- **ID do Teste**: O identificador único do teste proposto.
- **Descrição**: Um breve resumo do que será testado.
- **Página/Função Testada**: A área ou funcionalidade específica do sistema que será avaliada no teste.
- **Critério de Sucesso**: O que define o sucesso do teste. Em outras palavras, o que deve acontecer para que o teste seja considerado bem-sucedido.
- **Status**: O status atual do teste, indicando se ele já foi concluído ou ainda está pendente.

Cada teste tem como foco garantir que os usuários possam utilizar o sistema com facilidade e que a interface seja compreensível e responsiva em diferentes dispositivos. Abaixo estão os testes propostos:

| **ID do Teste** | **Descrição** | **Página/Função Testada** | **Critério de Sucesso** | **Status** |
|-----------------|---------------|---------------------------|-------------------------|------------|
| T01             | Teste de navegabilidade entre as páginas. Verificar se o usuário consegue navegar facilmente entre as páginas de escolha de modelos, dashboard, histórico e previsão. | Navegação Geral | O usuário deve conseguir acessar todas as páginas sem dificuldades e a transição entre elas deve ser rápida e intuitiva. | Não Concluído |
| T02             | Teste da clareza das informações exibidas. Avaliar se os usuários compreendem as informações apresentadas nos gráficos e tabelas sem necessitar de explicações adicionais. | Dashboard | As informações devem ser claras, com gráficos de fácil interpretação e legendas explicativas. | Não Concluído |
| T03             | Teste de resposta visual dos componentes interativos (botões, modais, gráficos). Avaliar se os botões são facilmente clicáveis e se os modais abrem e fecham sem problemas. | Todas as Páginas | Os componentes interativos devem responder imediatamente às ações do usuário, sem atrasos ou erros. | Não Concluído |
| T04             | Teste de tempo de resposta ao selecionar um modelo. Verificar se a seleção de um modelo é rápida e se o modal de seleção funciona corretamente. | Escolha de Modelos | O modal deve abrir imediatamente ao clicar em um modelo e a seleção deve ser registrada sem atraso. | Não Concluído |
| T05             | Teste de compreensão das predições. Avaliar se os usuários conseguem interpretar corretamente os resultados das predições de falhas e suas classes. | Previsão Diária | Os resultados devem ser exibidos de forma clara e o usuário deve entender rapidamente se há falhas previstas ou não. | Não Concluído |
| T06             | Teste da usabilidade do componente de upload de dados. Avaliar se os usuários conseguem facilmente fazer upload de arquivos de dados para o treinamento do modelo. | Treinamento Mensal | O processo de upload deve ser simples e o usuário deve receber feedback claro sobre o progresso e o sucesso do upload. | Não Concluído |
| T07             | Teste de performance da aplicação em diferentes dispositivos. Verificar se o sistema responde adequadamente em dispositivos móveis e tablets, mantendo a usabilidade. | Todas as Páginas | O sistema deve ser responsivo e manter a funcionalidade completa em dispositivos móveis e tablets. | Não Concluído |
| T08             | Teste de feedback visual de erros. Verificar se os usuários recebem mensagens claras em caso de erro (ex: falha ao carregar dados, erro de conexão com a API). | Todas as Páginas | O sistema deve exibir mensagens de erro amigáveis e instrutivas, indicando o problema e possíveis ações corretivas. | Não Concluído |

:::danger IMPORTANTE
Os testes não foram realizados graças ao tempo limitado. Todavia eles foram feitos, com base de que futuramente **devem** ser realizados para garantir a qualidade do sistema.
:::

## **3.1** Conclusão

Os testes de usabilidade descritos acima são essenciais para assegurar que o sistema atenda às expectativas dos usuários em termos de navegação, interação e compreensão das informações apresentadas. Ao cobrir diferentes aspectos da experiência de usuário, esses testes ajudarão a identificar possíveis melhorias na interface e no desempenho da aplicação.

Esses testes futuros fornecerão informações valiosas sobre a experiência dos usuários com o sistema, permitindo a otimização de tempos de resposta, clareza dos dados exibidos e usabilidade geral. A implementação dessas avaliações será crucial para garantir que a aplicação seja intuitiva, acessível e eficaz para todos os usuários em diversos cenários de uso.