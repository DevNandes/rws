from flask import Flask
from os import environ
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from libs.tools import handle

# Import de rotas
from routes.app import app_routes
from routes.riscos import riscos_routes

def create_app():
    app = Flask(environ["APP_NAME"])
    app.config['JWT_SECRET_KEY'] = environ["JWT_SECRET_KEY"]
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(environ["JWT_ACCESS_TOKEN_EXPIRES"])

    jwt = JWTManager(app)
    CORS(app)
    app.root_path = environ['APP_DIR']

    # app.handle pode ser usado para logging ou outras funções utilitárias
    app.handle = handle

    # Registro de rotas
    app.register_blueprint(app_routes)
    app.register_blueprint(riscos_routes)

    return app
