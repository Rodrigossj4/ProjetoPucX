from pydantic import BaseModel
from typing import Optional


class Paciente(BaseModel):
    id: Optional[int]
    name: str
    sex: int
    age: int
    Chest_pain_type: int
    BP: int
    Cholesterol: int
    FBS_over_120: int
    EKG_results: int
    Max_HR: int
    Exercise_angina: int
    ST_depression: float
    Slope_of_ST: int
    Number_of_vessels_fluro: int
    Thallium: int
    Heart_Disease: Optional[str]
