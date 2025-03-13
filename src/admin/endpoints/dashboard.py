# src/endpoints/distro.py

import os
from fastapi import APIRouter, BackgroundTasks, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi import File, UploadFile

from src.common.logger_setup import get_logger
from src.admin.services import convert_file
from src.admin.templates import templates

logger = get_logger(__name__)

router = APIRouter()


# Display the upload form
@router.get('/dashboard', response_class=HTMLResponse)
def upload_form(request: Request):
    return templates.TemplateResponse('dashboard.html', {'request': request})


MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
# Handle the file upload
@router.post('/upload')
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
    if file.size > MAX_CONTENT_LENGTH:
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
    # output_file = os.path.join(content_path, name)
    background_tasks.add_task(convert_file, input_file, name)

    return templates.TemplateResponse(
        'dashboard.html',
        {'request': request, 'message': 'File uploaded successfully'}
    )
