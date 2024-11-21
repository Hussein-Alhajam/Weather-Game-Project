from flask import Flask
from config import Config
from extensions import db, socketio, oauth
from controllers.auth_controller import auth_bp
from controllers.room_controller import room_bp
from controllers.weather_controller import weather_bp
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions with the app
db.init_app(app)
socketio.init_app(app)
oauth.init_app(app)
jwt = JWTManager(app)

# Register Google OAuth provider
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={'scope': 'openid email profile'},
)

# Register Blueprints for routes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(room_bp, url_prefix='/room')
app.register_blueprint(weather_bp, url_prefix='/weather')

migrate = Migrate(app, db)

if __name__ == '__main__':
    socketio.run(app, debug=True)
