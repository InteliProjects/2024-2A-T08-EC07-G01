from fastapi import APIRouter, HTTPException
from typing import List
from app.models.predictions import Prediction, PredictionUpdate
from app.models.knr import KNR
from app.services.predictions_service import PredictionsServiceSingleton
from app.utils.fail_code import FailCodeByMonthRequest

router = APIRouter(prefix="/api/predictions", tags=["Predictions"])


@router.get(
    "/",
    response_model=List[Prediction],
    response_description="List of all predictions",
)
async def get_all_predictions():
    predictions = PredictionsServiceSingleton.get_instance().get_all_predictions()
    return predictions


@router.get(
    "/details/{knr}",
    response_model=Prediction,
    response_description="Get information about a specific prediction",
)
async def get_prediction(knr: str):
    prediction = PredictionsServiceSingleton.get_instance().get_prediction(knr)

    if prediction is None:
        raise HTTPException(status_code=404, detail="Prediction not found")

    return prediction


@router.post(
    "/",
    response_model=Prediction,
    response_description="Predict the failure codes for a given KNR",
)
async def predict_fail_codes(knr: KNR):
    prediction = PredictionsServiceSingleton.get_instance().predict(knr)
    return prediction


@router.put(
    "/{knr_id}",
    response_model=PredictionUpdate,
    response_description="Update the failure codes for a given KNR",
)
async def update_fail_codes(knr_id: str, prediction: PredictionUpdate):
    existing_prediction = PredictionsServiceSingleton.get_instance().get_prediction(
        knr_id
    )

    if not existing_prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")

    PredictionsServiceSingleton.get_instance().update_prediction(knr_id, prediction)

    updated_prediction = PredictionsServiceSingleton.get_instance().get_prediction(
        knr_id
    )

    return updated_prediction


@router.get(
    "/fail-codes-predicted",
    response_model=dict,
    response_description="List of the quantity of each possible failure codes was predicted",
)
async def get_fail_codes_predicted():
    fail_codes_predicted = (
        PredictionsServiceSingleton.get_instance().fail_codes_prediction()
    )
    return fail_codes_predicted


@router.get(
    "/total-fails",
    response_model=dict,
    response_description="Total of fails and no fails predicted",
)
async def get_total_fails():
    total_fails = PredictionsServiceSingleton.get_instance().total_fails()
    return total_fails


@router.post(
    "/fail-codes-by-month",
    response_model=dict,
    response_description="List of the quantity of each possible failure codes was predicted by month",
)
async def get_fail_codes_by_month(request: FailCodeByMonthRequest):
    fail_code_count = (
        PredictionsServiceSingleton.get_instance().get_fail_code_count_by_month(
            request.year, request.fail_code
        )
    )
    return fail_code_count
