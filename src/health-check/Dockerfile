ARG NODE_VERSION=18.14.2

# Usando a imagem base do Node.js
FROM node:${NODE_VERSION}-slim as base

ARG PORT=3001

# Definindo variáveis de ambiente
ENV NODE_ENV=production
ENV NUXT_PORT=$PORT

# Definindo o diretório de trabalho
WORKDIR /src/health-check

# Fase de build
FROM base as build

# Copiando os arquivos de dependências
COPY --link package.json yarn.lock ./

# Instalando dependências
RUN yarn install --frozen-lockfile

# Copiando o restante do código
COPY --link . .

# Construindo o projeto Nuxt para produção
RUN yarn build

# Fase de runtime
FROM base

# Expondo a porta para o contêiner
ENV PORT=$PORT

EXPOSE $PORT

COPY --from=build /src/health-check/.output /src/health-check/.output

CMD [ "node", ".output/server/index.mjs" ]