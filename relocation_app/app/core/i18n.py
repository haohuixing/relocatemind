import json
import os
from typing import Any

_locales_cache: dict[str, Any] = {}


def get_project_root() -> str:
    curr = os.path.abspath(os.path.dirname(__file__))
    for _ in range(5):
        if os.path.exists(os.path.join(curr, "locales")):
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
        with open(locale_path, "r", encoding="utf-8") as f:
            _locales_cache = json.load(f)
    return _locales_cache


def t(key_path: str, default: str = "") -> str:
    if not _locales_cache:
        load_locales()

    keys = key_path.split(".")
    val = _locales_cache
    for k in keys:
        if isinstance(val, dict) and k in val:
            val = val[k]
        else:
            return default or key_path
    return str(val) if isinstance(val, (str, int, float)) else key_path
