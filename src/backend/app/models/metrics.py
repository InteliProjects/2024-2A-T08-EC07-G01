from pydantic import BaseModel, Field


class Metrics (BaseModel):
    model_name: str = Field(..., description="Name of the trained model")
    f1_score: float = Field(..., description="F1 score of the model")
    precision: float = Field(..., description="Precision of the model")
    recall: float = Field(..., description="Recall of the model")
    accuracy: float = Field(..., description="Accuracy of the model")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "RandomForestModel_v1",
                "accuracy": 0.10,
                "precision": 0.20,
                "recall": 0.30,
                "f1_score": 0.40,
            }
        }

class MetricsWeights (BaseModel):
    f1_score: float = Field(None, description="F1 score of the model")
    precision: float = Field(None, description="Precision of the model")
    recall: float = Field(None, description="Recall of the model")
    accuracy: float = Field(None, description="Accuracy of the model")
    
    class Config:
        json_schema_extra = {
            "example": {
                "accuracy": 0.10,
                "precision": 0.20,
                "recall": 0.30,
                "f1_score": 0.40,
            }
        }


