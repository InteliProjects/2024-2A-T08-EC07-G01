from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.db.mongodb import MongoDB

from app.repositories.knr_repo import KNRRepository
from app.services.knr_service import KNRServiceSingleton
from app.routers.knr_router import router as knr_router

from app.repositories.models_repo import ModelRepository
from app.services.models_service import ModelServiceSingleton
from app.routers.models_router import router as models_router


from app.routers.healthcheck_router import router as healthcheck_router

from app.repositories.predictions_repo import PredictionsRepository
from app.services.predictions_service import PredictionsServiceSingleton
from app.routers.predictions_router import router as predictions_router

from app.services.train_service import TrainServiceSingleton
from app.routers.train_router import router as train_router

from dotenv import dotenv_values

config = dotenv_values(".env")

DATABASE_URI = config.get("DATABASE_URI", "mongodb://db:27017")
DATABASE_NAME = config.get("DATABASE_NAME", "cross_the_line")


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    app.state.db = MongoDB(DATABASE_URI, DATABASE_NAME)

    KNRServiceSingleton.initialize(KNRRepository(app.state.db))
    ModelServiceSingleton.initialize(ModelRepository(app.state.db))
    PredictionsServiceSingleton.initialize(
        PredictionsRepository(app.state.db), KNRRepository(app.state.db)
    )
    TrainServiceSingleton.initialize(ModelRepository(app.state.db))

    print("Connected to the MongoDB database!")

    yield

    app.state.db.close()
    print("Disconnected to the MongoDB database!")


app = FastAPI(lifespan=app_lifespan)

origins = [
        "http://localhost:3000",
        "http://localhost:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(knr_router)
app.include_router(models_router)
app.include_router(healthcheck_router)
app.include_router(predictions_router)
app.include_router(train_router)


@app.get("/")
async def read_root():
    return {"message": "crossing the line!"}
