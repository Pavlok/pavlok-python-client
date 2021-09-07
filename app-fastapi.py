from flask import Flask, jsonify, url_for, session, redirect
from flask_session import Session
from authlib.integrations.flask_client import OAuth
from typing import Optional

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse, Response, JSONResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi.responses import HTMLResponse


app = FastAPI(title="Pavlok Python Client", version="0.1.0")
# we need this to save temporary code & state in session
app.add_middleware(SessionMiddleware, secret_key="DiFAdW#8UNVR%M")





class Pavlok:
    token: int = None

        
    def set(self,value):
        session['pavlok-token'] = value
        return 'ok'


    def get(self):
        return session.get('pavlok-token')
    
    def clear(self):
        session['pavlok-token'] = None
        return 'ok'
    
    
#app = Flask(__name__)
#app.secret_key = "DiFAdW#8UNVR%M"
#oauth = OAuth(app)

# SESSION_TYPE = 'filesystem'
# app.config.from_object(__name__)
# Session(app)

# @app.route('/set/<key>/<value>')
# def set(key,value):
#     session[key] = value
#     return 'ok'

# @app.route('/get/<key>')
# def get(key):
#     return session.get(key)
config = Config('.env')  # read config from .env file
oauth = OAuth(config)
oauth.register(
    name='pavlok', access_token_url='https://app.pavlok.com/oauth/token',
      client_id='f4037a18271857d6512700426dfe93ae80e96033c55017c84989adad67ea6087',
    client_secret='21f1b59b17e88f657bdcc5f8cbe8abb0128ee722b8b400799bec7b1665d3e2b6',
  
    access_token_params=None,
    authorize_url='https://app.pavlok.com/oauth/authorize',
    authorize_params=None,
    api_base_url='https://app.pavlok.com/api/v1/stimuli'
)

pavlok_client = oauth.create_client('pavlok')

pavlok = Pavlok()


@app.get('/authorize')
async def authorize(request: Request):
    token = await oauth.pavlok.authorize_access_token(request)
    pavlok.token = token
    #pavlok.set(token)
    #user = await oauth.pavlok.parse_id_token(request, token)
    ret_html= str(token) + "\n\n<a href='/vibrate'>vibrate</a>"
    return HTMLResponse(content=ret_html,status_code=200)

@app.route('/login')
async def login(request: Request):
    #redirect_uri = url_for('authorize', _external=True)
    redirect_uri = request.url_for('authorize')
    return await oauth.pavlok.authorize_redirect(request, redirect_uri)


@app.get("/logout")
async def logout():
    return pavlok.clear()

@app.get("/vibrate")
@app.get("/vibrate/{strength}")
async def vibrate(strength: str = "200"):
#    sess = pavlok.get()
 #   if sess is None:
 #       pass #return redirect("/login")
        #return url_for('login', _external=True)
 #   else: 
 #       pass #       pavlok.token = sess
    if pavlok.token is None:
        response = RedirectResponse(url='/login')
        return response
    post_str = '/api/v1/stimuli/vibration/' + strength
    print("post_str: " + post_str)
    v = await pavlok_client.post( post_str,token=pavlok.token) #reason="API /vibrate sent!",
    print(v.text)
    return v.text 

@app.get("/beep")
@app.get("/beep/{strength}")
async def beep(strength: str = "200"):
#    sess = pavlok.get()
 #   if sess is None:
 #       pass #return redirect("/login")
        #return url_for('login', _external=True)
 #   else: 
 #       pass #       pavlok.token = sess
    if pavlok.token is None:
        response = RedirectResponse(url='/login')
        return response
    post_str = '/api/v1/stimuli/beep/' + strength
    print("post_str: " + post_str)
    v = await pavlok_client.post( post_str,token=pavlok.token) #reason="API /vibrate sent!",
    print(v.text)
    return v.text 

@app.get("/zap")
@app.get("/zap/{strength}")
async def beep(strength: str = "200"):
#    sess = pavlok.get()
 #   if sess is None:
 #       pass #return redirect("/login")
        #return url_for('login', _external=True)
 #   else: 
 #       pass #       pavlok.token = sess
    if pavlok.token is None:
        response = RedirectResponse(url='/login')
        return response
    post_str = '/api/v1/stimuli/zap/' + strength
    print("post_str: " + post_str)
    v = await pavlok_client.post( post_str,token=pavlok.token) #reason="API /vibrate sent!",
    print(v.text)
    return v.text 

@app.route('/get_token')
def get_token():
    return pavlok.token