import json
from typing import Optional
from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.auth import create_signed_token, parse_signed_token
from app.core.templates import templates
from app.modules.discovery.matcher import calculate_matches, load_countries_data

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
    passport_country: str = Form(...),
    monthly_income: float = Form(...),
    income_type: str = Form(...),
    dependents: str = Form("solo"),
    priority: str = Form("quality_of_life"),
    timeline: str = Form("3_6_months"),
):
    matches = calculate_matches(
        passport_country=passport_country,
        monthly_income=monthly_income,
        income_type=income_type,
        dependents=dependents,
        priority=priority,
        timeline=timeline,
    )

    test_payload = {
        "passport_country": passport_country,
        "monthly_income": monthly_income,
        "income_type": income_type,
        "dependents": dependents,
        "priority": priority,
        "timeline": timeline,
        "matches": matches,
    }

    signed_test_cookie = create_signed_token(test_payload)

    redirect = RedirectResponse(url="/results", status_code=303)
    redirect.set_cookie(
        key="anon_test_data",
        value=signed_test_cookie,
        httponly=True,
        max_age=3600,
        samesite="lax",
    )
    return redirect


@discovery_router.get("/results", response_class=HTMLResponse)
def results_page(request: Request):
    test_cookie = request.cookies.get("anon_test_data")
    test_data = parse_signed_token(test_cookie) if test_cookie else None

    if not test_data:
        return RedirectResponse(url="/free-test", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="results.html",
        context={
            "matches": test_data.get("matches", []),
            "passport_country": test_data.get("passport_country"),
            "monthly_income": test_data.get("monthly_income"),
            "income_type": test_data.get("income_type"),
            "dependents": test_data.get("dependents", "solo"),
            "priority": test_data.get("priority", "quality_of_life"),
            "timeline": test_data.get("timeline", "3_6_months"),
        },
    )