"""
Rotas relacionadas ao uso das maquinas, tais como: finalizacao de ops, listagem de ops, listagem das opcoes para exportacao
"""

from flask import Blueprint 
from flask import request
from os import environ
from libs.tools import paramatters
from libs.tools import handle
from libs.database import app_dbc

machines_routes = Blueprint('machines_routes', __name__, url_prefix="/app")

@machines_routes.route("/read/sensor-data", methods = ['GET'])
def machines_read_sensor_data_endpoint():
    """
    Retorne os dados dos sensores de determinada maquina
    ---
    parameters:
      - name: machine_id
        description: O ID da maquina
        type: string
        example: 229
        required: true
      - name: date
        description: A data para a qual os dados do sensor devem ser buscados, no formato 'YYYY-MM-DD'. 
                     Se não for fornecido, busca os dados da data atual.
        type: string
        example: '2023-11-12'
        required: false
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
        "machine_id": request.args.get("machine_id"),
        "date": request.args.get("date")  # Adicionando o parâmetro date
    }

    # validação e cast dos parâmetros de entrada  
    validation, parameters, code = paramatters.wizzard(machines_read_sensor_data_endpoint.__doc__, received_parameters)
    if code == 400:
        return validation
    
    machine_id = parameters["machine_id"]
    date = parameters.get("date")  # Obtendo o valor de date, que pode ser None

    response = app_dbc.get_machine_sensor_data(machine_id=machine_id, date=date)

    return {
        "data": "Dados de sensores retornados com sucesso",
        "sensor_data": response,
        "code": 200
    }
