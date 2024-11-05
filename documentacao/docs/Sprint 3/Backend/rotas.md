---
title: "Rotas"
sidebar_position: 2
---

:::tip
Bruno é um cliente de API open-source rápido e amigável com Git, destinado a revolucionar o status quo representado por ferramentas como Postman, Insomnia e outras similares.
:::

Para maior detalhe de como funciona cada rota, basta importar a collections que está localizada em `src/backend/collections` no [`bruno`](https://docs.usebruno.com/get-started/import-export-data/export-collections). Todavia, as rotas também podem ser visualizadas através da documentação do `fastapi`, que fica localizada na rota: http://localhost:8000/docs quando o [projeto](/docs/Sprint%203/guia-de-execucao.md) é inicializado.

## Tabela das Rotas:

### KNR

O knr representa um veículo que está percorrendo a linha de produção. Um Exemplo de

| Rota             | Método | Ação                                                                                   | Parâmetro | Resposta                                    |
| ---------------- | ------ | -------------------------------------------------------------------------------------- | --------- | ------------------------------------------- |
| `/api/knr/`      | GET    | Retorna a lista de todos os knr armazenados.                                           | N/A       | Lista com todos os knrs armazenados         |
| `/api/knr/{knr}` | GET    | Recupera um knr específico a partir de seu identificador.                              | N/A       | Objeto de um knr requisitado                |
| `/api/knr/`      | POST   | Adiciona um novo knr ao banco de dados, assim como realiza a previsão de falhas nele . | KNR       | String com o id do KNR                      |
| `/api/knr/{knr}` | PUT    | Atualiza um knr específico a partir de seu identificador.                              | KNR       | Booleano dependendo do sucesso da operação. |
| `/api/knr/{knr}` | DELETE | Remove um knr específico a partir de seu identificador.                                | N/A       | Booleano dependendo do sucesso da operação. |

### Models

O models, representa um modelo de predição, juntamente com sua localização dentro do banco de dados.

| Rota                       | Método | Ação                                                         | Parâmetro | Resposta                                    |
| -------------------------- | ------ | ------------------------------------------------------------ | --------- | ------------------------------------------- |
| `/api/models/`             | GET    | Retorna a lista de todos os modelos armazenados.             | N/A       | Lista com todos os modelos armazenados      |
| `/api/models/{model_name}` | GET    | Recupera um modelo específico a partir de seu identificador. | N/A       | Objeto do modelo requisitado                |
| `/api/models/`             | POST   | Adiciona um novo modelo ao banco de dados.                   | model     | String com o nome do modelo                 |
| `/api/models/{model_name}` | PUT    | Atualiza um modelo específico a partir de seu identificador. | model     | Booleano dependendo do sucesso da operação. |
| `/api/models/{model_name}` | DELETE | Remove um modelo específico a partir de seu identificador.   | N/A       | Booleano dependendo do sucesso da operação. |

## Objetos de cada classe

### KNR

```json
{
  "example": {
    "KNR": "KNR123",
    "NAME": "Model A",
    "ID": 123,
    "STATUS": 1,
    "UNIT": "Unit123",
    "VALUE_ID": "Value001",
    "VALUE": "200",
    "DATA": "2024-01-01T12:00:00",
    "timestamp": "2024-09-10T15:30:00",
    "predicted_fails": ["fail1", "fail2"],
    "predicted_fail_code": [1, 2],
    "indicated_test": ["test1", "test2"],
    "real_fail": ["fail1", "fail2"],
    "real_fail_code": [1, 2]
  }
}
```

### Models

```json
{
  "example": {
    "model_name": "RandomForestModel_v1",
    "training_date": "2024-09-10T12:00:00",
    "gridfs_path": "/path/to/model/in/gridfs",
    "accuracy": 0.1,
    "precision": 0.2,
    "recall": 0.3,
    "f1_score": 0.4
  }
}
```
