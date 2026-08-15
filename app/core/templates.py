import os
from fastapi.templating import Jinja2Templates
from app.core.i18n import get_project_root, t


def resolve_templates_dir() -> str:
    root = get_project_root()
    templates_dir = os.path.join(root, "templates")
    if os.path.exists(templates_dir) and os.path.isdir(templates_dir):
        return templates_dir
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "templates")


templates = Jinja2Templates(directory=resolve_templates_dir())
templates.env.globals["t"] = t