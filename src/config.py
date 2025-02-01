import os

from dotenv import load_dotenv

load_dotenv()

project_root = os.getcwd()

content_path = os.getenv("CONTENT_PATH", "")
content_path = f'{project_root}/{content_path}'
external_url = os.getenv("EXTERNAL_URL", "http://127.0.0.1:8011")
broadcast_service = os.getenv("BROADCAST_SERVICE", "http://127.0.0.1:8005")
owner = os.getenv("OWNER", "owner1")
ui_proxy = os.getenv("UI_PROXY", "http://127.0.0.1:8012")
logs_root = os.getenv("LOGS_ROOT", "./logs")
logs_level = os.getenv("LOGS_LEVEL", "ERROR")
