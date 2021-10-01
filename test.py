# Author: Third Musketeer
# -*- coding: utf-8 -*-
import os
from os.path import join, dirname
from starlette.requests import Request
from dotenv import load_dotenv
from src.pavlok.main import Pavlok


dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

pavlok = Pavlok(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    title="Pavlok Python Client",
)


if __name__ == "__main__":
    pavlok.start()
