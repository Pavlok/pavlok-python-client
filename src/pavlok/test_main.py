# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from .main import Pavlok

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

pavlok = Pavlok(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    title="Pavlok Python Client",
)
pavlok.start()


@pavlok.app.on_event("startup")
async def startup_event():
    token = await pavlok.authorize(request)

client = TestClient(pavlok.app)


def test_vibrate():
    response = client.get("/vibrate")
    assert response.status_code == 200
