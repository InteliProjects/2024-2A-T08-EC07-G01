from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Train(BaseModel):
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


class ModelMetrics(BaseModel):
    model_name: Optional[str] = None
    accuracy: float
    precision: float
    recall: float
    f1_score: float

    class Config:
        schema_extra = {
            "example": {
                "model_name": "GRU",
                "accuracy": 1.0,
                "precision": 0.0,
                "recall": 0.0,
                "f1_score": 0.0
            }
        }

class ModelComparison(BaseModel):
    new_model_metrics: ModelMetrics
    last_model_metrics: Optional[ModelMetrics] = None
    differences: Optional[ModelMetrics] = None
    message: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "new_model_metrics": {
                    "model_name": "GRU",
                    "accuracy": 1.0,
                    "precision": 0.0,
                    "recall": 0.0,
                    "f1_score": 0.0
                },
                "last_model_metrics": {
                    "accuracy": 0.8752,
                    "precision": 0.9212,
                    "recall": 0.9056,
                    "f1_score": 0.9056
                },
                "differences": {
                    "accuracy": 0.1248,
                    "precision": -0.9212,
                    "recall": -0.9056,
                    "f1_score": -0.9056
                },
                "message": "Retrain successful."
            }
        }

class SelectModelRequest(BaseModel):
    model_name: str
    model_type: str
