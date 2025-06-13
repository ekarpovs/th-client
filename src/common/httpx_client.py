'''
Asynchronous http client
'''

from fastapi.responses import JSONResponse
from httpx import AsyncClient, ConnectTimeout, Response
from tenacity import retry, stop_after_attempt, retry_if_exception_type

import src.common.config as cfg
from src.clients.utilis import store_static_file
from src.common.logger_setup import get_logger

UI_PROXY_URL = f'{cfg.ui_proxy}/clients/simple'
BROADCAST_SERVISE_TARGET_URL = cfg.broadcast_service

logger = get_logger(__name__)


def initialize() -> AsyncClient:
    '''initialize an AsyncClient'''
    return AsyncClient()


async def get_client_pack(requests_client: AsyncClient, client_name):
    '''loads clients from ui proxy, unpack and sore files into the static folder'''
    target_url = f'{UI_PROXY_URL}/{client_name}'
    client_pack = await __send_get_request(requests_client, target_url)
    if 'pack' in client_pack:
        content = client_pack['pack']['html']
        await store_static_file(client_name, 'index.html', content)
        content = client_pack['pack']['css']
        await store_static_file(client_name, 'style.css', content)
        content = client_pack['pack']['js']
        await store_static_file(client_name, 'main.js', content)
        return True
    else:
        logger.error(f'get_client_pack for {client_name} error')
        return False

async def ping_broadcast_server(requests_client: AsyncClient) -> dict:
    ''''''
    target_url = f'{BROADCAST_SERVISE_TARGET_URL}'
    return await __send_get_request(requests_client, target_url)


async def stop_all_room_clients(requests_client: AsyncClient) -> dict:
    ''''''
    target_url = f'{BROADCAST_SERVISE_TARGET_URL}/shutdown-room'
    data = {}
    data['owner-type'] = cfg.owner_type
    data['owner'] = cfg.owner
    return await __send_post_request(
        requests_client,
        target_url, data)


async def redirect_to_broadcast_server(
        requests_client: AsyncClient,
        data: dict) -> dict:
    ''''''
    target_url = f'{BROADCAST_SERVISE_TARGET_URL}/redirect'
    data['owner-type'] = cfg.owner_type
    data['owner'] = cfg.owner
    return await __send_post_request(
        requests_client,
        target_url, data)


@retry(
    retry=retry_if_exception_type(ConnectTimeout),
    stop=stop_after_attempt(3))
async def __send_get_request(
        requests_client: AsyncClient,
        target_url: str) -> dict:
    ''''''
    try: 
        return __response_data(await requests_client.get(url=target_url))
    except Exception as e:
        logger.error(f'__send_get_request {e}')
        return {"error": f'__send_get_request {e}'}

@retry(
    retry=retry_if_exception_type(ConnectTimeout),
    stop=stop_after_attempt(3))
async def __send_post_request(
        requests_client: AsyncClient,
        target_url: str,
        data: dict) -> dict:
    ''''''
    try: 
        return __response_data(await requests_client.post(
            url=target_url,
            json=data,
        ))
    except Exception as e:
        logger.error(f'__send_post_request {e}')
        return {}


def __response_data(response: Response) -> dict:
    ''''''
    response.raise_for_status()
    resp_data = response.json()
    return resp_data
