from datetime import datetime
from app.models.predictions import Prediction, PredictionUpdate
from app.models.knr import KNR
from app.models.predictions import Prediction
from app.repositories.predictions_repo import PredictionsRepository
from app.repositories.knr_repo import KNRRepository
from typing import Optional, List
from app.pipeline.orchestrator import Orchestrator
import pandas as pd
import os
import json
from app.utils.predict import mock_prediction
from collections import Counter


# TODO: Completar predict Service
class PredictionService:
    def __init__(self, predict_repo: PredictionsRepository, knr_repo: KNRRepository):
        self.predict_repo = predict_repo
        self.knr_repo = knr_repo

    def get_all_predictions(self) -> List[Prediction]:
        return self.predict_repo.get_all_predictions()

    def get_prediction(self, knr: str) -> Optional[Prediction]:
        return self.predict_repo.get_prediction(knr)

    def predict(self, knr: KNR) -> Prediction:
        # Convert KNR object to DataFrame
        df_input = pd.DataFrame([knr.dict()])

        # Load the main pipeline configuration
        main_pipeline_file_path = os.path.join(os.getcwd(), 'app', 'pipeline', 'pipeline_principal.json')
        with open(main_pipeline_file_path, "r") as file:
            main_pipeline_config = json.load(file)

        main_steps = main_pipeline_config.get("predict_steps", [])

        # Prepare dataframes for the orchestrator
        dataframes = {
            "df_input": df_input
        }

        # Create an orchestrator for the main pipeline
        main_orchestrator = Orchestrator(
            pipeline_steps=main_steps,
            dataframes=dataframes,
            mongo_uri="mongodb://db:27017",
            db_name="cross_the_line"
        )

        # Run the main prediction pipeline
        main_orchestrator.run_dynamic_pipeline()

        # Get the prediction result from the orchestrator's results
        main_prediction = main_orchestrator.dataframes.get("prediction_result")

        # Build the initial prediction response
        response = Prediction(
            KNR=knr.KNR,
            predicted_fail_codes=[main_prediction] if main_prediction is not None else [],
            real_fail_codes=[-1],  # Placeholder for real fail codes
            indicated_tests=[""]   # Placeholder for indicated tests
        )

        # If the main prediction fails (main_prediction == 1), run the classification pipeline
        if main_prediction == 1:
            classification_pipeline_file_path = os.path.join(os.getcwd(), 'app', 'pipeline', 'pipeline_classificacao.json')
            with open(classification_pipeline_file_path, "r") as file:
                classification_pipeline_config = json.load(file)
            
            classification_steps = classification_pipeline_config.get("predict_steps", [])

            # Create an orchestrator for the classification pipeline
            classification_orchestrator = Orchestrator(
                pipeline_steps=classification_steps,
                dataframes=dataframes,
                mongo_uri="mongodb://db:27017",
                db_name="cross_the_line"
            )

            # Run the classification prediction pipeline
            classification_orchestrator.run_dynamic_pipeline()

            # Extract predictions from the classification pipeline results
            classification_predictions = {
                key: value for key, value in classification_orchestrator.dataframes.items() if key.startswith('prediction_S_GROUP_ID')
            }

            # Extract the predicted fail codes based on classification results
            predicted_fail_codes = [
                key.replace('prediction_', '') for key, pred in classification_predictions.items() if pred == 1
            ]

            # Update the response with classification predicted fail codes
            response.predicted_fail_codes = predicted_fail_codes

        # Save the prediction to MongoDB using the PredictionsRepository
        self.predict_repo.create_prediction(response)

        # Return the prediction response
        return response

    def update_prediction(self, knr: str, prediction: PredictionUpdate) -> bool:
        return self.predict_repo.update_prediction(knr, prediction)

    def delete_prediction(self, knr: str) -> bool:
        return self.predict_repo.delete_prediction(knr)

    def fail_codes_prediction(self) -> dict:
        return self.predict_repo.fail_codes_prediction()

    def total_fails(self) -> dict:
        return self.predict_repo.total_fails_prediction()

    def get_fail_code_count_by_month(self, year, fail_code: int):
        predicted_fail_code_count = {}
        real_fail_code_count = {}

        for month in range(1, 13):
            knr_list = self.knr_repo.get_knr_by_month(month, year)

            predictions = self.predict_repo.get_predictions_by_knrs(knr_list, fail_code)

            predicted_count = 0
            real_count = 0

            for prediction in predictions:
                predicted_count += prediction["predicted"].count(fail_code)
                real_count += prediction["real"].count(fail_code)

            month_name = datetime(year, month, 1).strftime("%B").lower()
            predicted_fail_code_count[month_name] = predicted_count
            real_fail_code_count[month_name] = real_count

        return {
            "predicted_fail_code_count": predicted_fail_code_count,
            "real_fail_code_count": real_fail_code_count,
        }


class PredictionsServiceSingleton:
    _instance: Optional[PredictionService] = None

    def __init__(self, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    @classmethod
    def initialize(cls, predict_repo: PredictionsRepository, knr_repo: KNRRepository):
        if cls._instance is None:
            cls._instance = PredictionService(predict_repo, knr_repo)

    @classmethod
    def get_instance(cls) -> PredictionService:
        if cls._instance is None:
            raise Exception(
                "ModelServiceSingleton is not initialized. Call initialize() first."
            )

        return cls._instance
