from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from authlib.integrations.flask_client import OAuth
from config import Config

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")
oauth = OAuth()

google = oauth.register(
    name='google',
    client_id=Config.GOOGLE_CLIENT_ID,
    client_secret=Config.GOOGLE_CLIENT_SECRET,
    server_metadata_url=Config.GOOGLE_DISCOVERY_URL,
    client_kwargs={'scope': 'openid email profile'},
)