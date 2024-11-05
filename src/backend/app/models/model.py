from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

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
                "created_at": "2024-09-10T12:00:00"
            }
        }



class ModelUpdate(BaseModel):
    model_name: Optional[str] = Field(None, description="Name of the trained model")
    training_date: Optional[datetime] = Field(
        None, description="Date when the model was trained"
    )
    gridfs_path: Optional[str] = Field(
        None, description="Path in GridFS where the model is stored"
    )
    recipe_path: Optional[str] = Field(
        ..., description="Path in GridFS where the recipe is stored"
    )

    type_model: Optional[str] = Field(..., description="Name of the trained model")

    accuracy: Optional[float] = Field(None, description="Accuracy of the model")
    precision: Optional[float] = Field(None, description="Precision of the model")
    recall: Optional[float] = Field(None, description="Recall of the model")
    f1_score: Optional[float] = Field(None, description="F1 score of the model")

    last_used: Optional[datetime] = Field(
        None, description="Date when the model was last used"
    )
    using: Optional[bool] = Field(..., description="If the model is being used")

    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "RandomForestModel_v1",
                "training_date": "2024-09-10T12:00:00",
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
