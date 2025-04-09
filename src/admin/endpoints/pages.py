from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.admin.templates import templates

router = APIRouter()


# Home Page
@router.get('/', response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse('index.html', {'request': request})


# # Login Page
# @router.get('/login', response_class=HTMLResponse)
# def login(request: Request):
#     return templates.TemplateResponse('login.html', {'request': request, 'user': None})
