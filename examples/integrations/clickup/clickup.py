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
import sqlite3
from pyclickup import ClickUp

from pavlok.main import Pavlok


connection = sqlite3.connect('clickup.db', check_same_thread=False)
cursor = connection.cursor()

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


def connect_clickup(pavlok_user_id, clickup_token):
    # "ON CONFLICT (pavlok_user_id) DO UPDATE SET access_token = excluded.access_token"
    query = (
        "INSERT INTO clickup(access_token, pavlok_user_id) VALUES('{0}', '{1}')"
        "".format(clickup_token, pavlok_user_id)
    )
    cursor.execute(query)
    cursor.connection.commit()


def disconnect_clickup(pavlok_user_id):
    query = (
        "DELETE FROM clickup WHERE pavlok_user_id='{0}'"
        "".format(pavlok_user_id)
    )
    cursor.execute(query)
    cursor.connection.commit()


def get_clickup_token(pavlok_user_id):
    clickup_token_query = "SELECT id, pavlok_user_id, access_token FROM clickup WHERE pavlok_user_id = '{0}' LIMIT 1".format(
        pavlok_user_id
    )
    results = cursor.execute(clickup_token_query).fetchall()
    if len(results) == 0:
        return False, False, "ClickUp not integrated for user"
    else:
        result = results[0]
        if not result[2]:
            return True, False, "Clickup not connected for user"
        else:
            return True, True, result


def get_clickup_tasks(pavlok_user_id):
    is_integrated, is_token_present, result = get_clickup_token(pavlok_user_id)
    if not is_integrated or not is_token_present:
        return is_integrated, is_token_present, result
    else:

        clickup = ClickUp(result[2])

        main_team = clickup.teams[0]

        tasks = clickup._get_tasks(team_id=main_team.id)
        return is_integrated, is_token_present, tasks


@app.on_event("shutdown")
async def database_disconnect():
    await connection.close()


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
    code = request.query_params.get("code")
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
    connect_clickup(pavlok.token["user"]["id"], resp["access_token"])
    return RedirectResponse(url="/clickup")


@app.get("/clickup/disconnect")
def clickup_login(request: Request):
    disconnect_clickup(pavlok.token["user"]["id"])
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
    create_table_query = (
        "CREATE TABLE IF NOT EXISTS clickup ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "pavlok_user_id INTEGER, "
        "access_token TEXT NOT NULL"
        ")"
    )
    cursor.execute(create_table_query)
    uvicorn.run(app="clickup:app", port=8000, reload=True)
