---
title: "Dockerização do Backend"
sidebar_position: 3
---

Aqui está um exemplo de como o Dockerfile para o backend é configurado. Ele serve como referência para dockerizar o backend do projeto.

:::warning ATENÇÃO
O Dockerfile foi **dividido** em partes para facilitar o entendimento. No **final** desta seção, será mostrado o Dockerfile **completo**.
:::

### **1.1.1** Etapa 1

```dockerfile
# Utiliza a imagem oficial do Python na versão 3.10
FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app
```

Esta primeira parte do Dockerfile cria o ambiente base utilizando uma imagem do Python 3.10 e define o diretório de trabalho, onde os arquivos do projeto serão copiados.

### **1.1.2** Etapa 2

```dockerfile
# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências necessárias sem usar cache para manter a imagem mais enxuta
RUN pip install --no-cache-dir --upgrade -r requirements.txt

```

Nesta etapa, o arquivo `requirements.txt` é copiado para o container e as dependências do projeto são instaladas. Usar o `--no-cache-dir` ajuda a reduzir o tamanho final da imagem.

### **1.1.3** Etapa 2

```dockerfile
# Copia o código da aplicação para o diretório de trabalho no container
COPY ./app /app/app

# Define uma variável de ambiente para o PythonPath
ENV PYTHONPATH=/app

# Expõe a porta 8000, que será usada pelo FastAPI
EXPOSE 8000

```

Aqui, o código da aplicação é copiado para o container, a variável de ambiente `PYTHONPATH` é configurada e a porta 8000 é exposta, pois será usada para rodar o servidor FastAPI.

### **1.1.4** Etapa 4

```dockerfile
# Comando para iniciar o servidor FastAPI
CMD ["fastapi", "run", "--host", "0.0.0.0"]
```

Por fim, o comando `CMD` define como o servidor FastAPI será executado quando o container iniciar.

### **1.2** Dockerfile Completo

```dockerfile
# Utiliza a imagem oficial do Python na versão 3.10
FROM python:3.10

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências necessárias sem usar cache para manter a imagem mais enxuta
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copia o código da aplicação para o diretório de trabalho no container
COPY ./app /app/app

# Define uma variável de ambiente para o PythonPath
ENV PYTHONPATH=/app

# Expõe a porta 8000, que será usada pelo FastAPI
EXPOSE 8000

# Comando para iniciar o servidor FastAPI
CMD ["fastapi", "run", "--host", "0.0.0.0"]
```

### **3.0** Comandos

Aqui estão os principais comandos para rodar o backend usando Docker:

#### **3.1** Build da imagem

Este comando cria a imagem Docker a partir do Dockerfile:

```bash
docker build -t backend .
```

#### **3.2** Rodar o container

Este comando executa o container e mapeia a porta 8000 do container para a máquina local:

```bash
docker run -p 8000:8000 backend
```

#### **3.3** Parar o container

Para parar a execução do container:

```bash
docker stop backend

```

#### **3.4** Remover o container

Para remover o container:

```bash
docker rm backend
```

#### **3.5** Remover a imagem

Para remover a imagem:

```bash
docker rmi backend
```

### **4.0** Conclusão

A dockerização do backend do projeto garante um ambiente de desenvolvimento consistente, facilita a colaboração entre a equipe e torna a implantação mais ágil e segura. Através do uso de Docker e Docker Compose, o backend pode ser executado de forma eficiente e replicável em qualquer ambiente.

:::tip Vantagens da Dockerização do Backend

Ambientes consistentes em diferentes máquinas
Fácil escalabilidade e portabilidade
Menor chance de erros de configuração
:::