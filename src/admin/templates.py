
import os
from fastapi.templating import Jinja2Templates


prject_root = os.getcwd()

templates = Jinja2Templates(directory='./src/admin/templates')
