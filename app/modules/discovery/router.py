import json
from typing import Optional

from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from app.core.templates import templates
from app.models.profile import AssessmentInput
from app.modules.discovery.matcher import load_countries_data
from app.modules.discovery.service import calculate_matches_for_assessment
from app.modules.discovery.session import read_assessment_cookie, set_assessment_cookie

discovery_router = APIRouter()


@discovery_router.get("/free-test", response_class=HTMLResponse)
def free_test_page(request: Request):
    countries = load_countries_data()
    return templates.TemplateResponse(
        request=request,
        name="free_test.html",
        context={"countries_json": json.dumps(countries)},
    )


@discovery_router.post("/match")
def process_match(
    response: Response,
    passport_country: Optional[str] = Form(None),
    monthly_income: Optional[float] = Form(None),
    income_type: Optional[str] = Form(None),
    savings: Optional[float] = Form(None),
    dependents: Optional[str] = Form(None),
    region: Optional[str] = Form(None),
    climate: Optional[str] = Form(None),
    priority: Optional[str] = Form(None),
    timeline: Optional[str] = Form(None),
):
    try:
        assessment = AssessmentInput.model_validate(
            {
                "passport_country": passport_country,
                "monthly_income": monthly_income,
                "income_type": income_type,
                "savings": savings,
                "dependents": dependents,
                "region": region,
                "climate": climate or "any",
                "priority": priority,
                "timeline": timeline,
            }
        )
    except ValidationError:
        return RedirectResponse(url="/free-test?error=invalid_input", status_code=303)

    # Validate the complete dataset/result contract before issuing the redirect.
    calculate_matches_for_assessment(assessment)
    redirect = RedirectResponse(url="/results", status_code=303)
    set_assessment_cookie(redirect, assessment)
    return redirect


@discovery_router.get("/results", response_class=HTMLResponse)
def results_page(request: Request):
    assessment = read_assessment_cookie(request)
    if not assessment:
        return RedirectResponse(url="/free-test", status_code=303)

    snapshot = calculate_matches_for_assessment(assessment)
    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "matches": [match.model_dump() for match in snapshot.matches],
            "passport_country": assessment.passport_country,
            "monthly_income": assessment.monthly_income,
            "income_type": assessment.income_type,
            "dependents": assessment.dependents,
            "priority": assessment.priority,
            "timeline": assessment.timeline,
        },
    )