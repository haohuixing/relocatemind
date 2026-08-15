from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class QuizInput(BaseModel):
    passport_country: str = Field(..., example="United States")
    monthly_income: float = Field(..., ge=0, example=4000.0)
    income_type: str = Field(..., example="remote_work")


class MatchResult(BaseModel):
    country_id: str
    name: str
    flag: str
    visa_name: str
    min_income_usd: float
    cost_of_living_usd: float
    tax_rate_pct: float
    quality_of_life_score: float
    summary: str
    checklist: List[str]
    eligible: bool
    reasons: List[str]
    score: int


class UserProfile(BaseModel):
    id: Optional[int] = None
    user_id: str
    passport_country: Optional[str] = "United States"
    monthly_income: Optional[float] = 4000.0
    income_type: Optional[str] = "remote_work"
    matches_json: Optional[List[Dict[str, Any]]] = None
    checklist_json: Optional[List[Dict[str, Any]]] = None
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)