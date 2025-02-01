"""
"""

from typing import Dict

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.description import description, title, version, license, contact
from src import router
from src.httpx_client import get_client_pack, initialize, ping_broadcast_server
from src.logger_setup import get_logger
import src.config as cfg


@asynccontextmanager
async def lifespan(app: FastAPI):
    # StartUp
    logger.info("Startup")
    __print_config()
    app.requests_client = initialize()
    await get_client_pack(app.requests_client, 'prompter')
    await get_client_pack(app.requests_client, 'viewer')
    # pong = await ping_broadcast_server(app.requests_client)
    # logger.info(pong)
    yield
    # ShutDown
    logger.info("Shutdown")
    # await app.requests_client.aclose()

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

app.include_router(router.router)


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
    logger.info(f"logs_root: {cfg.logs_root}")
    logger.info(f"logs_level: {cfg.logs_level}")
