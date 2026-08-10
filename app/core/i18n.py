import json
import os
from typing import Any

_locales_cache: dict[str, Any] = {}

# Built-in fallbacks so keys always render clean, human-readable text
FALLBACKS: dict[str, str] = {
    "homepage.hero_tag": "Global Mobility Platform 2026",
    "homepage.hero_title": "Find the Country That Fits Your Income & Passport",
    "homepage.hero_subtitle": "Get instant match scores for 8+ digital nomad and residency programs worldwide.",
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
    "homepage.sample_3_desc": "Eco-friendly haven offering 0% foreign income tax and low cost of living thresholds."
}


def get_project_root() -> str:
    curr = os.path.abspath(os.path.dirname(__file__))
    for _ in range(6):
        if os.path.exists(os.path.join(curr, "locales", "en.json")):
            return curr
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


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

    last_key = keys[-1].replace("_", " ").title()
    return last_key