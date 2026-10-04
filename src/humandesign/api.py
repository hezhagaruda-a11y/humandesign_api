import os
import importlib.metadata

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import general, transits, composite
from .routers.v2 import general as general_v2
from .utils.version import get_version


__version__ = get_version()
if __version__ == "0.0.0":
    try:
        __version__ = importlib.metadata.version("humandesign-api")
    except importlib.metadata.PackageNotFoundError:
        pass


app = FastAPI(title="Human Design API", version=__version__)


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
# `allow_origins=["*"]` combined with `allow_credentials=True` is rejected by
# every modern browser (the CORS spec forbids the wildcard when credentials
# are allowed). We don't use cookies — auth is a Bearer token — so we set
# allow_credentials=False and use an explicit origin allow-list.
#
# Origins can be overridden at deploy time via the CORS_ORIGINS env var
# (comma-separated). Default covers local dev.
# ---------------------------------------------------------------------------
_default_origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
_env_origins = os.getenv("CORS_ORIGINS", "").strip()
ALLOWED_ORIGINS = (
    [o.strip() for o in _env_origins.split(",") if o.strip()]
    if _env_origins
    else _default_origins
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["Content-Length"],
    max_age=600,
)


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(general.router)
app.include_router(transits.router)
app.include_router(composite.router)
app.include_router(general_v2.router)


# ---------------------------------------------------------------------------
# Health check — used by Render keep-alive pings and load balancers
# ---------------------------------------------------------------------------
@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok", "version": __version__}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("humandesign.api:app", host="0.0.0.0", port=8000, reload=True)
