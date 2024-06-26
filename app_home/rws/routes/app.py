"""
Rotas relacionadas a gestao do aplicativo
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
from libs.tools import paramatters, handle
from libs.database import app_dbc

app_routes = Blueprint('app_routes', __name__, url_prefix="/app")

@app_routes.route("/login", methods=['POST'])
def executa_login_endpoint():
    """
    Retorne um JWT token para o usuario
    ---
    parameters:
      - name: email
        description: Email do usuario para logar
        type: string
        example: teste@gmail.com
        required: true
      - name: password
        description: Uma senha usada pelo usuario para login
        type: string
        example: catatau2023
        required: true
    responses:
      200:
        description: Login Realizado com sucesso
        examples:
          application/json: {
              "jwtToken": "DSAJNAD76DS87ASD5ASD78AD6SAD78ASD5",
              "code": 200
          }
    """

    received_parameters = {
        "email": request.form.get("email"),
        "password": request.form.get("password")
    }

    # Validação e cast dos parâmetros de entrada
    validation, parameters, code = paramatters.wizzard(executa_login_endpoint.__doc__, received_parameters)
    if code == 400:
        return jsonify(validation), 400
    
    email = parameters["email"]
    password = parameters["password"]

    handle.info(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'))

    # Busca a senha armazenada no banco de dados
    response = app_dbc.get_senha(email=email)
    if not response:
        return jsonify({
            "mensagem": "Email nao cadastrado favor entrar em contato com o administrador!",
            "code": 404
        }), 404

    stored_password = response[0].get("senhaUsuario")
    try:
        if not bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return jsonify({
                "mensagem": "Email ou senha incorretos, por favor tente novamente!",
                "code": 401
            }), 401
    except ValueError:
        return jsonify({
            "mensagem": "Erro interno ao verificar a senha. Contate o administrador.",
            "code": 500
        }), 500
    
    # Gera o token JWT
    access_token = create_access_token(identity={"email": email, "idUsuario": response[0].get("idUsuario")})

    return jsonify({
        "mensagem": "Login Realizado com sucesso",
        "jwtToken": access_token,
        "nomeUsuario": response[0].get("nomeUsuario"),
        "linguagem": response[0].get("linguagemUsuario"),
        "idPerfil": response[0].get("idPerfil"),
        "nomePerfil": response[0].get("nomePerfil"),
        "tema": response[0].get("temaUsuario"),
        "code": 200
    }), 200

@app_routes.route("/cadastro", methods=['POST'])
def cadastro_usuario():
    """
    Cadastra um novo usuario
    ---
    parameters:
      - name: username
        description: Nome do usuario
        type: string
        example: Raphael Fernandes
        required: true
      - name: email
        description: Email do usuario
        type: string
        example: raphaelfernandes1607@gmail.com
        required: true
      - name: password
        description: Senha do usuario
        type: string
        example: catatau2023
        required: true
    responses:
      201:
        description: Cadastro realizado com sucesso
        examples:
          application/json: {
              "mensagem": "Cadastro realizado com sucesso",
              "code": 201
          }
    """

    received_parameters = {
        "username": request.form.get("username"),
        "email": request.form.get("email"),
        "password": request.form.get("password")
    }

    # Validação e cast dos parâmetros de entrada
    validation, parameters, code = paramatters.wizzard(cadastro_usuario.__doc__, received_parameters)
    if code == 400:
        return jsonify(validation), 400

    username = parameters["username"]
    email = parameters["email"]
    password = parameters["password"]

    # Criptografar a senha
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Cadastrar o novo usuário
    try:
        app_dbc.cadastrar_usuario(username, email, hashed_password)
        return jsonify({
            "mensagem": "Cadastro realizado com sucesso",
            "code": 201
        }), 201
    except Exception as e:
        handle.error(f"Erro ao cadastrar usuário: {e}")
        return jsonify({
            "mensagem": "Erro ao cadastrar usuário, tente novamente mais tarde.",
            "code": 500
        }), 500
    
@app_routes.route("/menus", methods=['GET'])
@jwt_required()
def busca_menus_usuario():
    """
    Busca menus que usuario tem acesso
    ---
    parameters:
      - name: idUsuario
        description: id do usuario
        type: integer
        example: 1
        required: true
    responses:
      200:
        description: Menus do usuario encontrados com sucesso
        examples:
          application/json: {
              "menus": [{}]
              "code": 200
          }
    """

    # Obtem o ID do usuário a partir do token JWT
    current_user = get_jwt_identity()
    idUsuario = current_user["idUsuario"]

    # Busca os menus do usuário
    try:
        result = app_dbc.busca_menus_usuario(idUsuario)
        return jsonify({
            "menus": result,
            "code": 200
        }), 200
    except Exception as e:
        handle.error(f"Erro ao buscar menus: {e}")
        return jsonify({
            "mensagem": "Erro ao buscar menus, tente novamente mais tarde.",
            "code": 500
        }), 500