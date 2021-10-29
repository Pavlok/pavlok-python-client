# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
import requests
from fastapi import APIRouter, Depends
from starlette.requests import Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app import pavlok, templates
from .services import get_projects, connect_todoist, disconnect_todoist
from core.database import get_db

router = APIRouter()


@router.get("")
def todoist(request: Request, db: Session = Depends(get_db)):
    if pavlok.token is None:
        response = RedirectResponse(url="/login")
        return response

    is_integrated, is_token_present, projects = get_projects(
        pavlok.token["user"]["id"], db
    )
    context = {
        "request": request,
        "token": pavlok.token,
        "is_integrated": is_integrated,
        "is_token_present": is_token_present,
        "projects": projects,
    }

    return templates.TemplateResponse("todoist.html", context, status_code=200)


# https://todoist.com/oauth/authorize?client_id=0123456789abcdef&scope=data:read,data:delete&state=secretstring
@router.get("/login")
def todoist_login(request: Request):
    todoist_auth_url = "https://todoist.com/oauth/authorize?client_id={0}&scope=data:read&state={1}".format(
        os.environ.get("TODOIST_CLIENT_ID"),
        os.environ.get("TODOIST_CLIENT_SECRET"),
    )
    return RedirectResponse(url=todoist_auth_url)


@router.get("/callback")
def todoist_auth_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    payload = {
        "client_id": os.environ.get("TODOIST_CLIENT_ID"),
        "client_secret": os.environ.get("TODOIST_CLIENT_SECRET"),
        "code": code,
    }
    todoist_token_resp = requests.post(
        "https://todoist.com/oauth/access_token", data=payload
    )
    resp = todoist_token_resp.json()
    connect_todoist(pavlok.token["user"]["id"], resp["access_token"], db)
    return RedirectResponse(url="/todoist")

