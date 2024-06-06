from flask import Flask
from os import environ
#from flasgger import Swagger
from flask_cors import CORS
from libs.tools import handle

# import de rotas


from routes.app import teste_routes

def create_app():
    app = Flask(environ["APP_NAME"])
    CORS(app)
    app.root_path = environ['APP_DIR']

    # documentacao do app
    #app.config['SWAGGER'] = {
    #'title': environ["APP_DESCRIPTION"],
    #"specs_route": "/documentation"
    #}
    #Swagger(app)

    app.handle = handle

    # registro de rotas
    app.register_blueprint(teste_routes)

    return app