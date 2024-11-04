from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from app.routes import summarize
from app.routes import init_socket_handlers
socketio = SocketIO(cors_allowed_origins="*")


def create_app():
    print("[APP] Creating Flask application")
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})

    print("[APP] Initializing SocketIO")
    socketio.init_app(app)

    print("[APP] Registering blueprints")
    app.register_blueprint(summarize)

    print("[APP] Setting up socket handlers")
    init_socket_handlers(socketio)

    print("[APP] Application setup complete")
    return app
