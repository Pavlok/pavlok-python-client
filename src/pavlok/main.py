# Author: Third Musketeer
# -*- coding: utf-8 -*-

"""
    Pavlok Python Client

"""
from os.path import dirname, join
from authlib.integrations.starlette_client import OAuth
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
import uvicorn

from .enums import StimulusType
from .constants import PAVLOK_BASE_URL, PAVLOK_API_BASE_URL
from .utils import get_stimulus_api_url
from .pavlok_response_models import StimuliResponse

PavlokOAuth = OAuth()

template_path = join(dirname(__file__), "templates")

templates = Jinja2Templates(directory=template_path)


class Pavlok:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        title: str,
        token: Optional[str] = None,
        name: Optional[str] = "pavlok",
        access_token_url: Optional[str] = PAVLOK_BASE_URL + "oauth/token/",
        access_token_params: Optional[str] = None,
        authorize_url: Optional[str] = PAVLOK_BASE_URL + "oauth/authorize/",
        authorize_params: Optional[str] = None,
        api_base_url: Optional[str] = PAVLOK_API_BASE_URL,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None if token is None else token
        self.name = name
        self.access_token_url = access_token_url
        self.authorize_url = authorize_url
        self.api_base_url = api_base_url
        self.title = title
        self.app = None

        PavlokOAuth.register(
            name=self.name,
            access_token_url=self.access_token_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            authorize_url=self.authorize_url,
            api_base_url=self.api_base_url,
        )

        self.client = PavlokOAuth.create_client(self.name)

    def set_token(self, token, request: Request):
        request.session["pavlok-token"] = token
        self.token = token
        return token

    def get_token(self):
        return self.token

    def clear_token(self, request: Request):
        request.session.clear()
        self.token = None

    async def get_user(self, request: Request):
        return await PavlokOAuth.pavlok.parse_id_token(request, self.token)

    async def login(self, request: Request, redirect_url):
        return await PavlokOAuth.pavlok.authorize_redirect(request, redirect_url)

    async def authorize(self, request: Request):
        token = await PavlokOAuth.pavlok.authorize_access_token(request)
        self.set_token(token, request)
        return token

    async def send_stimulus(
        self, stimulus_type: str, strength: str = "200", reason: str = ""
    ):
        if stimulus_type not in [stimulus.value for stimulus in StimulusType]:
            return False, "Invalid stimulus"
        stimulus_api_url = get_stimulus_api_url(stimulus_type, strength)
        resp = await self.client.post(stimulus_api_url, token=self.token)
        return resp.text, stimulus_api_url

    async def vibrate(self, strength: str = "200", reason: str = ""):
        return await self.send_stimulus("vibration", strength, reason)

    async def beep(self, strength: str = "200", reason: str = ""):
        return await self.send_stimulus("beep", strength, reason)

    async def zap(self, strength: str = "200", reason: str = ""):
        return await self.send_stimulus("zap", strength, reason)

    def start(self, port: int = 8000, from_testing: bool = False):
        self.app = FastAPI(title=self.title, version="0.1.0")

        self.app.add_middleware(SessionMiddleware, secret_key="secret")

        @self.app.get("/authorize", response_class=RedirectResponse)
        async def authorize(request: Request):
            token = await self.authorize(request)
            user = self.get_user(request)
            return RedirectResponse(url="/")

        @self.app.get("/", response_class=HTMLResponse)
        def dashboard(request: Request):
            return templates.TemplateResponse(
                "index.html", {"request": request, "token": self.token}, status_code=200
            )

        @self.app.get("/login", response_class=RedirectResponse)
        async def login(request: Request):
            if self.token:
                return RedirectResponse(url="/")
            redirect_uri = request.url_for("authorize")
            return await self.login(request, redirect_uri)

        @self.app.get("/logout", response_class=RedirectResponse)
        async def logout(request: Request):
            self.clear_token(request)
            return RedirectResponse(url="/")

        @self.app.get(
            "/vibrate",
            response_model=StimuliResponse.StimuliSchema,
            responses=StimuliResponse.get_stimuli_response(
                StimulusType.VIBRATION.value
            ),
        )
        async def vibrate(request: Request, strength: str = "200"):
            if self.token is None:
                response = RedirectResponse(url="/login")
                return response
            stimuli_response = await self.vibrate(strength=strength)
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "token": self.token, "message": stimuli_response},
                status_code=200,
            )

        @self.app.get(
            "/beep",
            response_model=StimuliResponse.StimuliSchema,
            responses=StimuliResponse.get_stimuli_response(StimulusType.BEEP.value),
        )
        async def beep(request: Request, strength: str = "200"):
            if self.token is None:
                response = RedirectResponse(url="/login")
                return response
            stimuli_response = await self.beep(strength=strength)
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "token": self.token, "message": stimuli_response},
                status_code=200,
            )

        @self.app.get(
            "/zap",
            response_model=StimuliResponse.StimuliSchema,
            responses=StimuliResponse.get_stimuli_response(StimulusType.ZAP.value),
        )
        async def zap(request: Request, strength: str = "200"):
            if self.token is None:
                response = RedirectResponse(url="/login")
                return response
            stimuli_response = await self.zap(strength=strength)
            return templates.TemplateResponse(
                "index.html",
                {"request": request, "token": self.token, "message": stimuli_response},
                status_code=200,
            )

        @self.app.get("/get_token")
        async def get_token(request: Request):
            return self.get_token()

        @self.app.post("/set_token")
        async def set_token(token: str, request: Request):
            return self.set_token(token, request)

        if not from_testing:
            uvicorn.run(app=self.app, port=port)
