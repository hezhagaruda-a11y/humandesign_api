from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import general, transits, composite
from .routers.v2 import general as general_v2

import importlib.metadata
from .utils.version import get_version

__version__ = get_version()
if __version__ == "0.0.0":
    try:
        __version__ = importlib.metadata.version("humandesign-api")
    except importlib.metadata.PackageNotFoundError:
        pass

app = FastAPI(title="Human Design API", version=__version__)

# CORS – allows your laptop to talk to the engine
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(general.router)
app.include_router(transits.router)
app.include_router(composite.router)
app.include_router(general_v2.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)