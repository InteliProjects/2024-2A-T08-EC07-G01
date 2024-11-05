from pydantic import BaseModel


class FailCodeByMonthRequest(BaseModel):
    year: int
    fail_code: int
