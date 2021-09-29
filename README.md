# Pavlok Python Client
## Purpose
The Pavlok package makes it easy to play with your Pavlok device.

It works in two modes
- local development mode
- server mode

### Local Mode 

It can be used to play around with your device in a local development environment. It spins up a simple `FastAPI` server.

### Server Mode

It can be used to plug the module into your existing express server and build features/workflows for your pavlok device. 

## Installation

### Using pip

```
pip install pavlok
```

## Setup

You would need two keys for the module to work
- `Client ID`
- `Client Secret`

Navigate [here](http://pavlok-mvp.herokuapp.com/oauth/applications) and login with your Pavlok account to get one.

You'll need to choose a callback URL of `http://localhost:8000/authorize` for local mode.

## Usage

First thing you'd need to do is import the module into your app.

```
from pavlok.client import Pavlok
```

The simplest and quickest way to start using the module is to try it in the local mode.

```
pavlok = Pavlok(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    title="Pavlok Python Client",
)
pavlok.start()
```

This spins up a server on port 8000.  (ex: http://localhost:8000/). 

It initializes the Pavlok. Now you can login and start sending the stimuli to your device.

If you would like to configure a custom port for the local mode, you can do so by passing a custom options object as the third paramater to the `init` method. Make sure to mention the port in the callback URL of application you created [here](http://pavlok-mvp.herokuapp.com/oauth/applications)

```
pavlok = Pavlok(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    title="Pavlok Python Client",
)
pavlok.start()
```
To Use the module in the server mode, you would need to pass a couple of more options in the the `init` method and ensure you call it before your server starts listening

```
pavlok = Pavlok(
    client_id=os.environ.get("client_id"),
    client_secret=os.environ.get("client_secret"),
    title="Pavlok Python Client",
)

app = FastAPI(title=self.title, version="0.1.0")

app.add_middleware(SessionMiddleware, secret_key="secret")

@app.get("/authorize")
async def authorize(request: Request):
    token = await pavlok.authorize(request)
    user = self.get_user(request)
    return token
```

Now that you are authenticated, you can start sending the stimuli to your Pavlok device from the server.

Stimuli methods for the server mode take a required parameter in the options object i.e. `request`. It is the request object that `FastAPI` gets when one of it's api is called. Stimuli methods expects an authorization token stored on the request object to verify the user.

So a simple call to one of the stimuli method would look like

```
@app.get("/vibrate")
@app.get("/vibrate/{strength}")
async def vibrate(request: Request, strength: str = "200"):
    if self.token is None:
        response = RedirectResponse(url="/login")
        return response
    stimuli_response = await self.vibrate(strength=strength)
    return templates.TemplateResponse(
        "index.html", {"request": request, "token": self.token, "message": stimuli_response}, status_code=200
    )
```

### License
Licensed under the ISC license. 