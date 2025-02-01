'''
Asynchronous http client
'''

from httpx import AsyncClient, ConnectTimeout, Response
from tenacity import retry, stop_after_attempt, retry_if_exception_type

import src.config as cfg
from src.utilis import store_static_file

UI_PROXY_URL = cfg.ui_proxy
BROADCAST_SERVISE_TARGET_URL = cfg.broadcast_service


def initialize() -> AsyncClient:
    '''initialize an AsyncClient'''
    return AsyncClient()


async def get_client_pack(requests_client: AsyncClient, client_name):
    '''loads prompter or viewer from ui proxy, unpack and sore files into the static folder'''
    target_url = f'{UI_PROXY_URL}/{client_name}'
    prompter_pack = await __send_get_request(requests_client, target_url)
    content = prompter_pack['pack']['html']
    await store_static_file(client_name, 'index.html', content)
    content = prompter_pack['pack']['css']
    await store_static_file(client_name, 'style.css', content)
    content = prompter_pack['pack']['js']
    await store_static_file(client_name, 'main.js', content)


async def ping_broadcast_server(requests_client: AsyncClient) -> dict:
    ''''''
    target_url = f'{BROADCAST_SERVISE_TARGET_URL}'
    return await __send_get_request(requests_client, target_url)


async def redirect_to_broadcast_server(
        requests_client: AsyncClient,
        data: dict) -> dict:
    ''''''
    target_url = f'{BROADCAST_SERVISE_TARGET_URL}/endpoint'
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
    return __response_data(await requests_client.get(url=target_url))


@retry(
    retry=retry_if_exception_type(ConnectTimeout),
    stop=stop_after_attempt(3))
async def __send_post_request(
        requests_client: AsyncClient,
        target_url: str,
        data: dict) -> dict:
    ''''''
    return __response_data(await requests_client.post(
        url=target_url,
        json=data,
    ))


def __response_data(response: Response) -> dict:
    ''''''
    response.raise_for_status()
    resp_data = response.json()
    return resp_data
