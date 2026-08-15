import json
import os
from typing import Any

_locales_cache: dict[str, Any] = {}

# Built-in fallbacks so keys always render clean, human-readable text
FALLBACKS: dict[str, str] = {
    "app.name": "RelocateMind",
    "app.tagline": "Discover your ideal country for relocation based on income, visa eligibility, and lifestyle goals.",
    "app.footer_updated": "Residency & Visa Index 2026",
    "nav.home": "Home",
    "nav.free_test": "Take Free Test",
    "nav.login": "Log In",
    "nav.register": "Create Account",
    "nav.dashboard": "Dashboard",
    "nav.logout": "Log Out",
    "nav.menu": "MENU",
    "nav.close": "CLOSE",
    "nav.language": "Language",
    "homepage.hero_tag": "Global Relocation Intelligence Engine",
    "homepage.hero_title": "Find the Country That Fits Your Income & Passport",
    "homepage.hero_subtitle": "Get instant, deterministic match scores for 8+ digital nomad and residency programs worldwide.",
    "homepage.cta_take_test": "Take Free Test (No Account Needed)",
    "homepage.cta_create_account": "Create Account Directly",
    "homepage.deck_tag": "Interactive Engine Deck",
    "homepage.deck_title": "Explore How the Matching Works",
    "homepage.deck_tab1": "01. Eligibility",
    "homepage.deck_tab2": "02. Cost Analysis",
    "homepage.deck_tab3": "03. Action Steps",
    "homepage.deck_p1_module": "01 // ELIGIBILITY MATRIX",
    "homepage.deck_p1_tag": "HARD FILTERS",
    "homepage.deck_p1_title": "Income & Visa Requirement Verification",
    "homepage.deck_p1_desc": "Cross-checks your passport restrictions, monthly revenue minimums, and accepted income structures.",
    "homepage.deck_p1_l1_label": "User Monthly Revenue:",
    "homepage.deck_p1_l1_val": "$4,500 / mo",
    "homepage.deck_p1_l2_label": "Portugal Visa Minimum:",
    "homepage.deck_p1_l2_val": "$3,200 / mo",
    "homepage.deck_p1_l3_label": "Verification Status:",
    "homepage.deck_p1_l3_val": "✓ ELIGIBLE (D8 VISA)",
    "homepage.deck_p2_module": "02 // PURCHASING POWER & TAX INDEX",
    "homepage.deck_p2_tag": "PURCHASING POWER",
    "homepage.deck_p2_title": "Local Living Cost vs. Income Ratio",
    "homepage.deck_p2_desc": "Calculates your real purchasing buffer in destination countries.",
    "homepage.deck_p2_l1_label": "Estimated Living Cost:",
    "homepage.deck_p2_l1_val": "$1,800 / mo",
    "homepage.deck_p2_l2_label": "Purchasing Buffer:",
    "homepage.deck_p2_l2_val": "2.5x Expenses",
    "homepage.deck_p2_est_rent": "Est. Monthly Rent",
    "homepage.deck_p2_tax_rate": "Est. Tax Rate",
    "homepage.deck_p3_module": "03 // EXECUTION ROADMAP",
    "homepage.deck_p3_tag": "EXECUTION ROADMAP",
    "homepage.deck_p3_title": "Step-by-Step Relocation Checklists",
    "homepage.deck_p3_desc": "Get actionable, itemized instructions for document apostilling and visa application.",
    "homepage.deck_p3_s1": "Gather $3,200/mo bank statements",
    "homepage.deck_p3_s2": "Obtain background clearance",
    "homepage.deck_p3_s3": "Apply via E-Consulate Portal",
    "homepage.destinations_tag": "Global Destinations",
    "homepage.destinations_title": "Sample Program Indexes",
    "homepage.destinations_link": "Run Full Matching Test",
    "homepage.sample_1_desc": "Mild climate, vibrant tech hub, and straightforward digital worker residency process.",
    "homepage.sample_2_desc": "Tax incentives under Beckham Law regime with Mediterranean lifestyle.",
    "homepage.sample_3_desc": "Eco-friendly haven offering 0% foreign income tax and low cost of living thresholds.",
    "free_test.title": "Anonymous Country Matcher",
    "free_test.subtitle": "Fill in your details below to calculate your country match scores instantly.",
    "free_test.section_1_num": "01",
    "free_test.section_1_title": "Passport & Monthly Revenue",
    "free_test.passport_label": "Select Passport Country",
    "free_test.income_label": "Monthly Income (USD)",
    "free_test.income_placeholder": "e.g. 4000",
    "free_test.per_month": "/ mo",
    "free_test.section_2_num": "02",
    "free_test.section_2_title": "Select Income Source Structure",
    "free_test.income_type_label": "Primary Income Source",
    "free_test.type_remote_title": "Remote Employment",
    "free_test.type_remote_sub": "W2 / Salaried Contract",
    "free_test.type_freelance_title": "Freelance / Business",
    "free_test.type_freelance_sub": "B2B / Self-Employed",
    "free_test.type_passive_title": "Passive / Investments",
    "free_test.type_passive_sub": "Dividends, Real Estate",
    "free_test.type_savings_title": "Capital & Savings",
    "free_test.type_savings_sub": "Liquid Bank Deposits",
    "free_test.submit_button": "Calculate Matches Now",
    "results.title": "Your Relocation Match Results",
    "results.subtitle": "Here are the top countries matched to your financial profile and passport.",
    "results.inputs_prefix": "INPUTS:",
    "results.save_banner_tag": "PERSISTENT STORAGE",
    "results.save_banner_title": "Want to save your matches and unlock action plans?",
    "results.save_banner_desc": "Create a free account now to store your plan and track your relocation checklist.",
    "results.save_cta": "Create Account to Save My Plan",
    "results.score_label": "Match Score",
    "results.purchasing_ratio": "Purchasing Buffer",
    "results.living_cost": "Living Cost",
    "results.min_income": "Min. Income Req.",
    "results.cost_of_living": "Cost of Living",
    "results.tax_rate": "Est. Tax Rate",
    "results.eligible_status": "Eligible",
    "results.ineligible_status": "Requirements Not Met",
    "results.unlock_steps": "Unlock Action Steps",
    "auth.register_title": "Create Your Account",
    "auth.register_subtitle": "Access your personalized relocation dashboard and saved plans.",
    "auth.login_title": "Welcome Back",
    "auth.login_subtitle": "Log in to access your dashboard.",
    "auth.email_label": "Email Address",
    "auth.email_placeholder": "johndoe@gmail.com",
    "auth.password_label": "Password",
    "auth.confirm_password_label": "Confirm Password",
    "auth.password_placeholder": "••••••••••••",
    "auth.btn_register": "Sign Up",
    "auth.btn_login": "Sign In",
    "auth.already_have_account": "Already have an account?",
    "auth.dont_have_account": "Don't have an account?",
    "auth.prepopulated_notice": "Your anonymous test results are ready and will be automatically saved to your new account!",
    "auth.password_mismatch_error": "Passwords do not match. Please verify both password fields.",
    "dashboard.title": "Your Relocation Dashboard",
    "dashboard.active_user_prefix": "Workspace for",
    "dashboard.update_profile_title": "Update Profile & Recalculate Matches",
    "dashboard.passport": "Passport Country",
    "dashboard.income": "Monthly Income ($USD)",
    "dashboard.income_type": "Income Structure",
    "dashboard.btn_update": "Update Profile & Recalculate",
    "dashboard.saved_matches_title": "Your Saved Country Matches",
    "dashboard.checklist_header": "RELOCATION ACTION CHECKLIST",
    "dashboard.completed_label": "Completed",
    "dashboard.no_matches": "No matches saved yet. Update your profile above to calculate matches.",
}


def get_project_root() -> str:
    """Returns absolute path to the project root directory."""
    curr = os.path.abspath(os.path.dirname(__file__))
    for _ in range(4):
        if os.path.exists(os.path.join(curr, "locales", "en.json")):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def load_locales():
    global _locales_cache
    root = get_project_root()
    locale_path = os.path.join(root, "locales", "en.json")
    if os.path.exists(locale_path):
        try:
            with open(locale_path, "r", encoding="utf-8") as f:
                _locales_cache = json.load(f)
        except Exception:
            _locales_cache = {}
    return _locales_cache


def t(key_path: str, default: str = "") -> str:
    if not _locales_cache:
        load_locales()

    keys = key_path.split(".")
    val = _locales_cache
    found = True
    for k in keys:
        if isinstance(val, dict) and k in val:
            val = val[k]
        else:
            found = False
            break

    if found and isinstance(val, (str, int, float)):
        return str(val)

    if default:
        return default

    if key_path in FALLBACKS:
        return FALLBACKS[key_path]

    return keys[-1].replace("_", " ").title()