from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from app.core.auth import get_current_user
from app.core.config import get_settings
from app.core.i18n import load_locales
from app.core.templates import templates
from app.modules.auth_router import auth_router
from app.modules.discovery.router import discovery_router

settings = get_settings()
settings.validate_for_startup()
load_locales()

app = FastAPI(title="RelocateMind - Supabase Engine")


@app.middleware("http")
async def add_user_context(request: Request, call_next):
    user = get_current_user(request)
    request.state.is_authenticated = user is not None
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault("X-Frame-Options", "DENY")
    return response


app.include_router(discovery_router)
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)