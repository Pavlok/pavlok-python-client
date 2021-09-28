from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from starlette.config import Config
from fastapi.responses import HTMLResponse

from pavlok.client import Pavlok

app = FastAPI(title="Pavlok Python Client", version="0.1.0")
# we need this to save temporary code & state in session
# app.add_middleware(SessionMiddleware, secret_key="DiFAdW#8UNVR%M")
app.add_middleware(SessionMiddleware, secret_key="secret")  # , autoload=True)

config = Config(".env")  # read config from .env file

pavlok = Pavlok(client_id=config("client_id"), client_secret=config("client_secret"))


@app.get("/")
async def dashboard(request: Request):
    ret_html = "<a href='/login'>Login</a>"
    return HTMLResponse(content=ret_html, status_code=200)


@app.get("/authorize")
async def authorize(request: Request):
    token = await pavlok.authorize(request)
    user = pavlok.get_user(request)
    print(user)
    ret_html = str(token) + "\n\n<a href='/vibrate'>vibrate</a>"
    return HTMLResponse(content=ret_html, status_code=200)


@app.get("/login")
async def login(request: Request):
    redirect_uri = request.url_for("authorize")
    return await pavlok.login(request, redirect_uri)


@app.get("/logout")
async def logout(request: Request):
    return pavlok.clear_token(request)


@app.get("/vibrate")
@app.get("/vibrate/{strength}")
async def vibrate(strength: str = "200"):
    if pavlok.token is None:
        response = RedirectResponse(url="/login")
        return response
    return await pavlok.vibrate(strength=strength)


@app.get("/beep")
@app.get("/beep/{strength}")
async def beep(strength: str = "200"):
    if pavlok.token is None:
        response = RedirectResponse(url="/login")
        return response
    return await pavlok.beep(strength=strength)


@app.get("/zap")
@app.get("/zap/{strength}")
async def zap(strength: str = "200"):
    if pavlok.token is None:
        response = RedirectResponse(url="/login")
        return response
    return await pavlok.zap(strength=strength)


@app.get("/get_token")
async def get_token(request: Request):
    return pavlok.get_token()


@app.post("/set_token")
async def set_token(token: str, request: Request):
    return pavlok.set_token(token, request)
