---
title: "Resumo Docker"
sidebar_position: 1
---

# **0.1** Introdução


O projeto foi dockerizado utilizando o próprio Docker com o objetivo de garantir um ambiente padronizado e isolado para o desenvolvimento e produção. A dockerização foi realizada para eliminar problemas comuns de inconsistência entre os ambientes, que podem surgir devido a diferenças nas configurações das máquinas de desenvolvimento e servidores.

Através do uso de containers, foi possível isolar todas as dependências e configurações necessárias para rodar o projeto, proporcionando um ambiente controlado e replicável. Isso simplificou o processo de desenvolvimento, permitindo que a equipe se concentrasse nas melhorias da aplicação sem se preocupar com discrepâncias de ambientes ou dependências.

Além disso, a dockerização facilita a implantação, já que todo o ambiente necessário para a aplicação é definido no Dockerfile. Isso garante que o processo de deploy seja mais rápido e confiável, reduzindo a necessidade de configuração manual e permitindo uma entrega contínua e eficiente.

:::tip Vantagens da Dockerização do Projeto
- Ambiente padronizado e isolado
- Eliminação de problemas de inconsistência entre ambientes
- Simplificação do processo de desenvolvimento
- Facilita a implantação e o deploy
- Garante entrega contínua e eficiente
:::

# **1.0** Tipos de arquivo

Na hora de dockerizar alguma aplicação, normalmente são utilizados os arquivos abaixos, afim de facilitar a criação e execução do container.

- Dockerfile
- docker-compose.yml

Abaixo será comentado a respeito de ambos e quais são suas funções e importâncias.

:::tip Informação
Normalmente, se tem um Dockerfile para **cada** "parte" do projeto, exemplo: **um** para o frontend, **um** para o backend e **um** para o banco de dados.

Enquanto isso, se tem apenas **um** docker-compose.yml no projeto.
:::

## **1.1** Dockerfile

O Dockerfile é um arquivo de script que contém uma sequência de instruções para construir uma imagem Docker. Nele, você define a base do sistema operacional, as dependências necessárias e o comportamento do aplicativo, como copiar arquivos, instalar pacotes e configurar variáveis de ambiente. Quando o Dockerfile é processado, ele gera uma imagem pronta para ser utilizada, o que simplifica a criação de ambientes de desenvolvimento e produção, garantindo que tudo funcione de maneira padronizada.

O mesmo funciona basicamente como um script de instalação, onde você define o que precisa ser feito para que a aplicação rode corretamente, definindo a ordem das operações. É como se estivesse realizando as operações em uma máquina com o Sistema Operacional recém instalada e sem nenhuma dependência instalada.

# **2.0** Conclusão

A dockerização do projeto foi uma etapa fundamental para garantir um ambiente de desenvolvimento e produção consistente e confiável, eliminando problemas comuns de inconsistência entre ambientes e facilitando o processo de deploy.

Através do Dockerfile, foi possível definir as etapas necessárias para construir a imagem Docker, incluindo a instalação de dependências, o build da aplicação e a configuração para rodar a aplicação. Com o docker-compose.yml, foi possível orquestrar a execução de múltiplos contêineres de forma eficiente, simplificando a criação e gerenciamento de ambientes complexos.