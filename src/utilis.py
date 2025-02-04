import os
import json
import re
import uuid
import aiofiles

import src.config as cfg
from src.logger_setup import get_logger

logger = get_logger(__name__)


async def load_content(name: str) -> dict:
    '''Load content from file'''

    full_name = f'{cfg.content_path}/{name}.json'
    logger.info(full_name)
    # Opening JSON file
    async with aiofiles.open(full_name) as f:
        json_data = await f.read()
        data = json.loads(json_data)
    return data


def get_auth_data() -> dict:
    '''return ws auth data'''
    return {
        'user': str(uuid.uuid1()),
        'owner': cfg.owner
    }


def check_static_path():
    ''''''
    project_root = os.getcwd()
    out_path = f'{project_root}/static/prompter'
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    out_path = f'{project_root}/static/viewer'
    if not os.path.exists(out_path):
        os.makedirs(out_path)

async def store_static_file(client_name, file_name: str, content):
    '''stores a static files into static folder'''      
    project_root = os.getcwd()
    full_name = f'{project_root}/static/{client_name}/{file_name}'

    if file_name.endswith('.js'):
        content = await __resolve_placeholders(content)

    async with aiofiles.open(full_name, "w") as f:
        # Writing data to a file
        await f.write(content)


async def __resolve_placeholders(content):
    '''resolve placeholders'''
    original_string = content
    pattern = re.compile(r'SESSION-GENERATED-URL')
    content = re.sub(pattern, cfg.external_url, original_string)
    pattern = re.compile(r'BROADCAST_SERVICE_URL')
    content = re.sub(pattern, cfg.broadcast_service, content)
    pattern = re.compile(r'REGISTERED-OWNER')
    content = re.sub(pattern, cfg.owner, content)
    return content


async def __load_js(client):
    '''load js and resolve user placeholder'''
    project_root = os.getcwd()
    content = ''
    async with aiofiles.open(f'{project_root}/temp/{client}.js') as f:
        content = await f.read()
    return content


async def __load_html_css(client, script):
    ''''''
    project_root = os.getcwd()
    content = ''
    async with aiofiles.open(f'{project_root}/static/{client}/{script}') as f:
        content = await f.read()
    return content


async def load_script(page, script):
    ''''''
    if script == 'prompter.js' or script == 'viewer.js':
        return await __load_js(page)
    return await __load_html_css(page, script)
