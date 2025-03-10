# src/endpoints/distro.py

import os
from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi import File, UploadFile

from src.admin.templates import templates

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
    file_path = os.path.join('content', 'files', filename)
    with open(file_path, 'wb') as buffer:
        buffer.write(await file.read())

    # Log the upload action
    # logger.info(f"Admin {current_user.email} uploaded file: {filename}")

    return templates.TemplateResponse(
        'dashboard.html',
        {'request': request, 'message': 'File uploaded successfully'}
    )
