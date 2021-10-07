# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import uvicorn
import requests

from pavlok.main import Pavlok
from services import get_clickup_tasks, add_integration

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

template_path = join(dirname(__file__), "templates")

templates = Jinja2Templates(directory=template_path)

pavlok = Pavlok(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    title="Pavlok Python Client",
)

app = FastAPI(title=pavlok.title, version="0.1.0")

static_path = join(dirname(__file__), "static")

app.mount("/static", StaticFiles(directory=static_path), name="static")

app.add_middleware(SessionMiddleware, secret_key="secret")


@app.get("/authorize")
async def authorize(request: Request):
    token = await pavlok.authorize(request)
    user = pavlok.get_user(request)
    return RedirectResponse(url="/")


@app.get("/")
def dashboard(request: Request):
    if pavlok.token:
        template = "index.html"
    else:
        template = "login.html"
    return templates.TemplateResponse(
        template, {"request": request, "token": pavlok.token}, status_code=200
    )


@app.get("/clickup")
def clickup(request: Request):
    if pavlok.token is None:
        response = RedirectResponse(url="/login")
        return response

    is_integrated, is_token_present, tasks = get_clickup_tasks(
        pavlok.token["user"]["id"]
    )
    clickup_context = {
        "request": request,
        "token": pavlok.token,
        "is_integrated": is_integrated,
        "is_token_present": is_token_present,
        "tasks": tasks,
    }

    return templates.TemplateResponse("clickup.html", clickup_context, status_code=200)


@app.get("/clickup/login")
def clickup_login(request: Request):
    print(os.environ.get("clickup_client_id"))
    clickup_auth_url = (
        "https://app.clickup.com/api?client_id={0}&redirect_uri={1}".format(
            os.environ.get("clickup_client_id"), os.environ.get("clickup_redirect_uri")
        )
    )
    return RedirectResponse(url=clickup_auth_url)


@app.get("/clickup/callback")
def clickup_auth_callback(request: Request):
    print(request.query_params)
    code = request.query_params.get('code')
    payload = {
        "client_id": os.environ.get("clickup_client_id"),
        "client_secret": os.environ.get("clickup_client_secret"),
        "grant_type": "authorization_code",
        "code": code,
    }
    clickup_token_resp = requests.post(
        "https://app.clickup.com/api/v2/oauth/token", data=payload
    )
    print(clickup_token_resp)
    resp = clickup_token_resp.json()
    add_integration(pavlok.token["user"]["id"], resp["access_token"])
    return RedirectResponse(url="/clickup")


@app.get("/login")
async def login(request: Request):
    if pavlok.token:
        return RedirectResponse(url="/")
    redirect_uri = request.url_for("authorize")
    return await pavlok.login(request, redirect_uri)


@app.get("/logout")
async def logout(request: Request):
    pavlok.clear_token(request)
    return RedirectResponse(url="/")


@app.get("/vibrate")
@app.get("/vibrate/{strength}")
async def vibrate(request: Request, strength: str = "200"):
    if pavlok.token is None:
        response = RedirectResponse(url="/login")
        return response
    stimuli_response = await pavlok.vibrate(strength=strength)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "token": pavlok.token, "message": stimuli_response},
        status_code=200,
    )


@app.get("/beep")
@app.get("/beep/{strength}")
async def beep(request: Request, strength: str = "200"):
    if pavlok.token is None:
        response = RedirectResponse(url="/login")
        return response
    stimuli_response = await pavlok.beep(strength=strength)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "token": pavlok.token, "message": stimuli_response},
        status_code=200,
    )


@app.get("/zap")
@app.get("/zap/{strength}")
async def zap(request: Request, strength: str = "200"):
    if pavlok.token is None:
        response = RedirectResponse(url="/login")
        return response
    stimuli_response = await pavlok.zap(strength=strength)
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "token": pavlok.token, "message": stimuli_response},
        status_code=200,
    )


@app.get("/get_token")
async def get_token(request: Request):
    return pavlok.get_token()


@app.post("/set_token")
async def set_token(token: str, request: Request):
    return pavlok.set_token(token, request)


if __name__ == "__main__":
    uvicorn.run(app="clickup:app", port=8000, reload=True)
