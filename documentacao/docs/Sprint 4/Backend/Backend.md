---
title: "Alterações Backend"
sidebar_position: 1
---

# **1.1** - Introdução

Durante a quarta Sprint, o projeto passou por uma série de aprimoramentos visando a implementação de novas funcionalidades. Um dos principais focos foi a inclusão da pipeline de treinamento e retreinamento do modelo, uma etapa fundamental para melhorar a eficiência e precisão das previsões realizadas. No entanto, para acomodar essa funcionalidade, foi necessário adaptar a estrutura do backend, garantindo que ele suportasse essas novas operações de forma eficiente.

As alterações realizadas no backend incluíram a adição de um novo roteador, um elemento crucial para organizar e direcionar as requisições relacionadas ao treinamento do modelo. Essa mudança foi cuidadosamente planejada para preservar a integridade das operações existentes, garantindo que a integração das novas funcionalidades não comprometesse o desempenho atual. Assim, foi possível assegurar que o backend continuasse funcionando corretamente, mesmo com a inclusão de funcionalidades mais complexas.

Além de atender às necessidades imediatas do projeto, essa reformulação do backend contribui para a escalabilidade a longo prazo. A inclusão de um roteador dedicado facilita a manutenção e a expansão futura do sistema, tornando-o mais adaptável a novas demandas. Dessa forma, as modificações realizadas não apenas aprimoram a funcionalidade atual, mas também preparam o projeto para futuras evoluções, assegurando um desenvolvimento sustentável.

## **2.1** - Novo repository de previsões

Para implementar essa funcionalidade, foi criado um `Predictions Repository`, responsável por armazenar as previsões geradas pelo modelo no banco de dados. Esse repositório centraliza o gerenciamento de previsões, facilitando seu armazenamento e acesso de forma organizada. A seguir, cada parte do código será detalhada para esclarecer seu funcionamento e propósito.

:::info 
Mais abaixo haverá o código completo desta parte afim de melhorar o entendimento.
:::

### **2.1.1** - Adquirir as previsões

Para adquirir as previsões, foi criado um método `get_all_predictions` que retorna todas as previsões armazenadas no banco de dados. Esse método é essencial para recuperar as previsões geradas pelo modelo, permitindo que sejam exibidas e utilizadas conforme necessário. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def get_all_predictions(self) -> List[Prediction]:
        documents = self.collection.find()
        return [Prediction(**document) for document in documents]
```

:::warning
A estrutura que ele retorna `Prediction` foi explicada anteriormente em Base de Dados.
:::

### **2.1.2** - Adicionar previsões

Para adicionar previsões, foi criado um método `create_prediction` que insere uma nova previsão no banco de dados. Esse método é fundamental para armazenar as previsões geradas pelo modelo, garantindo que estejam disponíveis para consulta posterior. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def create_prediction(self, prediction_info: Prediction) -> str:
        self.collection.insert_one(prediction_info.model_dump(by_alias=True))
        return str(prediction_info.KNR)
```

### **2.1.3** - Adquirir uma predição

Para adquirir uma previsão específica, foi criado um método `get_prediction` que retorna a previsão correspondente ao **KNR** fornecido. Esse método é essencial para recuperar previsões específicas, permitindo que sejam acessadas e utilizadas conforme necessário. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def get_prediction(self, knr_id: str) -> Optional[Prediction]:
        document = self.collection.find_one({"KNR": knr_id})
        return Prediction(**document) if document else None
```

### **2.1.4** - Atualizar uma previsão

Para atualizar uma previsão, foi criado um método `update_prediction` que modifica a previsão correspondente ao **KNR** fornecido. Esse método é fundamental para atualizar previsões existentes, garantindo que estejam sempre atualizadas e precisas. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def update_prediction(self, knr_id: str, prediction_info: PredictionUpdate) -> bool:
        result = self.collection.update_one(
            {"KNR": knr_id},
            {"$set": prediction_info.model_dump(exclude_unset=True, by_alias=True)},
        )
        return result.modified_count > 0
```

### **2.1.5** - Deletar uma previsão

Para deletar uma previsão, foi criado um método `delete_prediction` que remove a previsão correspondente ao **KNR** fornecido. Esse método é essencial para excluir previsões indesejadas, garantindo que o banco de dados permaneça organizado e atualizado. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def delete_prediction(self, knr_id: str) -> bool:
        result = self.collection.delete_one({"KNR": knr_id})
        return result.deleted_count > 0
```

### **2.1.6** - Código completo

A seguir, o código completo da classe `PredicitionsRepository` será apresentado para ilustrar sua implementação. Esse código reúne todos os métodos criados para gerenciar as previsões, garantindo que estejam armazenadas e acessíveis conforme necessário.

```python
class PredictionsRepository:
    def __init__(self, db: MongoDB):
        self.db = db
        self.collection = db.get_collection("predictions")

    def get_all_predictions(self) -> List[Prediction]:
        documents = self.collection.find()
        return [Prediction(**document) for document in documents]

    def create_prediction(self, prediction_info: Prediction) -> str:
        self.collection.insert_one(prediction_info.model_dump(by_alias=True))
        return str(prediction_info.KNR)

    def get_prediction(self, knr_id: str) -> Optional[Prediction]:
        document = self.collection.find_one({"KNR": knr_id})
        return Prediction(**document) if document else None

    def update_prediction(self, knr_id: str, prediction_info: PredictionUpdate) -> bool:
        result = self.collection.update_one(
            {"KNR": knr_id},
            {"$set": prediction_info.model_dump(exclude_unset=True, by_alias=True)},
        )
        return result.modified_count > 0

    def delete_prediction(self, knr_id: str) -> bool:
        result = self.collection.delete_one({"KNR": knr_id})
        return result.deleted_count > 0
```

:::warning
No código acima está apenas a classe, os imports foram **omitidos** para melhor entendimento. Caso queira analisar o código inteiro, acesse o [repositório](https://github.com/Inteli-College/2024-2A-T08-EC07-G01)
:::

## **3.1** - Novo serviço de previões

Foram desenvolvidos tanto um serviço para previsões quanto um repositório para armazená-las. O serviço gerencia todas as operações relacionadas às previsões, assegurando que elas sejam realizadas de maneira eficiente e segura. Este serviço atua como uma interface central para o processamento de previsões, facilitando a organização e a execução correta das tarefas. A seguir, serão detalhadas as partes do código, destacando seu funcionamento e propósito.

Além disso, foi implementado um Singleton para garantir que apenas uma instância do serviço seja criada. Essa abordagem evita duplicações e assegura a consistência das operações, prevenindo possíveis conflitos e melhorando a eficiência geral do sistema. Essa escolha arquitetural é essencial para manter a integridade dos dados e a confiabilidade do serviço.

Por fim, cada componente do código será analisado em detalhes, oferecendo uma visão abrangente de seu papel e funcionamento. Essa explicação permitirá compreender o fluxo completo das previsões, desde sua geração até o armazenamento no repositório.

### **3.1.1** - Serviço adquirir previsões

Para adquirir previsões, foi criado um método `get_all_predictions` que retorna todas as previsões armazenadas no repositório. Esse método é essencial para recuperar as previsões geradas pelo modelo, permitindo que sejam exibidas e utilizadas conforme necessário. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def get_all_predictions(self) -> List[Prediction]:
        return self.predict_repo.get_all_predictions()
```

### **3.1.2** - Serviço pegar uma previsão

Para pegar uma previsão específica, foi criado um método `get_prediction` que retorna a previsão correspondente ao **KNR** fornecido. Esse método é essencial para recuperar previsões específicas, permitindo que sejam acessadas e utilizadas conforme necessário. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def get_prediction(self, knr: str) -> Optional[Prediction]:
        return self.predict_repo.get_prediction(knr)
```

### **3.1.3** - Serviço adicionar uma previsão

Afim de adicionar/criar uma nova previsão, foi criado um método `predict` que insere uma nova previsão no repositório. Esse método é fundamental para armazenar as previsões geradas pelo modelo, garantindo que estejam disponíveis para consulta posterior. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def predict(self, knr: KNR) -> Prediction:
        df_input = pd.DataFrame([knr.dict()])

        pipeline_file_path = os.path.join(os.getcwd(), 'app', 'pipeline', 'pipeline_principal.json')
        with open(pipeline_file_path, "r") as file:
            pipeline_config = json.load(file)

        # Passos de previsão
        steps = pipeline_config.get("predict_steps", [])

        dataframes = {
        "df_input": df_input
        }

        orchestrator = Orchestrator(
            pipeline_steps=steps,
            dataframes=dataframes,
            mongo_uri="mongodb://db:27017",
            db_name="cross_the_line"
        )

        orchestrator.run_dynamic_pipeline()

        prediction = orchestrator.dataframes.get("prediction_result")

        response = Prediction(
        KNR= knr.KNR,
        predicted_fail_codes = [prediction],
        real_fail_codes = [-1], 
        indicated_tests = [""]  
        )
        return response
```

O método acima, chama o orquestrador, que por sua vez chama o script de Previsão, que é responsável por realizar a previsão. O orquestrador é responsável por chamar os scripts de acordo com o pipeline, que é um arquivo JSON que contém a ordem dos scripts que devem ser chamados.

### **3.1.4** - Serviço atualizar uma previsão

Para atualizar uma previsão, foi criado um método `update_prediction` que modifica a previsão correspondente ao **KNR** fornecido. Esse método é fundamental para atualizar previsões existentes, garantindo que estejam sempre atualizadas e precisas. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def update_prediction(self, knr: str, prediction: PredictionUpdate) -> bool:
        return self.predict_repo.update_prediction(knr, prediction)
```

### **3.1.5** - Serviço deletar uma previsão

Para deletar uma previsão, foi criado um método `delete_prediction` que remove a previsão correspondente ao **KNR** fornecido. Esse método exclui previsões indesejadas, garantindo que o repositório permaneça organizado e atualizado. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def delete_prediction(self, knr: str) -> bool:
        return self.predict_repo.delete_prediction(knr)
```

### **3.1.6** - Código completo

A seguir, o código completo da classe `PredictionsService` será apresentado para ilustrar sua implementação. Esse código reúne todos os métodos criados para gerenciar as previsões, garantindo que estejam armazenadas e acessíveis conforme necessário.

```python
class PredictionService:
    def __init__(self, predict_repo: PredictionsRepository):
        self.predict_repo = predict_repo

    def get_all_predictions(self) -> List[Prediction]:
        return self.predict_repo.get_all_predictions()

    def get_prediction(self, knr: str) -> Optional[Prediction]:
        return self.predict_repo.get_prediction(knr)

    def predict(self, knr: KNR) -> Prediction:
        # TODO: call the predictions function
        return Prediction(knr.KNR)

    def update_prediction(self, knr: str, prediction: PredictionUpdate) -> bool:
        return self.predict_repo.update_prediction(knr, prediction)

    def delete_prediction(self, knr: str) -> bool:
        return self.predict_repo.delete_prediction(knr)
```

### **3.1.7** - Singleton

Para garantir que apenas uma instância do serviço seja criada, foi implementado um Singleton. Essa abordagem evita duplicações e assegura a consistência das operações, prevenindo possíveis conflitos e melhorando a eficiência geral do sistema. A seguir, o código completo do Singleton será apresentado para ilustrar sua implementação.

```python
class PredictionsServiceSingleton:
    _instance: Optional[PredictionService] = None

    def __init__(self, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    @classmethod
    def initialize(cls, predict_repo: PredictionsRepository):
        if cls._instance is None:
            cls._instance = PredictionService(predict_repo)

    @classmethod
    def get_instance(cls) -> PredictionService:
        if cls._instance is None:
            raise Exception(
                "ModelServiceSingleton is not initialized. Call initialize() first."
            )

        return cls._instance
```

:::info
Foi utilizado o padrão Singleton para garantir que apenas uma instância do serviço seja criada. Isso evita duplicações e assegura a consistência das operações, prevenindo possíveis conflitos e melhorando a eficiência geral do sistema.
:::

## **4.1** - Mudanças feitas para implementar treino e retreino

Para implementar a pipeline de treinamento e retreinamento do modelo, foram realizadas diversas mudanças no backend. Essas alterações visaram aprimorar a estrutura do projeto, garantindo que ele suportasse as novas operações de forma eficiente e organizada. A seguir, cada parte do código será detalhada para esclarecer seu funcionamento e propósito.

### **4.1.1** - Mudanças model de Modelos

Para acomodar as operações de treinamento e retreinamento do modelo, foi necessário adicionar novos campos ao modelo `Model`. Esses campos são essenciais para armazenar informações relevantes sobre o treinamento, como a data de início e término, o status da operação e os resultados obtidos. A seguir, o código completo do modelo `Model` será apresentado para ilustrar as mudanças realizadas.

```python
class Model(BaseModel):
    model_name: str = Field(..., description="Name of the trained model")
    gridfs_path: str = Field(..., description="Path in GridFS where the model is stored")
    recipe_path: str = Field(..., description="Path in GridFS where the recipe is stored")
    type_model: str = Field(..., description="Type of the model")
    accuracy: float = Field(..., description="Accuracy of the model")
    precision: float = Field(..., description="Precision of the model")
    recall: float = Field(..., description="Recall of the model")
    f1_score: float = Field(..., description="F1 score of the model")
    last_used: Optional[datetime] = Field(None, description="Date when the model was last used")
    using: bool = Field(..., description="If the model is being used")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Date when the model was created")

    class Config:
        json_schema_extra = {
	@@ -34,10 +27,13 @@ class Config:
                "recall": 0.30,
                "f1_score": 0.40,
                "last_used": "2024-09-10T12:00:00",
                "using": True,
                "created_at": "2024-09-10T12:00:00"
            }
```

Foram adicionadas as seguintes propriedades ao modelo `Model`:

- `using`: Indica se o modelo está sendo utilizado atualmente.
- `created_at`: Data de criação do modelo.

### **4.1.2** - Novo `model` de Treino

O mesmo segue o mesmo princípio do `model` de Modelos, todavia ele possui 2 novas classes que são `ModelMetrics` e `ModelComparison`, que são responsáveis por armazenar as métricas do modelo e a comparação entre os modelos respectivamente. A seguir, o código completo do modelo `Training` será apresentado para ilustrar as mudanças realizadas.

```python
class Train(BaseModel):
    model_name: str = Field(..., description="Name of the trained model")
    gridfs_path: str = Field(
        ..., description="Path in GridFS where the model is stored"
    )
    recipe_path: str = Field(
        ..., description="Path in GridFS where the recipe is stored"
    )

    type_model: str = Field(..., description="Name of the trained model")
    accuracy: float = Field(..., description="Accuracy of the model")
    precision: float = Field(..., description="Precision of the model")
    recall: float = Field(..., description="Recall of the model")
    f1_score: float = Field(..., description="F1 score of the model")

    last_used: Optional[datetime] = Field(
        None, description="Date when the model was last used"
    )
    using: bool = Field(..., description="If the model is being used")


class ModelMetrics(BaseModel):
    accuracy: float
    precision: float
    recall: float
    f1_score: float

class ModelComparison(BaseModel):
    new_model_metrics: ModelMetrics
    last_model_metrics: Optional[ModelMetrics] = None
    differences: Optional[ModelMetrics] = None
    message: Optional[str] = None



    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "RandomForestModel_v1",
                "type_model": "Type 1",
                "gridfs_path": "/path/to/model/in/gridfs",
                "recipe_path": "/path/to/recipe/in/gridfs",
                "accuracy": 0.10,
                "precision": 0.20,
                "recall": 0.30,
                "f1_score": 0.40,
                "last_used": "2024-09-10T12:00:00",
                "using": True,
            }
        }
```

A classe ModelMetrics é responsável por armazenar as métricas do modelo, enquanto a classe ModelComparison é responsável por armazenar a comparação entre os modelos. Essas classes são essenciais para avaliar o desempenho dos modelos e identificar possíveis melhorias.

:::info
A informação a respeito de onde serão utilizadas as classes será mostrada mais abaixo neste documento.
:::

### **4.1.3** - Mudanças repository de modelos

Para acomodar as operações de treinamento e retreinamento do modelo, foi necessário adicionar novos métodos ao repositório de modelos. Esses métodos são essenciais para gerenciar as operações de treinamento, garantindo que sejam realizadas de maneira eficiente e organizada. A seguir, serão apresentados os novos métodos adicionados ao repositório de modelos.

#### **4.1.3.1** - Adquirir modelos por tipo

Foi criado um método `get_models_by_type` que retorna todos os modelos de um determinado tipo. Esse método é essencial para recuperar os modelos de um tipo específico, permitindo que sejam exibidos e utilizados conforme necessário. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def get_models_by_type(self, model_type: str) -> list[Model]:
        documents = self.collection.find({"type_model": model_type})
        return [Model(**document) for document in documents]
```

#### **4.1.3.2** Adquirir modelo atual

Foi criado um método `get_current_models` que retorna o modelo atualmente em uso. Esse método é essencial para recuperar o modelo em uso, permitindo que seja acessado e utilizado conforme necessário. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def get_current_models(self) -> list[Model]:
        documents = self.collection.find({"using": True})
        return [Model(**document) for document in documents]
```

#### **4.1.3.3** Adquirir ultimo modelo criado

Foi criado um método `get_last_model` que retorna o último modelo criado. Esse método serve para recuperar o último modelo criado, permitindo que seja acessado e utilizado conforme necessário, além de garantir a escolha de modelos ao usuário. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def get_latest_model(self) -> Optional[Model]:
        document = self.collection.find_one(sort=[('_id', -1)])
        return Model(**document) if document else None
```

#### **4.1.3.4** Atualizar modelos para não estarem sendo usados

Foi criado um método `unset_all_using` que atualiza todos os modelos para não estarem sendo usados. Esse método garante que apenas um modelo esteja sendo utilizado, evitando conflitos e garantindo a integridade dos dados. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def unset_all_using(self):
        self.collection.update_many({}, {'$set': {'using': False}})
```

#### **4.1.3.5** Atualizar modelo para estar sendo usado

Foi criado um método `set_model_using` que atualiza um modelo para estar sendo usado. Esse método define qual modelo está sendo utilizado, permitindo que seja acessado e utilizado conforme necessário. A seguir, o código completo desse método será apresentado para ilustrar sua implementação.

```python
def set_model_using(self, model_name: str):
        result = self.collection.update_one({'model_name': model_name}, {'$set': {'using': True}})
        if result.matched_count == 0:
            raise ValueError(f"Model '{model_name}' not found.")
```

### **4.1.4** - Nova rota no roteador de modelos

Para acomodar as operações de treinamento e retreinamento do modelo, foi criada uma nova rota para adquirir o modelo em uso atualmente. Essa rota é essencial para recuperar o modelo em uso, permitindo que seja acessado e utilizado conforme necessário. A seguir, o código completo da nova rota será apresentado para ilustrar sua implementação.

```python
@router.get(
    "/current-models",
    response_model=List[Model],
    response_description="Get all models currently in use",
)
async def get_current_models():
    models = ModelServiceSingleton.get_instance().get_current_models()
    return models
```

### **4.1.5** - Novo roteador de treino

Para acomodar as operações de treinamento e retreinamento do modelo, foi criado um novo roteador para gerenciar essas operações. Esse roteador é necessário para direcionar as requisições relacionadas ao treinamento, garantindo que sejam processadas de maneira eficiente e organizada. A seguir, será apresentado o código em partes para ilustrar a implementação do novo roteador.

#### **4.1.5.1** Rota de treino

Foi criada uma nova rota `/api/train` que permite treinar um modelo com base dataframe de **falhas** fornecidos. Essa rota é usada para iniciar o processo de treinamento, garantindo que o modelo seja atualizado e aprimorado conforme necessário. A seguir, o código completo da nova rota será apresentado para ilustrar sua implementação.

```python

@router.post(
    "/",
    response_description="Train a model",
    response_model=Train
)
async def train_model(
    df_falhas: UploadFile = File(...),
):
    df_falhas_content = await df_falhas.read()
    df_falhas = pd.read_csv(BytesIO(df_falhas_content))
    df_resultados = pd.read_csv("/app/app/pipeline/resultados.csv")

    try:
        model_metadata = TrainServiceSingleton.get_instance().train_model(df_resultados, df_falhas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")

    return {"message": f"Model '{model_metadata['model_name']}' trained successfully."}
```

:::warning
Foi levado em consideração, que o dataframe de resultados já estará no sistema da Volkswagen, por isso **não foi necessário** o upload do mesmo na hora do treino. Todavia ao realizar o treino, é necessário que o mesmo esteja presente no sistema por meio de uma `API` externa.
:::

#### **4.1.5.2** Rota de retreino

Foi criada uma nova rota `/api/train/retrain` que permite retreinar um modelo com base dataframe de **falhas** fornecidos. Essa rota é utilizada para iniciar o processo de retreinamento, garantindo que o modelo seja atualizado e aprimorado conforme necessário. A seguir, o código completo da nova rota será apresentado para ilustrar sua implementação.

```python
@router.post(
    "/retrain",
    response_description="Retrain the model",
    response_model=ModelComparison
)
async def retrain_model(
    df_falhas: UploadFile = File(...),
):
    df_falhas_content = await df_falhas.read()
    df_falhas = pd.read_csv(BytesIO(df_falhas_content))
    df_resultados = pd.read_csv("/app/app/pipeline/resultados.csv")

    try:
        # Use the train service to retrain the model and get the comparison
        comparison = TrainServiceSingleton.get_instance().retrain_model(df_resultados, df_falhas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model retraining failed: {str(e)}")

    return comparison
```

Este código retorna a comparação entre o novo modelo e o modelo anterior, permitindo avaliar as melhorias e ajustes realizados durante o retreinamento. Possibilitando ao usuário a escolha do modelo que melhor se adequa às suas necessidades.

#### **4.1.5.3** Escolha modelo

Por fim, foi criada uma nova rota `/api/train/select_model` que permite escolher um modelo para ser utilizado. Essa rota define qual modelo será utilizado, garantindo que apenas um modelo esteja em uso. A seguir, o código completo da nova rota será apresentado para ilustrar sua implementação.

```python
@router.post(
    "/select_model",
    response_description="Select a model to use"
)
async def select_model(
    model_name: str
):
    try:
        TrainServiceSingleton.get_instance().select_model(model_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to select model: {str(e)}")
    return {"message": f"Model '{model_name}' is now in use."}
```

:::info
A rota de selecionar o modelo deverá ser chamada **logo após a rota de retreino**. Por isso que a rota de retreino não retorna o modelo, mas sim a comparação entre os modelos.
:::

### **4.1.6** - Mudanças serviço de modelo

Para acomodar as operações de treinamento e retreinamento do modelo, foi necessário adicionar um novo método ao serviço. O mesmo serve para adquirir o modelo em uso atualmente. Esse método recupera o modelo em uso, permitindo que seja acessado e utilizado conforme necessário. A seguir, o código completo do novo método será apresentado para ilustrar sua implementação.

```python
def get_current_models(self) -> List[Model]:
        return self.model_repo.get_current_models()
```

### **4.1.7** - Criação do serviço de treino

Para acomodar as operações de treinamento e retreinamento do modelo, foi criado um novo serviço para gerenciar essas operações. Esse serviço coordena o treinamento e retreinamento do modelo, garantindo que sejam realizados de maneira eficiente e organizada. A seguir, será apresentado o código em partes para ilustrar a implementação do novo serviço.

#### **4.1.7.1** Classe principal

Foi criada a classe `TrainService` que gerencia as operações de treinamento e retreinamento do modelo. Essa classe é essencial para coordenar as etapas do processo, garantindo que sejam executadas corretamente e com eficiência. A seguir, o código completo da classe será apresentado para ilustrar sua implementação.

```python
class TrainService:
    def __init__(self, model_repo: ModelRepository):
        self.model_repo = model_repo

    def train_model(self, df_resultados: pd.DataFrame, df_falhas: pd.DataFrame) -> dict:
        '''
        Método para treinar um modelo com base nos dataframes de resultados e falhas fornecidos.

        Args:
            df_resultados (pd.DataFrame): Dataframe de resultados.
            df_falhas (pd.DataFrame): Dataframe de falhas.
        '''
        pipeline_file_path = os.path.join(os.getcwd(), 'app', 'pipeline', 'pipeline_principal.json')
        print("Absolute Path to JSON file:", pipeline_file_path)

        with open(pipeline_file_path, "r") as file:
            pipeline_config = json.load(file)

        steps = pipeline_config.get("prediction_steps", []) + pipeline_config.get("training_steps", [])

        dataframes = {
            "df_resultados": df_resultados,
            "df_falhas": df_falhas,
        }

        orchestrator = Orchestrator(
            pipeline_steps=steps,
            dataframes=dataframes,
            mongo_uri="mongodb://db:27017",
            db_name="cross_the_line",
        )

        model_metadata = orchestrator.run_dynamic_pipeline()

        new_model = Model(
            model_name=model_metadata.get("model_name"),
            type_model=model_metadata.get("type_model"),
            gridfs_path="path/to/model/in/gridfs",  # TODO: Replace with actual GridFS path
            recipe_path="path/to/recipe/in/gridfs",  # TODO: Replace with actual GridFS path
            accuracy=model_metadata["metrics"].get("accuracy", 0.0),
            precision=model_metadata["metrics"].get("precision", 0.0),
            recall=model_metadata["metrics"].get("recall", 0.0),
            f1_score=model_metadata["metrics"].get("f1", 0.0),
            last_used=None,  # TODO: You can set this to `datetime.datetime.utcnow()` if needed
            using=False 
        )

        
        try:
            self.model_repo.create_model(new_model)
            print(f"[INFO] Model '{new_model.model_name}' saved to repository.")
        except Exception as e:
            raise RuntimeError(f"Failed to save model: {str(e)}")

        return model_metadata

    def retrain_model(self, df_resultados: pd.DataFrame, df_falhas: pd.DataFrame) -> dict:
        '''
        Método para retreinar um modelo com base nos dataframes de resultados e falhas fornecidos.

        Args:
            df_resultados (pd.DataFrame): Dataframe de resultados.
            df_falhas (pd.DataFrame): Dataframe de falhas.
        '''
        pipeline_file_path = os.path.join(os.getcwd(), 'app', 'pipeline', 'pipeline_principal.json')
        print("Absolute Path to JSON file:", pipeline_file_path)

        with open(pipeline_file_path, "r") as file:
            pipeline_config = json.load(file)

        steps = pipeline_config.get("prediction_steps", []) + pipeline_config.get("training_steps", [])

        dataframes = {
            "df_resultados": df_resultados,
            "df_falhas": df_falhas,
        }

        orchestrator = Orchestrator(
            pipeline_steps=steps,
            dataframes=dataframes,
            mongo_uri="mongodb://db:27017",
            db_name="cross_the_line",
        )

        new_model_metadata = orchestrator.run_dynamic_pipeline()

        new_model = Model(
            model_name=new_model_metadata.get("model_name"),
            type_model=new_model_metadata.get("type_model"),
            gridfs_path="path/to/model/in/gridfs",  # TODO: Replace with actual GridFS path
            recipe_path="path/to/recipe/in/gridfs",  # TODO: Replace with actual GridFS path
            accuracy=new_model_metadata["metrics"].get("accuracy", 0.0),
            precision=new_model_metadata["metrics"].get("precision", 0.0),
            recall=new_model_metadata["metrics"].get("recall", 0.0),
            f1_score=new_model_metadata["metrics"].get("f1_score", 0.0),
            last_used=None,
            using=False,
            created_at=datetime.datetime.utcnow()
        )

        try:
            self.model_repo.create_model(new_model)
            print(f"[INFO] New model '{new_model.model_name}' saved to repository.")
        except Exception as e:
            raise RuntimeError(f"Failed to save new model: {str(e)}")

        last_model = self.model_repo.get_latest_model()

        if last_model and last_model.model_name != new_model.model_name:
            comparison = self.compare_models(new_model_metadata, last_model)
        else:
            comparison = {
                "message": "No previous model to compare with.",
                "new_model_metrics": new_model_metadata["metrics"]
            }

        return comparison

    def compare_models(self, new_model_metadata, last_model) -> dict:
        '''
        Método para comparar as métricas do novo modelo com o modelo anterior.

        Args:
            new_model_metadata (dict): Metadata of the new model.
            last_model (Model): Metadata of the last model.
        '''
        new_metrics = new_model_metadata["metrics"]
        last_metrics = {
            "accuracy": last_model.accuracy,
            "precision": last_model.precision,
            "recall": last_model.recall,
            "f1_score": last_model.f1_score
        }

        differences = {}
        for metric in new_metrics:
            new_value = new_metrics[metric]
            last_value = last_metrics.get(metric, 0.0)
            differences[metric] = new_value - last_value

        comparison = {
            "new_model_metrics": new_metrics,
            "last_model_metrics": last_metrics,
            "differences": differences
        }

        return comparison

    def select_model(self, model_name: str):
        self.model_repo.unset_all_using()
        self.model_repo.set_model_using(model_name)
```

Essa classe é essencial, pois é a responsável por chamar o orquestrador afim de treinar e retreinar o modelo, além de salvar o modelo no banco de dados. Elá também é capaz de comparar os modelos e selecionar o modelo que será utilizado.

#### **4.1.7.2** Singleton

Foi implementado um Singleton para garantir que apenas uma instância do serviço seja criada. Essa abordagem evita duplicações e assegura a consistência das operações, prevenindo possíveis conflitos e melhorando a eficiência geral do sistema. A seguir, o código completo do Singleton será apresentado para ilustrar sua implementação.

:::info

O código do mesmo pode ser visto mais acima na documentação
:::


## **5.1** - Conclusão

As alterações no backend desempenharam um papel crucial no desenvolvimento do projeto, adicionando funcionalidades fundamentais para o processo de treinamento e retreinamento do modelo preditivo. A adição do `Predictions Repository` e do `Predictions Service` forneceu uma arquitetura bem estruturada para gerenciar as previsões, permitindo uma fácil manutenção e escalabilidade. Além disso, a inclusão de rotas específicas para operações de treinamento, retreinamento e seleção de modelos garantiu que o processo de aprimoramento dos modelos fosse eficiente e integrado ao fluxo geral do projeto.

A implementação de padrões como o Singleton foi uma escolha arquitetural estratégica que assegurou a consistência das operações e evitou duplicações desnecessárias de serviços. Isso não apenas melhorou a eficiência do sistema, mas também garantiu a integridade dos dados durante operações críticas como o treino e o retreino dos modelos. As mudanças nas estruturas de dados, como os modelos `Model`, `Train`, `ModelMetrics`, e `ModelComparison`, forneceram uma base sólida para armazenar e comparar os resultados dos modelos, facilitando a avaliação de seu desempenho e evolução.

Por fim, as alterações realizadas no backend não apenas atenderam às necessidades atuais do projeto, mas também estabeleceram um alicerce robusto para futuras evoluções. A modularidade e flexibilidade das novas funcionalidades permitirão que o sistema se adapte a novas demandas com facilidade, assegurando um desenvolvimento sustentável e preparado para o crescimento. Dessa forma, o backend foi aprimorado para ser mais eficiente, seguro e preparado para lidar com operações mais complexas, garantindo uma experiência de uso mais fluida e organizada.