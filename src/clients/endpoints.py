'''
Router. You may use it for tests with API via URL/docs
'''


from mimetypes import guess_type
from typing import Optional

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.common.httpx_client import redirect_to_broadcast_server
from src.clients.utilis import get_cfg_data, load_content, load_script
from src.common.logger_setup import get_logger

router = APIRouter()

logger = get_logger(__name__)


@router.get("/app/{page}", tags=["LOAD"])
@router.get("/app/{page}/{script}", tags=["LOAD"])
async def get_script(page: str, script: Optional[str] = 'index.html'):
    '''load html page and scripts'''
    logger.info(f'get_script - {page} - {script}')
    if page != 'viewer' and page != 'prompter':
        logger.error('wrong url')
        return {'error': 'wrong url'}

    content = await load_script(page, script)

    content_type, _ = guess_type(script)
    return HTMLResponse(content, media_type=content_type)


@router.get("/webdata/{lang}", tags=["LOAD DATA"])
async def getweb_data(lang):
    '''get data from the file'''
    logger.info('getweb_data')
    doc_name = f'{lang}_data'
    content = await load_content(doc_name)
    content_value = content['content']
    return {"content": content_value}


@router.get("/cfg", tags=["CLIENT CONFIG"])
async def client_congig():
    '''get configuration data'''
    cfg = get_cfg_data()
    logger.info(f'client cfg data {cfg}')
    return cfg


@router.post("/redirect", tags=["REDIRECT"])
async def redirect(request: Request):
    '''redirect message to the broadcast server'''
    data = await request.json()
    logger.info(f'{data}')
    return await redirect_to_broadcast_server(
        request.app.requests_client, data)


@router.get("/status/{data}", tags=["CLIENT STATUS"])
async def client_status(data):
    '''get data from the file'''
    status = 'disconnected'
    if data:
        status = 'connected'
    logger.info(f'client: {data} {status}')
    return {"status": status}
