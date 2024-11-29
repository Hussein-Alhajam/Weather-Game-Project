from datetime import timedelta
from flask import Flask
from backend.config import Config
from backend.extensions import db, socketio, oauth
from controllers.auth_controller import auth_bp
from controllers.room_controller import room_bp
from controllers.weather_controller import weather_bp
from controllers.game_mech_controller import game_mech_bp
from controllers.inventory_controller import inventory_bp
from controllers.resource_controller import resource_bp
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, verify_jwt_in_request
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
app.register_blueprint(game_mech_bp, url_prefix='/game')
app.register_blueprint(inventory_bp, url_prefix='/inventory')
app.register_blueprint(resource_bp, url_prefix='/resource')


migrate = Migrate(app, db)

@app.after_request
def refresh_token_on_interaction(response):
    """Refresh the access token on every authenticated user interaction."""
    try:
        # Check if the request has a valid JWT token
        verify_jwt_in_request(optional=True)
        identity = get_jwt_identity()  # Get current user from the token
        
        if identity:  # If the user is authenticated
            new_access_token = create_access_token(
                identity=identity,
                additional_claims={"user_id": identity},
                expires_delta=timedelta(hours=1)  # Extend session on interaction
            )
            response.headers["Authorization"] = f"Bearer {new_access_token}"
    except Exception:
        # Skip refreshing the token if no JWT is present or valid
        pass

    return response

if __name__ == '__main__':
    socketio.run(app, debug=True)
