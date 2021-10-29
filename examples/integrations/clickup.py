# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import uvicorn
import requests


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
