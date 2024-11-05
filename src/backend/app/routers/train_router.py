from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from app.services.train_service import TrainServiceSingleton
from app.models.train import Train, ModelComparison, SelectModelRequest
import datetime

router = APIRouter(prefix="/api/train", tags=["Training"])

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
        # Use the train service to train the model and return the model metadata
        model_metadata = TrainServiceSingleton.get_instance().train_model(df_resultados, df_falhas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model training failed: {str(e)}")

    # Construct the response using the `Train` model
    return Train(
        model_name=model_metadata.get("model_name"),
        gridfs_path=model_metadata.get("gridfs_path", "default/gridfs/path"),  # Replace with actual path
        recipe_path=model_metadata.get("recipe_path", "default/recipe/path"),  # Replace with actual path
        type_model=model_metadata.get("type_model"),
        accuracy=model_metadata["metrics"].get("accuracy", 0.0),
        precision=model_metadata["metrics"].get("precision", 0.0),
        recall=model_metadata["metrics"].get("recall", 0.0),
        f1_score=model_metadata["metrics"].get("f1_score", 0.0),
        last_used=None,
        using=False,
        created_at=datetime.datetime.utcnow()
    )


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
    df_resultados = pd.read_csv("/app/app/pipeline/resultados.csv", compression='gzip')

    try:
        # Use the train service to retrain the model and get the comparison
        comparison = TrainServiceSingleton.get_instance().retrain_model(df_resultados, df_falhas)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model retraining failed: {str(e)}")
    return comparison

@router.post(
    "/select_model",
    response_description="Select a model to use"
)
async def select_model(
    request: SelectModelRequest
):
    model_name = request.model_name
    model_type = request.model_type
    try:
        TrainServiceSingleton.get_instance().select_model(model_name, model_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to select model: {str(e)}")
    return {"message": f"Model '{model_name}' is now in use."}