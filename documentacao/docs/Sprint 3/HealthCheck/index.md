---
title: "HealthCheck"
sidebar_position: 1
---

Durante a Sprint, foi desenvolvido um sistema de verificação de saúde das instâncias do Docker da aplicação. Dessa forma, o grupo criou um frontend em `Nuxt`, o qual realiza solicitações a cada 10 segundos para todos os serviços existentes, sendo eles: 

**Backend**: `localhost:8000/` 

**Frontend**: `localhost:3000/` 

**MongoDB**: `localhost:27017/` 

Assim, quando tem uma resposta, o sistema exibe da seguinte forma: 

<div align="center">

![Healthcheck Sucess](/img/HealthCheckPositivo.png)

</div>

Caso haja algum erro em algum serviço, será exibido: 

<div align="center">

![Healthcheck Fail](/img/HealthCheckFail.png)

</div>

## Guia de execução 

Para executar o frontend é necessário executar os seguintes comandos:

1. Entrar na pasta src do projeto.

```bash
cd src
```

2. Rodar o comando para "construir" (build) o contêiner (caso não tenha instalado o Docker ainda, verifique o [tutorial de execução](/docs/Sprint%203/guia-de-execucao.md)):

```bash
docker compose -f docker-compose-monitor.yml build
```

3. Inicializar o Docker compose 

```bash
docker compose -f docker-compose-monitor.yml up
```

4. Por fim, é necessário inicializar o restante do projeto, como pode ser visto no [guia de execução.](/docs/Sprint%203/guia-de-execucao.md)

5. Para visualizar os status, é necessário utilizar um navegodor sem o cors: 

```bash
google-chrome --disable-web-security --user-data-dir="[some directory here]"
```