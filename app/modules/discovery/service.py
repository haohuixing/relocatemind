from __future__ import annotations

import hashlib
import os
from functools import lru_cache
from typing import Any, Dict, List

from app.core.i18n import get_project_root
from app.models.profile import AssessmentInput, AssessmentSnapshot, MatchResult
from app.modules.discovery.matcher import calculate_matches


MATCHER_VERSION = "deterministic-v1"


def _program_data_path() -> str:
    return os.path.join(get_project_root(), "data", "countries.json")


@lru_cache(maxsize=1)
def get_program_data_version() -> str:
    """Return a content version so results can be traced to a dataset snapshot."""
    with open(_program_data_path(), "rb") as dataset:
        return hashlib.sha256(dataset.read()).hexdigest()[:16]


def calculate_matches_for_assessment(assessment: AssessmentInput) -> AssessmentSnapshot:
    """Run the Python matcher through one validated application boundary."""
    raw_matches: List[Dict[str, Any]] = calculate_matches(
        passport_country=assessment.passport_country,
        monthly_income=assessment.monthly_income,
        income_type=assessment.income_type,
        savings=assessment.savings,
        dependents=assessment.dependents,
        region=assessment.region,
        priority=assessment.priority,
        timeline=assessment.timeline,
    )
    matches = [MatchResult.model_validate(result) for result in raw_matches]
    return AssessmentSnapshot(
        assessment=assessment,
        matches=matches,
        matcher_version=MATCHER_VERSION,
        program_data_version=get_program_data_version(),
    )


def default_assessment() -> AssessmentInput:
    """Provide the existing dashboard fallback through the canonical schema."""
    return AssessmentInput(
        passport_country="United States",
        monthly_income=4000,
        income_type="remote_work",
        savings=15000,
        dependents="solo",
        region="any",
        climate="any",
        priority="quality_of_life",
        timeline="exploring",
    )


def assessment_for_profile(passport_country: str, monthly_income: float, income_type: str) -> AssessmentInput:
    """Adapt the legacy dashboard profile fields to the complete assessment contract."""
    defaults = default_assessment()
    return AssessmentInput.model_validate(
        {
            **defaults.model_dump(),
            "passport_country": passport_country,
            "monthly_income": monthly_income,
            "income_type": income_type,
        }
    )
