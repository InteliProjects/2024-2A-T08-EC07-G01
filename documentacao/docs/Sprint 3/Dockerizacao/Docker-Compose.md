---
title: "Docker Compose - Backend, Frontend e MongoDB"
sidebar_position: 4
---

Aqui está a documentação do arquivo `docker-compose.yml` que define os serviços para o backend, frontend e banco de dados MongoDB. Este arquivo facilita a configuração de um ambiente de múltiplos contêineres, permitindo que cada parte do sistema funcione de forma integrada.

## **1.0** Serviços Definidos no Docker Compose

### **1.1** Backend

```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  container_name: backend
  ports:
    - "8000:8000"
  environment:
    - DATABASE_URI=mongodb://db:27017
    - DATABASE_NAME=cross_the_line
  depends_on:
    - db
```

Este serviço define o backend da aplicação, que será construído a partir do Dockerfile localizado no diretório `./backend`. Algumas especificações importantes incluem:

- **Portas:** O backend é exposto na porta 8000, o que permite o acesso externo.
- **Variáveis de ambiente:** Definem a URI do banco de dados MongoDB e o nome do banco que será utilizado pela aplicação.
- **depends_on:** O backend depende do serviço de banco de dados db (MongoDB), garantindo que o MongoDB esteja ativo antes de iniciar o backend.

### **1.2** MongoDB (Banco de dados)

```yaml
db:
  image: "mongo:latest"
  container_name: dangobalango
  ports:
    - "27017:27017"
  volumes:
    - mongo_data:/data/db
```
O serviço **db** utiliza a imagem mais recente do MongoDB e expõe a porta 27017. Ele também monta um volume chamado `mongo_data`, que é utilizado para persistir os dados da base mesmo após a parada do contêiner. Alguns detalhes importantes:

- **Container Name:** O nome do contêiner foi definido como `dangobalango`.
- **Volumes:** O volume `mongo_data` é utilizado para garantir que os dados armazenados no banco de dados não sejam perdidos quando o contêiner for parado ou removido.

### **1.3** Frontend

```yaml
frontend:
  build:
    context: ./app
    dockerfile: Dockerfile
  container_name: frontend
  ports:
    - "3000:3000"
  depends_on:
    - backend
  networks:
    - network
```

O serviço **frontend** constrói a aplicação front-end a partir do Dockerfile no diretório `./app`. Ele está configurado para expor a porta 3000, que será usada para acessar a interface da aplicação. Este serviço depende do backend, ou seja, o backend deve estar rodando para que o frontend seja iniciado corretamente.

## **2.0** Volumes

```yaml
volumes:
  mongo_data:
```

O volume `mongo_data` é utilizado pelo contêiner do MongoDB para armazenar dados do banco de forma persistente. Isso significa que os dados não serão perdidos caso o contêiner seja reiniciado ou removido.

## **3.0** Networks

```yaml
networks:
  network:
```

Uma rede chamada `network` foi definida e associada ao serviço frontend, garantindo que os contêineres possam se comunicar entre si de forma eficiente e segura.

## **4.0** Comandos

Para executar os serviços definidos no `docker-compose.yml`, basta rodar o comando abaixo no diretório raiz do projeto:

```bash
docker-compose up
```

Este comando irá iniciar os três serviços (backend, db e frontend) e configurá-los para se comunicarem corretamente. O backend será exposto na porta 8000, o MongoDB na porta 27017 e o frontend na porta 3000.

:::tip Comandos úteis
Aqui estão alguns comandos úteis para gerenciar os contêineres:
:::

### **4.1** Parar os serviços

```bash
docker-compose down
```

Este comando interrompe e remove os contêineres, redes e volumes que foram criados durante a execução do `docker-compose up`.

### **4.2** Recriar um Serviço Específico

Para reconstruir e reiniciar apenas um serviço (ex: backend):

```bash
docker-compose up --build backend
```

### **4.3** Verificar logs

Para visualizar os logs de um serviço específico, como o backend:

```bash
docker-compose logs backend
```

## **5.0** Conclusão

O uso do Docker Compose neste projeto facilita a criação e gerenciamento de ambientes complexos que incluem múltiplos serviços. Com o Compose, é possível orquestrar facilmente a interação entre backend, frontend e banco de dados, garantindo que todos os componentes do sistema estejam sincronizados e funcionando corretamente. Além disso, a definição de volumes e redes garante a persistência dos dados e a comunicação eficiente entre os contêineres.

:::tip Vantagens do Docker Compose

Orquestração de múltiplos serviços
Persistência de dados através de volumes
Facilita o desenvolvimento e testes locais
Simplifica a configuração de redes e comunicação entre contêineres
:::