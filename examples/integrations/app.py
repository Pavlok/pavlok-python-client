# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request

from pavlok.main import Pavlok
from core.database import Base, engine
from dotenv import load_dotenv

load_dotenv()

template_path = join(dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_path)

static_path = join(dirname(__file__), "static")


pavlok = Pavlok(
    client_id=os.environ.get("PAVLOK_CLIENT_ID"),
    client_secret=os.environ.get("PAVLOK_CLIENT_SECRET"),
    title="Pavlok Python Client",
)

app = FastAPI(title=pavlok.title, version="0.1.0")

static_path = join(dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")
app.add_middleware(SessionMiddleware, secret_key="secret")


@app.get("/")
def dashboard(request: Request):
    if pavlok.token:
        template = "index.html"
    else:
        template = "login.html"
    return templates.TemplateResponse(
        template, {"request": request, "token": pavlok.token}, status_code=200
    )


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


@app.get("/authorize")
async def authorize(request: Request):
    token = await pavlok.authorize(request)
    user = pavlok.get_user(request)
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


# @app.on_event("shutdown")
# async def database_disconnect():
#     await connection.close()
