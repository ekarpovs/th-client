"""
"""

from typing import Dict

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.description import description, title, version, license, contact
from src.clients import endpoints
from src.common.httpx_client import initialize, ping_broadcast_server
from src.common.logger_setup import get_logger
import src.common.config as cfg
from src.clients.utilis import check_static_path
# Admin
from src.admin.endpoints import pages_router, dash_router, auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # StartUp
    logger.info("Startup")
    __print_config()
    check_static_path()
    app.requests_client = initialize()
    # await get_client_pack(app.requests_client, 'prompter')
    # await get_client_pack(app.requests_client, 'viewer')
    pong = await ping_broadcast_server(app.requests_client)
    logger.info(pong)
    yield
    # ShutDown
    logger.info("Shutdown")
    await app.requests_client.aclose()

app = FastAPI(
    lifespan=lifespan,
    title=title,
    description=description,
    version=version,
    contact=contact,
    license=license
)

origins = [
    #   'https://piehost.com/socketio-tester',
    # IMPORTANT: Add other endpoints here
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Static Files
app.mount('/static_admin', StaticFiles(directory='static_admin'), name='static_admin')

app.include_router(endpoints.router)

app.include_router(pages_router, prefix="/adm", tags=["Pages"])
app.include_router(auth_router, prefix="/adm/auth", tags=["Auth"])
app.include_router(dash_router, prefix="/adm", tags=["Dashboard"])

@app.get("/", tags=["HELTH"])
def ping() -> Dict:
    '''ping'''
    return {"pong": "TH client is live"}


logger = get_logger(__name__)


# Output configuration
def __print_config():
    logger.info("Current configuration:")
    logger.info(f"content: {cfg.content_path}")
    logger.info(f"external_url: {cfg.external_url}")
    logger.info(f"broadcast_service: {cfg.broadcast_service}")
    logger.info(f"owner_type: {cfg.owner_type}")
    logger.info(f"owner: {cfg.owner}")
    logger.info(f"ui_proxy: {cfg.ui_proxy}")
    logger.info(f"logs_root: {cfg.logs_root}")
    logger.info(f"logs_level: {cfg.logs_level}")
