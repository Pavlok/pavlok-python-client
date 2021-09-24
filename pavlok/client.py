# Author: Third Musketeer
# -*- coding: utf-8 -*-

"""
    Pavlok Python Client

"""

from authlib.integrations.starlette_client import OAuth
from typing import Optional
from starlette.requests import Request

from .constants import PAVLOK_BASE_URL, PAVLOK_API_BASE_URL, PAVLOK_STIMULI_API_URL

PavlokOAuth = OAuth()


class Pavlok:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
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
        self.token = None if token is None else token.strip()
        self.name = name
        self.access_token_url = access_token_url
        self.authorize_url = authorize_url
        self.api_base_url = api_base_url

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
        return True

    async def get_user(self, request: Request):
        return await PavlokOAuth.pavlok.parse_id_token(request, self.token)

    async def login(self, request: Request, redirect_url):
        return await PavlokOAuth.pavlok.authorize_redirect(request, redirect_url)

    async def authorize(self, request: Request):
        auth_token = await PavlokOAuth.pavlok.authorize_access_token(request)
        self.set_token(auth_token, request)
        return auth_token

    async def send_stimulus(
        self, stimulus_type: str, strength: str = "200", reason: str = ""
    ):
        if stimulus_type not in ["vibration", "beep", "zap"]:
            return False, "Invalid stimulus"
        stimulus_api_url = PAVLOK_STIMULI_API_URL + stimulus_type + "/" + strength + "/"
        resp = await self.client.post(stimulus_api_url, token=self.token)
        return True, resp.text, stimulus_api_url

    async def vibrate(self, strength: str = "200", reason: str = ""):
        return await self.send_stimulus("vibration", strength, reason)

    async def beep(self, strength: str = "200", reason: str = ""):
        return await self.send_stimulus("beep", strength, reason)

    async def zap(self, strength: str = "200", reason: str = ""):
        return await self.send_stimulus("zap", strength, reason)
