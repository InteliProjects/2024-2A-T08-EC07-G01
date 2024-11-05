---
title: "Guia de Execução"
sidebar_position: 1
---

## Execução com o Docker


### Preparação do ambiente 

Para ter um ambiente que interaja com docker, é necessário realizar a instalação do mesmo. Para esse projeto foi utilizada a Versão 26.1.4 do docker, em 16/09/2024. Caso tenha algum problema, consulte a [documentação do docker](https://docs.docker.com/compose/install/) 

1. Instale o Docker e o Docker compose: 

```bash
sudo apt install docker docker-compose-v2
```

Após a execução, deve ser utilizado o comando:

```bash
sudo apt-get update
```

### Executando o projeto

Agora, para a execução do projeto, é necessário abrir um terminal na pasta do projeto e executar os seguintes comandos:

```bash
cd src
docker compose up
```

Depois da execução do comando, o projeto estará funcionando. 
Os serviços estão localizados nas seguintes portas:

**FrontEnd**: (http://localhost:3000)

**BackEnd**: (http://localhost:8000)

**Docs do Backend**: (http://localhost:8000/docs)

**MongoDB**: (http://localhost:27017)

## Execução dos serviços de forma individual

### Frontend 

Para rodar o FrontEnd, é necessário ter npm e node^[18.14.2]. Dessa forma, siga as instruções:

1. Entrar na pasta do projeto e instalar as dependências:
```bash
cd src/app
```

2. "Buildar" o Contêiner:
```bash
docker build -t frontend
```

3. Inicializar o Contêiner:
```bash
docker up -t frontend
```

### Backend

O backend foi construído na versão 3.10 do Python, sendo assim é a versão recomendada para não ter problemas de biblioteca. Para sua execução, siga as seguintes instruções:

1. Entrar na pasta do projeto e instalar as dependências:
```bash
cd src/backend
```

2. "Buildar" o Contêiner:
```bash
docker build -t backend
```

3. Inicializar o Contêiner:
```bash
docker up -t backend
```

### Database