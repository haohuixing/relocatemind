import json
import os
from typing import Any, List, Dict
from app.core.i18n import get_project_root


def load_countries_data() -> List[Dict[str, Any]]:
    root = get_project_root()
    file_path = os.path.join(root, "data", "countries.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def calculate_matches(
    passport_country: str, monthly_income: float, income_type: str
) -> List[Dict[str, Any]]:
    countries = load_countries_data()
    results = []

    for country in countries:
        eligible = True
        reasons = []

        if monthly_income < country["min_income_usd"]:
            eligible = False
            reasons.append(
                f"Income (${monthly_income:.0f}) below required minimum (${country['min_income_usd']})"
            )

        if income_type not in country["allowed_income_types"]:
            eligible = False
            reasons.append(
                f"Income type '{income_type.replace('_', ' ').title()}' not accepted for this visa"
            )

        if eligible:
            score = 70.0
            income_ratio = monthly_income / country["min_income_usd"]
            score += min(15.0, (income_ratio - 1.0) * 15.0)
            score += country["quality_of_life_score"] / 10.0
            if monthly_income >= country["cost_of_living_usd"] * 2:
                score += 4.0

            final_score = min(99, round(score))
        else:
            final_score = max(15, round(30 - len(reasons) * 10))

        results.append(
            {
                "country_id": country["id"],
                "name": country["name"],
                "flag": country["flag"],
                "visa_name": country["visa_name"],
                "min_income_usd": country["min_income_usd"],
                "cost_of_living_usd": country["cost_of_living_usd"],
                "tax_rate_pct": country["tax_rate_pct"],
                "quality_of_life_score": country["quality_of_life_score"],
                "summary": country["summary"],
                "checklist": country.get("checklist", []),
                "eligible": eligible,
                "reasons": reasons,
                "score": final_score,
            }
        )

    results.sort(key=lambda x: (x["eligible"], x["score"]), reverse=True)
    return results
