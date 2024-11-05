import json
import os
import pandas as pd
from app.models.model import Model
from app.repositories.models_repo import ModelRepository
from typing import Optional
from app.pipeline.orchestrator import Orchestrator
import datetime


class TrainService:
    def __init__(self, model_repo: ModelRepository):
        self.model_repo = model_repo

    def train_model(self, df_resultados: pd.DataFrame, df_falhas: pd.DataFrame) -> dict:
        # Load pipeline configuration
        pipeline_file_path = os.path.join(
            os.getcwd(), "app", "pipeline", "pipeline_principal.json"
        )
        classification_file_path = os.path.join(
            os.getcwd(), "app", "pipeline", "pipeline_classificacao.json"
        )

        with open(pipeline_file_path, "r") as file:
            pipeline_config = json.load(file)

        with open(classification_file_path, "r") as file:
            classification_config = json.load(file)

        steps = pipeline_config.get("prediction_steps", []) + pipeline_config.get(
            "training_steps", []
        )
        classification_steps = classification_config.get("training_steps", [])

        print(steps)
        # Initialize dataframes for the pipeline
        dataframes = {
            "df_resultados": df_resultados,
            "df_falhas": df_falhas,
        }

        # Create an orchestrator to run the pipeline
        main_orchestrator = Orchestrator(
            pipeline_steps=steps,
            dataframes=dataframes,
            mongo_uri="mongodb://db:27017",
            db_name="cross_the_line",
        )

        # Run the pipeline and get the model metadata
        main_model_metadata = main_orchestrator.run_dynamic_pipeline()

        # Debug print to verify model metadata
        print(f"[DEBUG] Orchestrator returned model metadata: {main_model_metadata}")

        main_model_type_mapping = {
            "train_main_model": "type0"  # Assuming 'train_main_model' is the key in main_models_metadata
        }

        # Iterate over main models metadata and save to the repository
        for step_name, model_meta in main_model_metadata.items():
            # Extract model name and metrics
            model_name = model_meta.get("model_name")
            metrics = model_meta.get("metrics", {})

            # Determine model_type based on step_name
            model_type = main_model_type_mapping.get(step_name, "unknown")

            # Create a new Model object to store in the database
            new_model = Model(
                model_name=model_name,
                type_model=model_type,
                gridfs_path=f"path/to/models/{model_name}.h5",  # Replace with actual GridFS path
                recipe_path=f"path/to/recipes/{model_name}_recipe.json",  # Replace with actual GridFS path
                accuracy=metrics.get("accuracy", 0.0),
                precision=metrics.get("precision", 0.0),
                recall=metrics.get("recall", 0.0),
                f1_score=metrics.get("f1_score", 0.0),
                last_used=None,
                using=False,  # Adjust based on your logic
                created_at=datetime.datetime.utcnow(),
            )

            # Save the main model in the repository
            try:
                self.model_repo.create_model(new_model)
                print(
                    f"[INFO] Main Model '{new_model.model_name}' saved to repository."
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to save main model '{new_model.model_name}': {str(e)}"
                )

        classification_orchestrator = Orchestrator(
            pipeline_steps=classification_steps,
            dataframes=dataframes,
            mongo_uri="mongodb://db:27017",
            db_name="cross_the_line",
        )

        classification_models_metadata = (
            classification_orchestrator.run_dynamic_pipeline()
        )

        classification_model_type_mapping = {
            "S_GROUP_ID_1": "type1",
            "S_GROUP_ID_2": "type2",
            "S_GROUP_ID_4": "type4",
            "S_GROUP_ID_5": "type5",
            "S_GROUP_ID_133": "type133",
            "S_GROUP_ID_137": "type137",
            "S_GROUP_ID_140": "type140",
            "S_GROUP_ID_9830946": "type9830946",
        }

        for step_name, model_meta in classification_models_metadata.items():
            # Extract model name and metrics
            model_name = model_meta.get("model_name")
            metrics = model_meta.get("metrics", {})

            # Determine model_type based on model_name
            model_type = classification_model_type_mapping.get(model_name, "unknown")

            # Create a new Model object to store in the database
            new_model = Model(
                model_name=model_name,
                type_model=model_type,
                gridfs_path=f"path/to/models/{model_name}.h5",  # Replace with actual GridFS path
                recipe_path=f"path/to/recipes/{model_name}_recipe.json",  # Replace with actual GridFS path
                accuracy=metrics.get("accuracy", 0.0),
                precision=metrics.get("precision", 0.0),
                recall=metrics.get("recall", 0.0),
                f1_score=metrics.get("f1_score", 0.0),
                last_used=None,
                using=False,
                created_at=datetime.datetime.utcnow(),
            )

            # Save the classification model in the repository
            try:
                self.model_repo.create_model(new_model)
                print(
                    f"[INFO] Classification Model '{new_model.model_name}' saved to repository."
                )
            except Exception as e:
                raise RuntimeError(
                    f"Failed to save classification model '{new_model.model_name}': {str(e)}"
                )

        return main_model_metadata

    def retrain_model(self, df_resultados: pd.DataFrame, df_falhas: pd.DataFrame):
        """
        Retrains the main model and the 8 classification models, saves them, and stores their metadata.

        Parameters:
        df_resultados (pd.DataFrame): The resultados DataFrame.
        df_falhas (pd.DataFrame): The falhas DataFrame.

        Returns:
        dict: Comparison of the new main model's performance with the previous one.
        """
        # Define paths to pipeline configurations
        main_pipeline_file_path = os.path.join(
            os.getcwd(), "app", "pipeline", "pipeline_principal.json"
        )
        classification_pipeline_file_path = os.path.join(
            os.getcwd(), "app", "pipeline", "pipeline_classificacao.json"
        )
        print("Absolute Path to Main Pipeline JSON file:", main_pipeline_file_path)
        print(
            "Absolute Path to Classification Pipeline JSON file:",
            classification_pipeline_file_path,
        )

        # Load main pipeline configuration
        try:
            with open(main_pipeline_file_path, "r") as file:
                main_pipeline_config = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Main pipeline configuration file not found at {main_pipeline_file_path}"
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding main pipeline JSON: {str(e)}")

        # Load classification pipeline configuration
        try:
            with open(classification_pipeline_file_path, "r") as file:
                classification_pipeline_config = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Classification pipeline configuration file not found at {classification_pipeline_file_path}"
            )
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding classification pipeline JSON: {str(e)}")

        # Extract training steps
        main_training_steps = main_pipeline_config.get(
            "prediction_steps", []
        ) + main_pipeline_config.get("training_steps", [])
        classification_training_steps = classification_pipeline_config.get(
            "training_steps", []
        )

        if not main_training_steps:
            print("[WARNING] No training steps found in main_pipeline_config.")
        if not classification_training_steps:
            print(
                "[WARNING] No training steps found in classification_pipeline_config."
            )

        # Initialize dataframes for the main pipeline
        main_dataframes = {
            "df_resultados": df_resultados,
            "df_falhas": df_falhas,
        }

        print(f"[DEBUG] Main Pipeline Steps: {main_training_steps}")
        # Create an orchestrator to run the main pipeline
        main_orchestrator = Orchestrator(
            pipeline_steps=main_training_steps,
            dataframes=main_dataframes,
            mongo_uri="mongodb://db:27017",
            db_name="cross_the_line",
        )

        # Run the main pipeline and get the main model's metadata
       # Get main model metadata from the orchestrator
        main_model_metadata = main_orchestrator.run_dynamic_pipeline()

        # Debug print to verify main model's metadata
        print(f"[DEBUG] Main Orchestrator returned models metadata: {main_model_metadata}")

        # Check if main_model_metadata contains the necessary keys
        if isinstance(main_model_metadata, dict):
            model_name = main_model_metadata.get("model_name")
            metrics = main_model_metadata.get("metrics", {})
            model_type = main_model_metadata.get("type_model", "unknown")

            if not model_name:
                print("[ERROR] 'model_name' missing in main model metadata.")
            else:
                # Construct a new Model object with the metadata
                new_model = Model(
                    model_name=model_name,
                    type_model=model_type,
                    gridfs_path=f"path/to/models/{model_name}.h5",  # Update with actual GridFS path
                    recipe_path=f"path/to/recipes/{model_name}_recipe.json",  # Update with actual recipe path
                    accuracy=metrics.get("accuracy", 0.0),
                    precision=metrics.get("precision", 0.0),
                    recall=metrics.get("recall", 0.0),
                    f1_score=metrics.get("f1_score", 0.0),
                    last_used=None,
                    using=False,  # Adjust based on your logic
                    created_at=datetime.datetime.utcnow(),
                )

                # Attempt to save the model in the repository
                try:
                    self.model_repo.create_model(new_model)
                    print(f"[INFO] Main Model '{new_model.model_name}' saved to repository.")
                except Exception as e:
                    raise RuntimeError(f"Failed to save main model '{new_model.model_name}': {str(e)}")

        else:
            print("[ERROR] The main model metadata is not in the expected format.")


        # Initialize dataframes for the classification pipeline
        classification_dataframes = {
            "df_resultados": df_resultados,
            "df_falhas": df_falhas,
        }

        print("[DEBUG] Classification Pipeline Steps:", classification_training_steps)
        # Create an orchestrator to run the classification pipeline
        classification_orchestrator = Orchestrator(
            pipeline_steps=classification_training_steps,
            dataframes=classification_dataframes,
            mongo_uri="mongodb://db:27017",
            db_name="cross_the_line",
        )

        # Run the classification pipeline and get the classification models' metadata
        classification_models_metadata = (
            classification_orchestrator.run_dynamic_pipeline()
        )

        # Debug print to verify classification models metadata
        print(
            f"[DEBUG] Classification Orchestrator returned models metadata: {classification_models_metadata}"
        )

        # Define model_type mapping for classification models
        classification_model_type_mapping = {
            "S_GROUP_ID_1": "type1",
            "S_GROUP_ID_2": "type2",
            "S_GROUP_ID_4": "type4",
            "S_GROUP_ID_5": "type5",
            "S_GROUP_ID_133": "type133",
            "S_GROUP_ID_137": "type137",
            "S_GROUP_ID_140": "type140",
            "S_GROUP_ID_9830946": "type9830946",
        }

        # Iterate over classification models metadata and save to the repository
        for step_name, model_meta in classification_models_metadata.items():
            # Ensure model_meta is a dictionary
            if isinstance(model_meta, dict):
                model_name = model_meta.get("model_name")
                metrics = model_meta.get("metrics", {})
                model_type = classification_model_type_mapping.get(
                    model_name, "unknown"
                )

                if not model_name:
                    print(
                        f"[ERROR] Missing 'model_name' in classification model metadata for step '{step_name}'."
                    )
                    continue

                # Create a new Model object to store in the database
                new_model = Model(
                    model_name=model_name,
                    type_model=model_type,
                    gridfs_path=f"path/to/models/{model_name}.h5",  # Replace with actual GridFS path
                    recipe_path=f"path/to/recipes/{model_name}_recipe.json",  # Replace with actual GridFS path
                    accuracy=metrics.get("accuracy", 0.0),
                    precision=metrics.get("precision", 0.0),
                    recall=metrics.get("recall", 0.0),
                    f1_score=metrics.get("f1_score", 0.0),
                    last_used=None,
                    using=False,
                    created_at=datetime.datetime.utcnow(),
                )

                # Save the classification model in the repository
                try:
                    self.model_repo.create_model(new_model)
                    print(
                        f"[INFO] Classification Model '{new_model.model_name}' saved to repository."
                    )
                    self.model_repo.unset_all_using(new_model.type_model)
                    self.model_repo.set_model_using(new_model.model_name)
                except Exception as e:
                    raise RuntimeError(
                        f"Failed to save classification model '{new_model.model_name}': {str(e)}"
                    )
            else:
                print(
                    f"[ERROR] Model metadata for step '{step_name}' is not a dictionary: {model_meta}"
                )

        # Compare the main model with the last trained main model
        main_model_name = model_name  # Replace with actual main model name if different
        last_main_model = self.model_repo.get_latest_model("type0")

        if last_main_model and last_main_model.model_name != main_model_name:
            # Compare the new main model's metrics with the last main model's metrics
            comparison = self.compare_models(main_model_metadata, last_main_model)
        else:
            # No previous model, so new model is the first model
            comparison = {
                "message": "No previous main model to compare with.",
                "new_model_metrics": {
                    "model_name": main_model_name,
                    "accuracy": main_model_metadata.get("metrics", {}).get(
                        "accuracy", 0.0
                    ),
                    "precision": main_model_metadata.get("metrics", {}).get(
                        "precision", 0.0
                    ),
                    "recall": main_model_metadata.get("metrics", {}).get("recall", 0.0),
                    "f1_score": main_model_metadata.get("metrics", {}).get(
                        "f1_score", 0.0
                    ),
                },
            }

        # Return the comparison result
        return comparison

    def compare_models(self, new_model_metadata, last_model) -> dict:
        new_metrics = new_model_metadata["metrics"]
        model_name = new_model_metadata.get("model_name")
        last_metrics = {
            "accuracy": last_model.accuracy,
            "precision": last_model.precision,
            "recall": last_model.recall,
            "f1_score": last_model.f1_score,
        }

        differences = {}
        for metric in new_metrics:
            new_value = new_metrics[metric]
            last_value = last_metrics.get(metric, 0.0)
            differences[metric] = new_value - last_value

        comparison = {
            "new_model_metrics": {"model_name": model_name, **new_metrics},
            "last_model_metrics": last_metrics,
            "differences": differences,
        }

        return comparison

    def select_model(self, model_name: str, model_type: Optional[str] = "type0"):
        # Set 'using' to False for all models of the specified model_type
        self.model_repo.unset_all_using(model_type=model_type)
        # Set 'using' to True for the selected model
        self.model_repo.set_model_using(model_name)


class TrainServiceSingleton:
    _instance: TrainService = None

    def __init__(self, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    def __new__(cls, *args, **kwargs):
        raise RuntimeError("Call get_instance() instead")

    @classmethod
    def initialize(cls, model_repo: ModelRepository):
        if cls._instance is None:
            cls._instance = TrainService(model_repo)

    @classmethod
    def get_instance(cls) -> TrainService:
        if cls._instance is None:
            raise Exception(
                "ModelServiceSingleton is not initialized. Call initialize() first."
            )
        return cls._instance
