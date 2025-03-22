import json
import os

from dotenv import load_dotenv

load_dotenv()

project_root = os.getcwd()

content_path = os.getenv('CONTENT_PATH', 'content')
content_path = f'{project_root}/{content_path}'
languages = os.getenv('LANGUAGES', {'ru': 'Russian'})
if isinstance(languages, str):
    languages = json.loads(languages)

external_url = os.getenv('EXTERNAL_URL', 'http://127.0.0.1:8011')
path_root = os.getenv("PATH_ROOT", '/ws/socket.io')
broadcast_service = os.getenv('BROADCAST_SERVICE', 'http://127.0.0.1:8020')
broadcast_service_ext_url = os.getenv('BROADCAST_SERVICE_EXT_URL', 'http://127.0.0.1:8020')
transports = os.getenv('TRANSPORTS', ['websocket', 'polling'])
if isinstance(transports, str):
    transports = [i.strip() for i in transports[1:-1].replace('"',"").split(',')]
reconnectionAttempts = os.getenv('RECONNECTION_ATTEMPTS', 5)
owner_type = os.getenv('OWNER_TYPE', 'test')
owner = os.getenv('OWNER', 'owner1')
ui_proxy = os.getenv('UI_PROXY', 'http://127.0.0.1:8012')
logs_root = os.getenv('LOGS_ROOT', './logs')
logs_level = os.getenv('LOGS_LEVEL', "ERROR")
max_content_size = int(os.getenv('MAX_CONTENT_LENGTH', '52428800'))
