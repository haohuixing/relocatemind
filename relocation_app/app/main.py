from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from app.core.auth import get_current_user_id
from app.core.i18n import load_locales
from app.core.templates import templates
from app.database import Base, engine
from app.modules.auth_router import auth_router
from app.modules.discovery.router import discovery_router

Base.metadata.create_all(bind=engine)
load_locales()

app = FastAPI(title="Relocation Discovery MVP")


@app.middleware("http")
def add_user_context(request: Request, call_next):
    user_id = get_current_user_id(request)
    request.state.is_authenticated = user_id is not None
    response = call_next(request)
    return response


app.include_router(discovery_router)
app.include_router(auth_router)


@app.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
