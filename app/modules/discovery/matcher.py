import json
import os
from typing import Any, List, Dict, Optional
from app.core.i18n import get_project_root

EU_PASSPORTS = {
    "Germany", "France", "Spain", "Italy", "Portugal", "Netherlands",
    "Belgium", "Ireland", "Austria", "Sweden", "Poland", "Denmark",
    "Finland", "Czechia", "Greece"
}


def load_countries_data() -> List[Dict[str, Any]]:
    root = get_project_root()
    file_path = os.path.join(root, "data", "countries.json")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def calculate_matches(
    passport_country: Optional[str] = None,
    monthly_income: Optional[float] = None,
    income_type: Optional[str] = None,
    savings: Optional[float] = None,
    dependents: Optional[str] = None,
    region: Optional[str] = None,
    priority: Optional[str] = None,
    timeline: Optional[str] = None,
) -> List[Dict[str, Any]]:
    countries = load_countries_data()
    results = []

    is_user_eu = passport_country in EU_PASSPORTS if passport_country else False

    # Dependents multiplier calculation
    has_spouse = dependents in ["couple", "family_small", "family_large"]
    num_children = 1 if dependents == "family_small" else (2 if dependents == "family_large" else 0)

    for country in countries:
        eligible = True
        reasons = []
        is_eu_freedom = is_user_eu and country.get("is_eu_country", False)

        # 1. Family-Adjusted Minimum Income Requirement
        base_min = float(country.get("min_income_usd", 0))
        spouse_pct = float(country.get("dependent_spouse_pct", 0.0)) if has_spouse else 0.0
        child_pct = float(country.get("dependent_child_pct", 0.0)) * num_children
        adjusted_min_income = 0.0 if is_eu_freedom else base_min * (1.0 + spouse_pct + child_pct)

        shortfall_usd = 0.0

        # Hard Income Check
        if monthly_income is not None and not is_eu_freedom and monthly_income < adjusted_min_income:
            eligible = False
            shortfall_usd = round(adjusted_min_income - monthly_income)
            reasons.append(f"Income (${monthly_income:,.0f}) is below family minimum (${adjusted_min_income:,.0f}/mo)")

        # Hard Income Structure Check
        if income_type and not is_eu_freedom and income_type not in country.get("allowed_income_types", []):
            eligible = False
            reasons.append(f"Income structure '{income_type.replace('_', ' ').title()}' is not accepted")

        # Hard Savings Check
        min_savings = float(country.get("min_savings_usd", 0))
        if savings is not None and not is_eu_freedom and min_savings > 0 and savings < min_savings:
            eligible = False
            reasons.append(f"Liquid savings (${savings:,.0f}) is below required bank deposit (${min_savings:,.0f})")

        # 2. Hyper-Responsive Score Engine (Dynamic Swings)
        score = 50.0  # Dynamic baseline

        if eligible:
            # Region Preference Swing (+15% or -20%)
            if region and region != "any":
                if country.get("region") == region:
                    score += 15.0
                else:
                    score -= 20.0  # Major penalty if outside requested region

            # EU Freedom Boost
            if is_eu_freedom:
                score += 20.0
                reasons.append("✓ EU Freedom of Movement granted")
            elif monthly_income is not None and adjusted_min_income > 0:
                income_ratio = monthly_income / adjusted_min_income
                score += min(25.0, (income_ratio - 1.0) * 15.0)

            # Savings Buffer Boost
            if savings is not None and min_savings > 0 and savings >= min_savings * 1.5:
                score += 10.0

            # Priority Alignment Swing (+15% or -10%)
            tax_rate = country.get("tax_rate_pct", 100)
            if priority == "low_tax":
                if tax_rate == 0:
                    score += 15.0
                elif tax_rate <= 15:
                    score += 10.0
                else:
                    score -= 10.0
            elif priority == "low_cost" and country.get("cost_of_living_usd", 5000) <= 1300:
                score += 15.0
            elif priority == "quality_of_life" and country.get("quality_of_life_score", 0) >= 88:
                score += 12.0
            elif priority == "fast_process" and country.get("processing_time_months", 12) <= 1:
                score += 15.0
            elif priority == "citizenship" and country.get("citizenship_pathway_years", 99) <= 5:
                score += 15.0

            # Clamp between 15% and 99%
            final_score = max(15, min(99, round(score)))
        else:
            final_score = max(15, round(30 - (shortfall_usd / 200)))

        results.append(
            {
                "country_id": country["id"],
                "name": country["name"],
                "flag": country["flag"],
                "region": country.get("region", "europe"),
                "visa_name": country["visa_name"],
                "is_eu_country": country.get("is_eu_country", False),
                "is_eu_freedom": is_eu_freedom,
                "min_income_usd": round(adjusted_min_income),
                "base_min_income_usd": base_min,
                "min_savings_usd": min_savings,
                "shortfall_usd": shortfall_usd,
                "cost_of_living_usd": country["cost_of_living_usd"],
                "tax_rate_pct": country["tax_rate_pct"],
                "quality_of_life_score": country["quality_of_life_score"],
                "citizenship_pathway_years": country.get("citizenship_pathway_years", 5),
                "processing_time_months": country.get("processing_time_months", 2),
                "summary": country["summary"],
                "checklist": country.get("checklist", []),
                "eligible": eligible,
                "reasons": reasons,
                "score": final_score,
            }
        )

    results.sort(key=lambda x: (x["eligible"], x["score"]), reverse=True)
    return results