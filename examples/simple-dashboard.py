import os
from os.path import join, dirname
from starlette.requests import Request
from dotenv import load_dotenv
from pavlok.main import Pavlok


dotenv_path = join(dirname(__file__), "../.env")
load_dotenv(dotenv_path)

pavlok = Pavlok(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    title="Pavlok Python Client",
)
pavlok.start()


@pavlok.app.get("/")
async def dashboard(request: Request):
    token = await pavlok.authorize(request)
    print("--->")
    return pavlok.dashboard(request)


async def send_vibrate():
    for i in range(3):
        await pavlok.vibrate()

if __name__ == "__main__":
    send_vibrate()