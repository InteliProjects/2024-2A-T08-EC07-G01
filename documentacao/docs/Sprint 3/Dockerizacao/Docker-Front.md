---
title: "Dockerização do Frontend"
sidebar_position: 2
---

Segue abaixo um exemplo de como o Dockerfile funciona, o mesmo é o que será utilizado para dockerizar o frontend do projeto.

:::warning ATENÇÃO

O mesmo afim de melhorar a leitura e entendimento, foi **dividido** em partes, todavia no fim, deve ser apenas um Dockerfile com todo o conteúdo. No **final** desta etapa do documento, será apresentado o Dockerfile **completo**.
:::

### **1.1.1** Etapa 1

```dockerfile
# Define uma variável de build chamada NODE_VERSION, que especifica a versão do Node.js a ser utilizada
# Essa variável pode ser alterada na hora de construir a imagem, mas o valor padrão é 18.14.2
ARG NODE_VERSION=18.14.2

# Etapa 1: Criação da imagem base
# Utiliza a imagem do Node.js na versão especificada, mas na versão "slim" (mais enxuta, com menos pacotes incluídos)
FROM node:${NODE_VERSION}-slim as base

# Define uma variável de build chamada PORT, que será usada para definir a porta em que a aplicação vai rodar
ARG PORT=3000

# Configura uma variável de ambiente chamada NODE_ENV para 'production'
# Isso indica que a aplicação será executada no modo de produção, otimizando o comportamento do Node.js para esse cenário
ENV NODE_ENV=production

# Define o diretório de trabalho dentro do container, onde o código da aplicação será copiado e executado
WORKDIR /src
```

Esta etapa, é a primeira parte do Dockerfile, onde é definido a versão do Node.js que será utilizada, a porta que a aplicação irá rodar e o ambiente em que a aplicação será executada.

### **1.1.2** Etapa 2

```dockerfile
# Etapa 2: Build da aplicação
# A partir da imagem base anterior, esta etapa é usada para construir o projeto
FROM base as build

# Copia os arquivos package.json e package-lock.json para o diretório de trabalho no container
# A flag --link otimiza o processo de cópia para evitar duplicação desnecessária
COPY --link package.json package-lock.json .

# Instala todas as dependências do projeto, incluindo as de desenvolvimento (indicado por --production=false)
# Isso é necessário para rodar a build da aplicação, mas essas dependências serão removidas posteriormente
RUN npm install --production=false

# Copia o restante dos arquivos do projeto para o diretório de trabalho no container
# Isso inclui o código-fonte, configurações e tudo o que for necessário para o build
COPY --link . .

# Executa o comando de build da aplicação, geralmente definido no package.json (ex: npm run build)
# Esse comando compila o código para produção, gerando uma versão otimizada da aplicação
RUN npm run build

# Remove as dependências de desenvolvimento que foram instaladas anteriormente, deixando apenas as de produção
# Isso ajuda a reduzir o tamanho da imagem final, tornando-a mais leve
RUN npm prune
```

Já esta segunda etapa do Dockerfile, é responsável por realizar o build da aplicação, onde são copiados os arquivos necessários para a execução da aplicação, instaladas as dependências e executado o comando de build da aplicação.

O comando de build da aplicação, é o comando que irá compilar o código para produção, gerando uma versão otimizada da aplicação. O mesmo é definido no package.json, como por exemplo: `npm run build`.

:::tip Informação

Como estamos usando Nuxt, o comando padrão para buildar o mesmo utilizando o NPM é `npm run build`. Todavia dependendo do framework que você está utilizando, o comando pode ser diferente.
:::

### **1.1.3** Etapa 3

```dockerfile

# Etapa 3: Configuração para rodar a aplicação
# Utiliza novamente a imagem base, mas desta vez sem as ferramentas de build, apenas para rodar a aplicação
FROM base

# Define a variável de ambiente PORT, que será usada para determinar em qual porta a aplicação vai rodar
ENV PORT=$PORT

# Copia o build gerado na etapa anterior (output da build) para o diretório de trabalho atual no container
# Essa cópia utiliza o build já otimizado e pronto para rodar
COPY --from=build /src/.output /src/.output

# Comando que será executado quando o container for iniciado
# Inicia o servidor Nuxt.js a partir do arquivo index.mjs dentro do diretório de saída gerado no build
CMD [ "node", ".output/server/index.mjs" ]
```

Por fim, a terceira etapa do Dockerfile, é responsável por configurar o ambiente para rodar a aplicação, onde é definido a porta em que a aplicação irá rodar, copiado o build gerado na etapa anterior e definido o comando que será executado quando o container for iniciado.

Neste caso, o comando para iniciar a aplicação é `node .output/server/index.mjs`, que inicia o servidor Nuxt.js a partir do arquivo index.mjs dentro do diretório de saída gerado no build.

### **1.1.4** Dockerfile Completo

```dockerfile
# Define uma variável de build chamada NODE_VERSION, que especifica a versão do Node.js a ser utilizada
# Essa variável pode ser alterada na hora de construir a imagem, mas o valor padrão é 18.14.2
ARG NODE_VERSION=18.14.2

# Etapa 1: Criação da imagem base
# Utiliza a imagem do Node.js na versão especificada, mas na versão "slim" (mais enxuta, com menos pacotes incluídos)
FROM node:${NODE_VERSION}-slim as base

# Define uma variável de build chamada PORT, que será usada para definir a porta em que a aplicação vai rodar
ARG PORT=3000

# Configura uma variável de ambiente chamada NODE_ENV para 'production'
# Isso indica que a aplicação será executada no modo de produção, otimizando o comportamento do Node.js para esse cenário
ENV NODE_ENV=production

# Define o diretório de trabalho dentro do container, onde o código da aplicação será copiado e executado
WORKDIR /src

# Etapa 2: Build da aplicação
# A partir da imagem base anterior, esta etapa é usada para construir o projeto
FROM base as build

# Copia os arquivos package.json e package-lock.json para o diretório de trabalho no container
# A flag --link otimiza o processo de cópia para evitar duplicação desnecessária
COPY --link package.json package-lock.json .

# Instala todas as dependências do projeto, incluindo as de desenvolvimento (indicado por --production=false)
# Isso é necessário para rodar a build da aplicação, mas essas dependências serão removidas posteriormente
RUN npm install --production=false

# Copia o restante dos arquivos do projeto para o diretório de trabalho no container
# Isso inclui o código-fonte, configurações e tudo o que for necessário para o build
COPY --link . .

# Executa o comando de build da aplicação, geralmente definido no package.json (ex: npm run build)
# Esse comando compila o código para produção, gerando uma versão otimizada da aplicação
RUN npm run build

# Remove as dependências de desenvolvimento que foram instaladas anteriormente, deixando apenas as de produção
# Isso ajuda a reduzir o tamanho da imagem final, tornando-a mais leve
RUN npm prune

# Etapa 3: Configuração para rodar a aplicação
# Utiliza novamente a imagem base, mas desta vez sem as ferramentas de build, apenas para rodar a aplicação
FROM base

# Define a variável de ambiente PORT, que será usada para determinar em qual porta a aplicação vai rodar
ENV PORT=$PORT

# Copia o build gerado na etapa anterior (output da build) para o diretório de trabalho atual no container
# Essa cópia utiliza o build já otimizado e pronto para rodar
COPY --from=build /src/.output /src/.output

# Comando que será executado quando o container for iniciado
# Inicia o servidor Nuxt.js a partir do arquivo index.mjs dentro do diretório de saída gerado no build
CMD [ "node", ".output/server/index.mjs" ]
```

## **1.2** docker-compose.yml

O **Docker Compose** é uma ferramenta poderosa para orquestrar ambientes que envolvem múltiplos contêineres Docker, permitindo que diversos serviços sejam configurados e gerenciados de forma eficiente. Ele possibilita a definição de contêineres interdependentes, como um frontend, backend e banco de dados, em um único arquivo YAML, facilitando o processo de criação e execução de ambientes complexos sem a necessidade de configurar cada contêiner manualmente. Através de um único comando (`docker-compose up`), todos os serviços definidos são iniciados simultaneamente.

Com o Compose, é possível especificar não apenas os serviços que a aplicação utiliza, mas também as redes e volumes necessários para garantir que os contêineres possam se comunicar e compartilhar dados. Essa definição centralizada de serviços, redes e volumes simplifica a implantação de ambientes multi-contêiner, principalmente em projetos que exigem integração entre diferentes componentes, como um servidor web que interage com um banco de dados, ou microserviços distribuídos.

Outro benefício importante é a capacidade de reproduzir ambientes idênticos entre diferentes estágios, como desenvolvimento, teste e produção. Usando o mesmo arquivo `docker-compose.yml`, desenvolvedores podem garantir que o ambiente em suas máquinas locais será idêntico ao ambiente de produção, reduzindo problemas de compatibilidade e facilitando a colaboração dentro da equipe.

# **2.0** Como executar o Docker

Para buildar sua aplicação e transformá-la em uma imagem Docker, é necessário executar alguns comandos específicos após a criação do Dockerfile. Esses comandos seguirão as instruções definidas no Dockerfile, garantindo que sua aplicação e suas dependências sejam corretamente configuradas e otimizadas em uma imagem Docker pronta para ser utilizada.

Esse processo é fundamental para garantir que a aplicação seja executada de forma consistente e isolada em qualquer ambiente que suporte Docker. Através da execução desses comandos, a aplicação se torna portátil e facilmente distribuível, facilitando sua implantação e escalabilidade em diferentes ambientes, como desenvolvimento, testes ou produção.

## **2.1** Comandos

Para executar o Docker, é necessário seguir os passos abaixo:

:::warning ATENÇÃO
Estes são os comandos específicos para o frontend **apenas**, para outras partes o comando pode ser outro.
:::

### **2.1.1** Build da imagem

Este comando é responsável por construir a imagem Docker a partir do Dockerfile, seguindo as instruções definidas no arquivo. Ele irá baixar as dependências necessárias, compilar a aplicação e gerar uma imagem otimizada pronta para ser executada em um container.

```bash
docker build -t frontend .
```

### **2.1.2** Execução do container

O comando cria e executa um contêiner a partir da imagem front, mapeando a porta 5000 do contêiner para a porta 5001 da máquina local, permitindo que a aplicação rodando no contêiner seja acessada através da porta 5001 no host.

:::info Informação
É necessário mapear a porta 5000 do contêiner porque essa é a porta na qual a aplicação dentro do contêiner está configurada para rodar. Como os contêineres são isolados, para acessar a aplicação a partir do host (sua máquina local), é preciso "expor" essa porta para o mundo externo, vinculando-a a uma porta do host, como a 5001, para que seja possível acessar a aplicação pelo navegador ou outras ferramentas.
:::

```bash
docker run -p 5001:5000 front
```

### **2.1.3** Parar o container

Para parar a execução do contêiner, basta executar o comando abaixo. Isso irá interromper a execução da aplicação e encerrar o contêiner, liberando os recursos utilizados.

```bash
docker stop front
```

### **2.1.4** Remover o container

Para remover o contêiner após pará-lo, execute o comando abaixo. Isso irá excluir o contêiner e liberar o espaço ocupado no sistema.

```bash
docker rm front
```

### **2.1.5** Remover a imagem

Para remover a imagem Docker após parar e remover o contêiner, execute o comando abaixo. Isso irá excluir a imagem do sistema, liberando o espaço ocupado no disco.

```bash
docker rmi front
```

## **3.0** Conclusão

A dockerização do frontend do projeto foi uma etapa fundamental para garantir um ambiente de desenvolvimento e produção consistente, isolado e replicável. Atravavés do uso de containers, foi possível padronizar as dependências e configurações necessárias para rodar a aplicação, eliminando problemas de inconsistência entre ambientes e facilitando o processo de desenvolvimento e implantação.

Através do Dockerfile, foi possível definir as etapas necessárias para construir a imagem Docker, incluindo a instalação de dependências, o build da aplicação e a configuração para rodar a aplicação. Com o docker-compose.yml, foi possível orquestrar a execução de múltiplos contêineres de forma eficiente, simplificando a criação e gerenciamento de ambientes complexos.

A dockerização do frontend proporcionou um ambiente padronizado e isolado para o desenvolvimento e produção da aplicação, garantindo que a equipe possa trabalhar de forma consistente e eficiente em qualquer ambiente. Além disso, facilitou a implantação da aplicação, permitindo que a equipe entregue novas versões de forma rápida e confiável, garantindo a qualidade e estabilidade do sistema.'

:::tip Vantagens da Dockerização do Frontend
- Ambiente padronizado e isolado
- Eliminação de problemas de inconsistência entre ambientes
- Simplificação do processo de desenvolvimento
- Facilita a implantação e o deploy
- Garante entrega contínua e eficiente
:::