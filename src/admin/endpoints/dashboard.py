# src/endpoints/distro.py

import os
from fastapi import APIRouter, BackgroundTasks, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import File, UploadFile

import src.common.config as cfg
from src.common.httpx_client import initialize, ping_broadcast_server, get_client_pack
from src.common.logger_setup import get_logger
from src.admin.services import check_content, clean_content, convert_file
from src.admin.templates import templates

logger = get_logger(__name__)

router = APIRouter()


# Display the upload form
@router.get('/dashboard', response_class=HTMLResponse, tags=["ADMIN"])
def upload_form(request: Request):
    return templates.TemplateResponse('dashboard.html', {'request': request})


@router.get('/checksrv', tags=["ADMIN"])
async def check_srv(request: Request, requests_client = Depends(initialize)):
    ''''''
    result = await ping_broadcast_server(requests_client)
    logger.info(result)
    return result


@router.get('/start', tags=["ADMIN"])
async def start(request: Request, requests_client = Depends(initialize)) -> JSONResponse:
    ''''''
    response = {
            "success": False,
            "message": 'Show can not be started'
        }
    result = check_content()
    if not result:
        response['message'] = f'{response["message"]} - please load content'
        return response
    
    result = await get_client_pack(requests_client, 'prompter')
    if result:
        result = await get_client_pack(requests_client, 'viewer')
    if result:
        response['success'] = True
        response['message'] = 'Show started successfully'
    return response


@router.get('/stop', tags=["ADMIN"])
async def stop(request: Request, requests_client = Depends(initialize)):
    ''''''
    response = {
            "success": True,
            "message": 'Show finished'
        }
    # send request to server
    return response

@router.get('/cleancont', tags=["ADMIN"])
async def clean(request: Request):
    ''''''
    clean_content()
    return {"message": "Content deleted"}


# Handle the file upload
@router.post('/upload', tags=["ADMIN"])
async def upload_file(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    if file.content_type != 'text/plain':
        return templates.TemplateResponse(
            'dashboard.html',
            {'request': request, 'error': 'Only text files are allowed'}
        )

    # Check file size
    if file.size > cfg.max_content_size:
        return templates.TemplateResponse(
            'dashboard.html',
            {'request': request, 'error': 'File size exceeds limit of 50 MB'}
        )
    
    # Use secure_filename to prevent directory traversal attacks
    from werkzeug.utils import secure_filename
    filename = secure_filename(file.filename)
    
    # Save the file
    project_root = os.getcwd()
    store_path = f'{project_root}/content/files'
 
    if not os.path.exists(store_path):
        os.makedirs(store_path)
 
    input_file = os.path.join(store_path, filename)

    with open(input_file, 'wb') as buffer:
        buffer.write(await file.read())

    # Log the upload action
    logger.info(f"Admin uploaded file: {filename}")

    name, _ = tuple(filename.split('.'))
    background_tasks.add_task(convert_file, input_file, name)

    return JSONResponse(content={"message": "File uploaded successfully"})
    # return templates.TemplateResponse(
    #     'dashboard.html',
    #     {'request': request, 'message': 'File uploaded successfully'}
    # )
