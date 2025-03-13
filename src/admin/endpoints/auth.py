from fastapi import APIRouter, BackgroundTasks, Request, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse

router = APIRouter()

@router.post('/login')
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    access_token = 'test_th_client_token'
    response = RedirectResponse('/adm/dashboard', status_code=status.HTTP_302_FOUND)
    response.set_cookie(
        key='access_token',
        value=f'Bearer {access_token}',
        httponly=True
    )
    # Set the Secure flag if the site uses HTTPS:
    # response.set_cookie(key='access_token', value=f'Bearer {access_token}', httponly=True, secure=True)
    return response


@router.get('/logout')
def logout():
    response = RedirectResponse('/adm', status_code=status.HTTP_302_FOUND)
    response.delete_cookie('access_token')
    return response
