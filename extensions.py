from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from authlib.integrations.flask_client import OAuth
from config import Config

db = SQLAlchemy()
socketio = SocketIO()
oauth = OAuth()

google = oauth.register(
    name='google',
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid email profile'},
)