from typing import Optional
from pydantic import BaseModel, Field


class KNR(BaseModel):
    KNR: str = Field(..., description="Car KNR")

    NAME: Optional[str] = Field(..., description="Car NAME")
    ID: Optional[int] = Field(..., description="Car ID")
    STATUS: Optional[int] = Field(..., description="Car STATUS")
    UNIT: Optional[str] = Field(..., description="Car UNIT")
    VALUE_ID: Optional[str] = Field(..., description="Car VALUE_ID")
    VALUE: Optional[str] = Field(..., description="Car VALUE")
    DATA: Optional[str] = Field(..., description="Car DATA")

    class Config:
        json_schema_extra = {
            "example": {
                "KNR": "KNR123",
                "NAME": "Model A",
                "ID": 123,
                "STATUS": 1,
                "UNIT": "Unit123",
                "VALUE_ID": "Value001",
                "VALUE": "200",
                "DATA": "2024-01-01T12:00:00",
            }
        }


class KNRUpdate(BaseModel):
    KNR: Optional[str] = Field(..., description="Car KNR")

    NAME: Optional[str] = Field(..., description="Car NAME")
    ID: Optional[int] = Field(..., description="Car ID")
    STATUS: Optional[int] = Field(..., description="Car STATUS")
    UNIT: Optional[str] = Field(..., description="Car UNIT")
    VALUE_ID: Optional[str] = Field(..., description="Car VALUE_ID")
    VALUE: Optional[str] = Field(..., description="Car VALUE")
    DATA: Optional[str] = Field(..., description="Car DATA")

    class Config:
        json_schema_extra = {
            "example": {
                "KNR": "KNR123",
                "NAME": "Model A",
                "ID": 123,
                "STATUS": 1,
                "UNIT": "Unit123",
                "VALUE_ID": "Value001",
                "VALUE": "200",
                "DATA": "2024-01-01T12:00:00",
            }
        }
