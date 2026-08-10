import json
from typing import Optional
from fastapi import APIRouter, Depends, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from app.core.auth import (
    create_signed_token,
    get_current_user_id,
    hash_password,
    parse_signed_token,
    verify_password,
)
from app.core.templates import templates
from app.database import get_db
from app.models.profile import UserProfile
from app.models.user import User
from app.modules.discovery.matcher import calculate_matches

auth_router = APIRouter()


@auth_router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    has_test_data = False
    test_cookie = request.cookies.get("anon_test_data")
    if test_cookie and parse_signed_token(test_cookie):
        has_test_data = True

    return templates.TemplateResponse(
        request=request,
        name="register.html",
        context={
            "has_test_data": has_test_data,
            "error": None,
        },
    )


@auth_router.post("/register")
def register_post(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "has_test_data": False,
                "error": "Email already registered. Please login.",
            },
            status_code=400,
        )

    user = User(email=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)

    test_cookie = request.cookies.get("anon_test_data")
    test_data = parse_signed_token(test_cookie) if test_cookie else None

    if test_data:
        passport = test_data.get("passport_country", "")
        income = test_data.get("monthly_income", 0.0)
        inc_type = test_data.get("income_type", "")
        matches = test_data.get("matches", [])
    else:
        passport = "United States"
        income = 4000.0
        inc_type = "remote_work"
        matches = calculate_matches(passport, income, inc_type)

    profile = UserProfile(
        user_id=user.id,
        passport_country=passport,
        monthly_income=income,
        income_type=inc_type,
        matches_json=json.dumps(matches),
        checklist_json=json.dumps([]),
    )
    db.add(profile)
    db.commit()

    session_token = create_signed_token({"user_id": user.id})
    redirect = RedirectResponse(url="/dashboard", status_code=303)
    redirect.set_cookie(
        key="session_token", value=session_token, httponly=True, max_age=86400
    )
    redirect.delete_cookie(key="anon_test_data")
    return redirect


@auth_router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None},
    )


@auth_router.post("/login")
def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "Invalid email or password."},
            status_code=400,
        )

    session_token = create_signed_token({"user_id": user.id})
    redirect = RedirectResponse(url="/dashboard", status_code=303)
    redirect.set_cookie(
        key="session_token", value=session_token, httponly=True, max_age=86400
    )
    return redirect


@auth_router.get("/logout")
def logout():
    redirect = RedirectResponse(url="/", status_code=303)
    redirect.delete_cookie(key="session_token")
    return redirect


@auth_router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request, db: Session = Depends(get_db)):
    user_id = get_current_user_id(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.profile:
        return RedirectResponse(url="/login", status_code=303)

    matches = (
        json.loads(user.profile.matches_json)
        if user.profile.matches_json
        else []
    )
    checklist = (
        json.loads(user.profile.checklist_json)
        if user.profile.checklist_json
        else []
    )

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "profile": user.profile,
            "matches": matches,
            "checklist": checklist,
        },
    )


@auth_router.post("/dashboard/update")
def update_profile(
    request: Request,
    passport_country: str = Form(...),
    monthly_income: float = Form(...),
    income_type: str = Form(...),
    db: Session = Depends(get_db),
):
    user_id = get_current_user_id(request)
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    profile = (
        db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    )
    if profile:
        profile.passport_country = passport_country
        profile.monthly_income = monthly_income
        profile.income_type = income_type

        updated_matches = calculate_matches(
            passport_country, monthly_income, income_type
        )
        profile.matches_json = json.dumps(updated_matches)

        db.commit()

    return RedirectResponse(url="/dashboard", status_code=303)
