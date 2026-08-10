import os
from fastapi.templating import Jinja2Templates
from app.core.i18n import t


def resolve_templates_dir() -> str:
    curr = os.path.abspath(os.path.dirname(__file__))
    for _ in range(5):
        candidate_root = os.path.join(curr, "templates")
        if os.path.exists(candidate_root) and os.path.isdir(candidate_root):
            return candidate_root
        candidate_app = os.path.join(curr, "app", "templates")
        if os.path.exists(candidate_app) and os.path.isdir(candidate_app):
            return candidate_app
        parent = os.path.dirname(curr)
        if parent == curr:
            break
        curr = parent
    return os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates"
    )


templates = Jinja2Templates(directory=resolve_templates_dir())
templates.env.globals["t"] = t
