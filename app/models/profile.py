from __future__ import annotations

import math
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class IncomeType(str, Enum):
    REMOTE_WORK = "remote_work"
    FREELANCE = "freelance"
    PASSIVE_INCOME = "passive_income"
    SAVINGS = "savings"


class HouseholdSize(str, Enum):
    SOLO = "solo"
    COUPLE = "couple"
    FAMILY_SMALL = "family_small"
    FAMILY_LARGE = "family_large"


class Region(str, Enum):
    EUROPE = "europe"
    AMERICAS = "americas"
    ASIA = "asia"
    MIDDLE_EAST = "middle_east"
    ANY = "any"


class Climate(str, Enum):
    ANY = "any"
    TROPICAL = "tropical"
    MEDITERRANEAN = "mediterranean"
    TEMPERATE = "temperate"
    COLD = "cold"


class Priority(str, Enum):
    QUALITY_OF_LIFE = "quality_of_life"
    LOW_TAX = "low_tax"
    LOW_COST = "low_cost"
    CITIZENSHIP = "citizenship"
    FAST_PROCESS = "fast_process"


class Timeline(str, Enum):
    ASAP = "asap"
    THREE_TO_SIX_MONTHS = "3_6_months"
    SIX_TO_TWELVE_MONTHS = "6_12_months"
    EXPLORING = "exploring"


class AssessmentInput(BaseModel):
    """Canonical validated input for the deterministic assessment engine."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, use_enum_values=True)

    passport_country: str = Field(..., min_length=2, max_length=100)
    monthly_income: float = Field(..., gt=0, le=1_000_000)
    income_type: IncomeType
    savings: float = Field(..., ge=0, le=100_000_000)
    dependents: HouseholdSize
    region: Region
    climate: Climate = Climate.ANY
    priority: Priority
    timeline: Optional[Timeline] = None

    @field_validator("monthly_income", "savings")
    @classmethod
    def validate_finite_amount(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("amount must be finite")
        return round(value, 2)

    @field_validator("passport_country")
    @classmethod
    def validate_country_name(cls, value: str) -> str:
        if any(ord(character) < 32 for character in value):
            raise ValueError("passport_country contains invalid control characters")
        return value


class MatchResult(BaseModel):
    """Validated result contract returned by the authoritative matcher."""

    model_config = ConfigDict(extra="forbid")

    country_id: str
    name: str
    flag: str
    region: str
    visa_name: str
    is_eu_country: bool
    is_eu_freedom: bool
    min_income_usd: float = Field(..., ge=0)
    base_min_income_usd: float = Field(..., ge=0)
    min_savings_usd: float = Field(..., ge=0)
    shortfall_usd: float = Field(..., ge=0)
    cost_of_living_usd: float = Field(..., ge=0)
    tax_rate_pct: float = Field(..., ge=0)
    quality_of_life_score: float = Field(..., ge=0, le=100)
    citizenship_pathway_years: float = Field(..., ge=0)
    processing_time_months: float = Field(..., ge=0)
    summary: str
    checklist: List[str]
    eligible: bool
    reasons: List[str]
    score: int = Field(..., ge=0, le=100)


class AssessmentSnapshot(BaseModel):
    """Immutable-shaped result envelope with version metadata."""

    model_config = ConfigDict(extra="forbid")

    assessment: AssessmentInput
    matches: List[MatchResult]
    matcher_version: str
    program_data_version: str


class AnonymousAssessmentCookie(BaseModel):
    """Small signed cookie payload; match results stay server-derived."""

    model_config = ConfigDict(extra="forbid")

    assessment: AssessmentInput
    issued_at: datetime


class QuizInput(AssessmentInput):
    """Backward-compatible name for callers that still use the old model."""


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