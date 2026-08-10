import json
from typing import Optional
from fastapi import APIRouter, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse

from app.core.auth import (
    create_signed_token,
    get_current_user,
    parse_signed_token,
)
from app.core.i18n import t
from app.core.templates import templates
from app.database import supabase, supabase_admin
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
            "success_message": None,
            "error": None,
        },
    )


@auth_router.post("/register")
def register_post(
    request: Request,
    response: Response,
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
):
    clean_email = email.strip()

    # 1. Password Matching Validation
    if password != confirm_password:
        test_cookie = request.cookies.get("anon_test_data")
        has_test_data = bool(test_cookie and parse_signed_token(test_cookie))
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "has_test_data": has_test_data,
                "success_message": None,
                "error": t("auth.password_mismatch_error", "Passwords do not match. Please verify both password fields."),
            },
            status_code=400,
        )

    try:
        # 2. Register user via Supabase Auth Engine
        auth_response = supabase.auth.sign_up({"email": clean_email, "password": password})
        
        if not auth_response.user:
            return templates.TemplateResponse(
                request=request,
                name="register.html",
                context={
                    "has_test_data": False,
                    "success_message": None,
                    "error": "Registration failed. Please try again with a valid email.",
                },
                status_code=400,
            )

        user_id = auth_response.user.id

        # 3. Extract anonymous test data from cookie if available
        test_cookie = request.cookies.get("anon_test_data")
        test_data = parse_signed_token(test_cookie) if test_cookie else None

        if test_data:
            passport = test_data.get("passport_country", "United States")
            income = float(test_data.get("monthly_income", 4000.0))
            inc_type = test_data.get("income_type", "remote_work")
            matches = test_data.get("matches", [])
        else:
            passport = "United States"
            income = 4000.0
            inc_type = "remote_work"
            matches = calculate_matches(passport, income, inc_type)

        # 4. Upsert User Profile entry using admin client (bypasses RLS before email confirmation)
        supabase_admin.table("user_profiles").upsert({
            "user_id": user_id,
            "passport_country": passport,
            "monthly_income": income,
            "income_type": inc_type,
            "matches_json": json.dumps(matches),
            "checklist_json": json.dumps([]),
        }).execute()

        # 5. Handle Email Confirmation vs Immediate Session
        if auth_response.session:
            access_token = auth_response.session.access_token
            redirect = RedirectResponse(url="/dashboard", status_code=303)
            redirect.set_cookie(
                key="sb_access_token",
                value=access_token,
                httponly=True,
                max_age=86400,
                samesite="lax",
            )
            redirect.delete_cookie(key="anon_test_data")
            return redirect

        # Confirmation email required state
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "has_test_data": False,
                "success_message": f"Confirmation email sent to {clean_email}! Please check your inbox and verify your email to log in.",
                "error": None,
            },
        )

    except Exception as e:
        error_msg = str(e)
        if "User already registered" in error_msg or "already_exists" in error_msg:
            error_msg = "Email already registered. Please login instead."
        return templates.TemplateResponse(
            request=request,
            name="register.html",
            context={
                "has_test_data": False,
                "success_message": None,
                "error": error_msg,
            },
            status_code=400,
        )


@auth_router.get("/login", response_class=HTMLResponse)
def login_page(request: Request, confirmed: Optional[bool] = None):
    success_msg = None
    if confirmed:
        success_msg = "Email verified successfully! You can now log in below."

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"error": None, "success_message": success_msg},
    )


@auth_router.post("/login")
def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
):
    clean_email = email.strip()

    try:
        auth_response = supabase.auth.sign_in_with_password(
            {"email": clean_email, "password": password}
        )

        if not auth_response.session:
            return templates.TemplateResponse(
                request=request,
                name="login.html",
                context={
                    "error": "Please confirm your email address before logging in.",
                    "success_message": None,
                },
                status_code=400,
            )

        access_token = auth_response.session.access_token

        redirect = RedirectResponse(url="/dashboard", status_code=303)
        redirect.set_cookie(
            key="sb_access_token",
            value=access_token,
            httponly=True,
            max_age=86400,
            samesite="lax",
        )
        redirect.delete_cookie(key="anon_test_data")
        return redirect

    except Exception as e:
        error_str = str(e)
        error_msg = "Invalid email or password."
        
        if "Email not confirmed" in error_str or "email_not_confirmed" in error_str:
            error_msg = "Please verify your email address before logging in."
        elif "Invalid login credentials" in error_str:
            error_msg = "Invalid email or password. Please check your credentials."

        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": error_msg, "success_message": None},
            status_code=400,
        )


@auth_router.get("/logout")
def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    redirect = RedirectResponse(url="/", status_code=303)
    redirect.delete_cookie(key="sb_access_token")
    return redirect


@auth_router.get("/dashboard", response_class=HTMLResponse)
def dashboard_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    user_id = user["id"]
    
    profile_res = (
        supabase_admin.table("user_profiles")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    if not profile_res.data:
        default_matches = calculate_matches("United States", 4000.0, "remote_work")
        new_profile = {
            "user_id": user_id,
            "passport_country": "United States",
            "monthly_income": 4000.0,
            "income_type": "remote_work",
            "matches_json": json.dumps(default_matches),
            "checklist_json": json.dumps([]),
        }
        supabase_admin.table("user_profiles").insert(new_profile).execute()
        profile = new_profile
    else:
        profile = profile_res.data[0]

    raw_matches = profile.get("matches_json")
    if isinstance(raw_matches, str):
        matches = json.loads(raw_matches) if raw_matches else []
    else:
        matches = raw_matches if raw_matches else []

    raw_checklist = profile.get("checklist_json")
    if isinstance(raw_checklist, str):
        checklist = json.loads(raw_checklist) if raw_checklist else []
    else:
        checklist = raw_checklist if raw_checklist else []

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "user": user,
            "profile": profile,
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
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    user_id = user["id"]
    updated_matches = calculate_matches(passport_country, monthly_income, income_type)

    supabase_admin.table("user_profiles").update({
        "passport_country": passport_country,
        "monthly_income": monthly_income,
        "income_type": income_type,
        "matches_json": json.dumps(updated_matches),
    }).eq("user_id", user_id).execute()

    return RedirectResponse(url="/dashboard", status_code=303)