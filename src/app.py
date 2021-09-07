from authlib.integrations.flask_client import OAuth
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi.responses import HTMLResponse
#from starsessions import SessionMiddleware


app = FastAPI(title="Pavlok Python Client", version="0.1.0")
# we need this to save temporary code & state in session
#app.add_middleware(SessionMiddleware, secret_key="DiFAdW#8UNVR%M")
app.add_middleware(SessionMiddleware, secret_key='secret')#, autoload=True)





class Pavlok:
    token: int = None

        
    def set(self,value, request:Request):
#        session['pavlok-token'] = value
        request.session['pavlok-token'] = value

        return 'ok'


    def get(self,request:Request):
        return request.session['pavlok-token']
    
    def clear(self,request:Request):
        request.session.clear()#['pavlok-token'] = None
        return 'ok'
    
config = Config('.env')  # read config from .env file
oauth = OAuth(config)
oauth.register(
    name='pavlok',
    access_token_url=config('access_token_url'),
    client_id=config('client_id'),
    client_secret=config('client_secret'),
#   access_token_params=config('access_token_params'),
    authorize_url=config('authorize_url'),
#   authorize_params=config('authorize_params'),
    authorize_params=None,
    api_base_url=config('api_base_url')
)

pavlok_client = oauth.create_client('pavlok')

pavlok = Pavlok()

@app.get('/')
async def dashboard(request: Request):
    ret_html= "<a href='/login'>Login</a>"
    return HTMLResponse(content=ret_html,status_code=200)

@app.get('/authorize')
async def authorize(request: Request):
    token = await oauth.pavlok.authorize_access_token(request)
    pavlok.token = token
    pavlok.set(token,request)
    user = await oauth.pavlok.parse_id_token(request, token)
    ret_html= str(token) + "\n\n<a href='/vibrate'>vibrate</a>"
    return HTMLResponse(content=ret_html,status_code=200)

@app.get('/login')
async def login(request: Request):
    #redirect_uri = url_for('authorize', _external=True)
    redirect_uri = request.url_for('authorize')
    return await oauth.pavlok.authorize_redirect(request, redirect_uri)


@app.get("/logout")
async def logout(request: Request):
    return pavlok.clear(request)

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

@app.get('/get_token')
async def get_token(request: Request):
    return pavlok.get(request)

@app.get('/set_token')
async def set_token(request: Request):
    return pavlok.set(request)