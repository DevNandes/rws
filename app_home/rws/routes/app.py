"""
Rotas relacionadas ao uso das maquinas, tais como: finalizacao de ops, listagem de ops, listagem das opcoes para exportacao
"""

from flask import Blueprint 
from flask import request
from os import environ
from libs.tools import paramatters
from libs.tools import handle
from libs.database import app_dbc

teste_routes = Blueprint('teste_routes', __name__, url_prefix="/testes")

@teste_routes.route("/hello-world", methods = ['GET'])
def teste_rotas_endpoint():
    """
    Retorne os dados dos sensores de determinada maquina
    ---
    parameters:
      - name: teste
        description: UMa string aleatoria para retornar
        type: string
        example: Hello World
        required: true
    responses:
      200:
        description: Dados de sensores retornados com sucesso
        examples:
          application/json: { 
              "data": "Dados de sensores retornados com sucesso",
              "code": 200
          }
    """

    received_parameters = {
        "teste": request.args.get("teste"),
    }

    # validação e cast dos parâmetros de entrada  
    validation, parameters, code = paramatters.wizzard(teste_rotas_endpoint.__doc__, received_parameters)
    if code == 400:
        return validation
    
    teste = parameters["teste"]

    response = app_dbc.get_teste(teste)

    return {
        "data": "Dados de sensores retornados com sucesso",
        "sensor_data": response,
        "code": 200
    }
