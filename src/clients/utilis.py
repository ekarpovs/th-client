import os
import json
import re
import uuid
from shutil import rmtree

import aiofiles
from babel import Locale

import src.common.config as cfg
from src.common.logger_setup import get_logger

logger = get_logger(__name__)


async def load_content(name: str) -> dict:
    '''Load content from a file'''

    full_name = f'{cfg.content_path}/{name}.json'
    logger.info(full_name)
    # Opening JSON file
    async with aiofiles.open(full_name) as f:
        json_data = await f.read()
        data = json.loads(json_data)
    return data

def get_languages_from_content() -> list:
    '''Get list of languages from the content folder'''
    languages = []
    project_root = os.getcwd()
    content_path = f'{project_root}/content'
    content_folder = os.fsencode(content_path)
    # for filename in os.listdir(content_folder):
    for file in os.listdir(content_folder):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            language = build_language_descriptor(filename)
            if language['label'] !=  None:
                languages.append(language)
    logger.info(f'languages: {languages}')
    return languages
        

def build_language_descriptor(filename: str) -> dict:
    '''build language descriptor from content file name'''
    lang_code, _ = filename.split('_')
    dir = 'ltr'
    if lang_code == 'he':
        dir = 'rtl'
    try:
        # Use Babel's Locale to get the language name
        locale = Locale.parse(lang_code)
        # language name in English
        label = locale.get_display_name('en')
        logger.info(f'label: {label}')
    except Exception as e:
        # Handle invalid codes
        label = None
        logger.error(f'error: str(e), message: Invalid language code')

    language = {'code': lang_code.capitalize(), 'label': label, 'dir': dir}
    return language



def get_cfg_data() -> dict:
    '''return congiguration data'''
    return {
        'bsrvLocator': cfg.broadcast_service,
        'pathRoot': cfg.path_root,
        'transports': cfg.transports,
        'reconnectionAttempts': cfg.reconnectionAttempts,
        'authData' : {
            'owner-type': f'/{cfg.owner_type}',
            'owner': cfg.owner,
            'client': str(uuid.uuid1()),
        }
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
