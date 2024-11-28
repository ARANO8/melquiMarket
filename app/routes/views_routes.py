from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from app.utils.auth import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/views")

@router.get("/")
def get_signin_page(request: Request):
    return templates.TemplateResponse("SignIn.html", {"request": request})

@router.get("/dashboard")
def get_dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/Products")
def get_products_page(request: Request):
    return templates.TemplateResponse("tablesProducts.html", {"request": request})

@router.get("/Users")
def get_users_page(request: Request):
    return templates.TemplateResponse("tablesUsers.html", {"request": request})

# @router.get("/dashboard")
# def get_dashboard_page(request: Request, current_user = Depends(get_current_user)):
#     return templates.TemplateResponse("dashboard.html", {"request": request, "user": current_user})

# @router.get("/tablesProducts")
# def get_tables_products_page(request: Request, current_user = Depends(get_current_user)):
#     return templates.TemplateResponse("tablesProducts.html", {"request": request, "user": current_user})

# @router.get("/tablesUsers")
# def get_tables_users_page(request: Request, current_user = Depends(get_current_user)):
#     return templates.TemplateResponse("tablesUsers.html", {"request": request, "user": current_user})
