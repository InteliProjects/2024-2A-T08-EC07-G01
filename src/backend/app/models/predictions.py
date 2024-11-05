from typing import List, Optional
from pydantic import BaseModel, Field


class Prediction(BaseModel):
    KNR: str = Field(..., title="Car KNR")

    predicted_fail_codes: Optional[List[int]] = Field(
        [-1], description="Predicted fail code"
    )
    real_fail_codes: Optional[List[int]] = Field([-1], description="Real fail code")
    indicated_tests: Optional[List[str]] = Field([""], description="Indicated tests for predicted fails")

    class Config:
        json_schema_extra = {
            "example": {
                "KNR": "top10knrsdavolkswagen",
                "predicted_fail_codes": [1, 2, 3],
                "real_fail_codes": [1, 2, 3],
                "indicated_tests": ["test1", "test2", "test3"]
            }
        }

class PredictionUpdate(BaseModel):
    KNR: Optional[str] = Field(None, title="Car KNR")

    predicted_fail_codes: Optional[List[int]] = Field(
        [-1], description="Predicted fail code"
    )
    real_fail_codes: Optional[List[int]] = Field([-1], description="Real fail code")
    indicated_tests: Optional[List[str]] = Field([""], description="Indicated tests for predicted fails")

    class Config:
        json_schema_extra = {
            "example": {
                "KNR": "top10knrsdavolkswagen",
                "predicted_fail_codes": [1, 2, 3],
                "real_fail_codes": [1, 2, 3],
                "indicated_tests": ["test1", "test2", "test3"]
            }
        }