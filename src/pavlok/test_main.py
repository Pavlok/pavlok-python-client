# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from multiprocessing import Process
import uvicorn

from .main import Pavlok


token = {
    "access_token": "",
    "token_type": "bearer",
    "expires_in": 2629746,
    "refresh_token": "",
    "unique_hash": "",
    "expires_at": 1635953475,
}


dotenv_path = join(dirname(__file__), "../../.env")
load_dotenv(dotenv_path)

pavlok = Pavlok(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    title="Pavlok Python Client",
    token=token,
)
pavlok.start(from_testing=True)
client = TestClient(pavlok.app)


def test_vibrate():
    response = client.get("/vibrate")
    assert response.status_code == 200


def test_beep():
    response = client.get("/beep")
    assert response.status_code == 200


def test_zap():
    response = client.get("/zap")
    assert response.status_code == 200
