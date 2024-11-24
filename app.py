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


# Register Blueprints for routes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(room_bp, url_prefix='/room')
app.register_blueprint(weather_bp, url_prefix='/weather')

migrate = Migrate(app, db)

if __name__ == '__main__':
    socketio.run(app, debug=True)
