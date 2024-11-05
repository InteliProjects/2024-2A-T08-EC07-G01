#
# 1. Backend
Aplicações web modernas são frequentemente divididas em diferentes camadas(ou _layers_) para melhor organização e escalabilidade. Uma arquitetura comum é dividir a aplicação em _layer_ de apresentação, _layer_ lógica e _layer_ de dados.

A camada de apresentação, também conhecida como interface do usuário, é responsável por exibir informações e interagir com os usuários. Já a camada lógica é responsável por processar as solicitações dos usuários, realizar a lógica de negócio e fornecer os dados necessários para a camada de apresentação. Por fim, a camada de dados, também conhecida como database, é responsável por armazenar e gerenciar os dados da aplicação, e pode ser implementada utilizando bancos de dados relacionais ou bancos de dados NoSQL.

Esta seção visa explicar um pouco sobre a camada lógica do projeto, também chamada **backend**, que serve para implementar as regras de negócio e fazer com que as outras camadas funcionem em conjunto.


# 1.1 Diagramas de sequência
Diagramas de sequência ilustram o fluxo de mensagens entre diferentes componentes de um sistema ao longo do tempo, ajudando a entender como as interações ocorrem. Os diagramas de sequência apresentados a seguir demonstram as interações entre os diferentes componentes do sistema, com ênfase no papel do backend. O backend, implementado com FastAPI, é responsável por gerenciar a lógica de negócio e coordenar a comunicação entre o usuário e o banco de dados MongoDB.

Em todos os diagramas, o backend atua como um intermediário essencial, processando requisições, validando dados, e garantindo que as operações sejam realizadas de forma eficiente e segura. Ele também assegura que as respostas apropriadas sejam enviadas de volta aos usuários, mantendo a integridade e consistência dos dados durante todo o fluxo de operação.

<div align="center">
  
**Diagrama de Sequência 1**

![Diagrama de Sequência 1](/img/seqDiagram01.png)

**Fonte:** Próprios autores

</div>
Neste primeiro diagrama, o Sistema Volkswagen envia uma requisição ao Backend contendo os dados do KNR. O backend realiza a validação necessária e prepara os dados para serem armazenados. Após a validação, o backend envia os dados do KNR para o Database.

<div align="center">
  
**Diagrama de Sequência 2**

![Diagrama de Sequência 2](/img/seqDiagram02.png)

**Fonte:** Próprios autores

</div>
Neste segundo diagrama de sequência, o Frontend solicita os resultados do KNR ao Backend. O Backend, após receber o pedido, persiste um log no Database para garantir a rastreabilidade das operações. Finalmente, o Backend envia uma previsão detalhada ao Frontend.

<div align="center">
  
**Diagrama de Sequência 3**

![Diagrama de Sequência 3](/img/seqDiagram03.png)

**Fonte:** Próprios autores

</div>
Neste terceiro diagrama de sequência, o Frontend (Vue+Typescript) envia uma requisição ao Backend (FastAPI) para obter dados históricos. O Backend, então, consulta o Database (MongoDB) para recuperar esses dados. Durante esse processo, o Backend também persiste um log no MongoDB. Após obter os dados históricos, o Backend retorna essas informações ao Frontend.

# 1.2 Tecnologias utilizadas
Havia várias tecnologias disponíveis para o backend, e a escolha foi baseada em critérios como facilidade de uso, desempenho e escalabilidade. Optamos por um banco de dados não estruturado para lidar com dados variados de forma flexível e eficiente. Também precisávamos de um framework moderno que oferecesse suporte a padrões abertos e integração rápida com outras plataformas.

### 1.2.1 Framework FastAPI
O FastAPI foi escolhido como o framework principal para a construção da API devido à sua simplicidade e alto desempenho. O FastAPI é ideal para aplicações que exigem alta capacidade de resposta e integração com diversos tipos de serviços, além de oferecer recursos nativos de validação de dados, documentação automática, e suporte a assinaturas de rotas baseadas em Python tipo anotado.

### 1.2.2 Banco de Dados MongoDB
O MongoDB foi selecionado como o banco de dados principal devido à sua flexibilidade e escalabilidade como um banco de dados NoSQL orientado a documentos. Ele é especialmente adequado para aplicações que lidam com dados semi-estruturados ou não estruturados, como é o caso dos dados desse projeto. Além disso, a escolha do MongoDB permite uma integração fluida com o FastAPI, utilizando bibliotecas assíncronas para operações de leitura e escrita, garantindo um desempenho eficiente.

# 1.3 Rotas
Endpoints, também chamados de rotas, são caminhos definidos em uma API que determinam como as solicitações dos usuários serão processadas pelo backend. Elas especificam o método HTTP a ser usado (como GET ou POST), a ação a ser executada, e quais dados serão retornados, funcionando como pontos de entrada para interações entre o cliente e o servidor.

### 1.3.1 `GET /api/knr/`
O seguinte endpoint define uma rota GET no caminho /api/knr/ para retornar uma lista de todos os modelos armazenados no banco de dados. A função get_all_models consulta o MongoDB para buscar modelos da coleção knr_collection e retornar a resposta no formato KNRCollection.

```python
@router.get(
    "/",
    response_model=KNRCollection,
    response_description="List of all models",
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
    tags=["KNR"],
)
async def get_all_models(request: Request):
    knrs = KNRCollection(
        knrs=await request.app.state.knr_collection.find().to_list(100)
    )
    print(knrs)
    print("00000000000000000000000")
    return knrs

```

### 1.3.2 `GET /api/knr/{knr}`

Este endpoint define uma rota GET no caminho `/api/knr/{knr}` para recuperar um modelo específico a partir do seu identificador. A função get_model consulta o MongoDB na coleção knr_collection usando o identificador fornecido e retorna a resposta no formato KNR.

```python

@router.get(
    "/{knr}",
    response_model=KNR,
    response_description="Get a single model",
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
    tags=["KNR"],
)
async def get_model(request: Request, knr: str):
    knr = await request.app.state.knr_collection.find_one({"knr": knr})
    print(knr)
    return KNR(**knr)

```

### 1.3.3 `POST /api/knr/`
Por fim, a rota POST no caminho `/api/knr/` adiciona um novo modelo ao banco de dados. A função add_model insere o modelo na coleção knr_collection do MongoDB e retorna a lista atualizada de todos os modelos no formato KNRCollection.

```python

@router.post(
    "/",
    response_model=KNRCollection,
    response_description="Add a new model",
    tags=["KNR"],
)
async def add_model(request: Request, knr: RegisterKNR):
    await request.app.state.knr_collection.insert_one(knr.model_dump())

    # retorna o model
    return KNRCollection(
        knrs=await request.app.state.knr_collection.find().to_list(100)
    )
     
```

### 1.3.4 Tabela resumo das rotas

| Rota | Método | Ação | Parâmetro | Resposta |
|-|-|-|-|-|
| `/api/knr/` | GET |Retorna a lista de todos os modelos armazenados.| N/A |Objeto com todos os modelos armazenados|
| `/api/knr/{knr}` | GET | Recupera um modelo específico a partir de seu identificador.| knr | Objeto do modelo requisitado |
| `/api/knr/` | POST | Adiciona um novo modelo ao banco de dados. | knr | Objeto da lista atualizada de todos os modelos. |




