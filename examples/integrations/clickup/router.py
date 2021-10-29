# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
import requests
from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from starlette.requests import Request
from sqlalchemy.orm import Session

from app import pavlok, templates
from .services import get_tasks, connect_clickup, disconnect_clickup
from core.database import get_db

router = APIRouter()


@router.get("")
def clickup(request: Request, db: Session = Depends(get_db)):
    if pavlok.token is None:
        response = RedirectResponse(url="/login")
        return response

    is_integrated, is_token_present, tasks = get_tasks(pavlok.token["user"]["id"], db)
    clickup_context = {
        "request": request,
        "token": pavlok.token,
        "is_integrated": is_integrated,
        "is_token_present": is_token_present,
        "tasks": tasks,
    }

    return templates.TemplateResponse("clickup.html", clickup_context, status_code=200)


@router.get("/login")
def clickup_login(request: Request):
    clickup_auth_url = (
        "https://app.clickup.com/api?client_id={0}&redirect_uri={1}".format(
            os.environ.get("CLICKUP_CLIENT_ID"), os.environ.get("CLICKUP_REDIRECT_URI")
        )
    )
    return RedirectResponse(url=clickup_auth_url)


@router.get("/callback")
def clickup_auth_callback(request: Request, db: Session = Depends(get_db)):
    code = request.query_params.get("code")
    payload = {
        "client_id": os.environ.get("CLICKUP_CLIENT_ID"),
        "client_secret": os.environ.get("CLICKUP_CLIENT_SECRET"),
        "grant_type": "authorization_code",
        "code": code,
    }
    clickup_token_resp = requests.post(
        "https://app.clickup.com/api/v2/oauth/token", data=payload
    )
    print(clickup_token_resp)
    resp = clickup_token_resp.json()
    connect_clickup(pavlok.token["user"]["id"], resp["access_token"], db)
    return RedirectResponse(url="/clickup")


@router.get("/disconnect")
def clickup_disconnect(request: Request, db: Session = Depends(get_db)):
    disconnect_clickup(pavlok.token["user"]["id"], db)
    return RedirectResponse(url="/clickup")
