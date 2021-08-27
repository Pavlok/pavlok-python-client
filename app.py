from flask import Flask, jsonify, url_for, session
from flask_session import Session
from authlib.integrations.flask_client import OAuth

class Pavlok:
    token: int = None

app = Flask(__name__)
app.secret_key = "DiFAdW#8UNVR%M"
oauth = OAuth(app)
github = oauth.register('github', {...})
oauth.register(
    name='pavlok',
    client_id='f4037a18271857d6512700426dfe93ae80e96033c55017c84989adad67ea6087',
    client_secret='21f1b59b17e88f657bdcc5f8cbe8abb0128ee722b8b400799bec7b1665d3e2b6',
    access_token_url='https://app.pavlok.com/oauth/token',
    access_token_params=None,
    authorize_url='https://app.pavlok.com/oauth/authorize',
    authorize_params=None,
    api_base_url='https://app.pavlok.com/api/v1/stimuli',
  #  client_kwargs={'scope': 'user:email'},
)

pavlok_client = oauth.create_client('pavlok')

pavlok = Pavlok()

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    #redirect_uri = ""
    return pavlok_client.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = pavlok_client.authorize_access_token()
    pavlok.token = token
    # you can save the token into database
    profile = pavlok_client.get('/user', token=token)
    #return jsonify(profile)
    print(profile)
    return pavlok.token

@app.route("/vibrate")
def vibrate():
   v = pavlok_client.post('/api/v1/stimuli/vibration/200',  token=pavlok.token) #reason="API /vibrate sent!",
   print(v)
   return (v.text) 
@app.route('/get_token')
def get_token():
    return pavlok.token