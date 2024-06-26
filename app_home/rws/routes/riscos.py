# routes/riscos.py

"""
Rotas relacionadas aos riscos
"""

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from libs.tools import paramatters, handle
from libs.database import riscos_dbc

riscos_routes = Blueprint('riscos_routes', __name__, url_prefix="/riscos")

@riscos_routes.route("/situacoes", methods=['GET'])
@jwt_required()
def busca_dashboards_status():
    """
    Busca dados que que gera os 4 dashboards superiores sobre os status
    ---
    responses:
      200:
        description: Dados dos dashboards superiores encontrados com sucesso
        examples:
          application/json: {
              "status": [{totalRiscos: 77, riscosResolvidos: 43, riscosTrajetoria: 10, riscosProblema: 11}]
              "code": 200
          }
    """
    try:
        result = riscos_dbc.busca_dashboards_status()
        return jsonify({
            "status": result,
            "code": 200
        }), 200
    except Exception as e:
        handle.error(f"Erro ao buscar dashboards: {e}")
        return jsonify({
            "mensagem": "Erro ao buscar dashboards, tente novamente mais tarde.",
            "code": 500
        }), 500

@riscos_routes.route("/options", methods=['GET'])
@jwt_required()
def busca_opcoes():
    """
    Busca todas as opções necessárias para o cadastro de riscos
    ---
    responses:
      200:
        description: Opções encontradas com sucesso
        examples:
          application/json: {
              "options": {
                  "tipoRiscoOptions": [{"value": 1, "label": "OPERACIONAL"}, ...],
                  "areaIdentificacaoOptions": [{"value": 1, "label": "APO"}, ...],
                  ...
              },
              "code": 200
          }
    """
    try:
        result = riscos_dbc.busca_opcoes()
        return jsonify({
            "options": result,
            "code": 200
        }), 200
    except Exception as e:
        handle.error(f"Erro ao buscar opções: {e}")
        return jsonify({
            "mensagem": "Erro ao buscar opções, tente novamente mais tarde.",
            "code": 500
        }), 500

@riscos_routes.route("/salvar", methods=['POST'])
@jwt_required()
def salvar_risco():
    """
    Salva um novo risco no banco de dados
    ---
    parameters:
      - name: risco
        description: Descrição do risco
        type: string
        example: "Descrição detalhada do risco"
        required: true
      - name: tipoRisco
        description: Tipo de Risco
        type: integer
        example: 1
        required: true
      - name: areaIdentificacao
        description: Área Identificadora
        type: integer
        example: 1
        required: true
      - name: dataEntrada
        description: Data de Entrada do Risco
        type: string
        format: date
        example: "2023-06-24"
        required: true
      - name: consequencias
        description: Consequências do risco
        type: string
        example: "Possíveis consequências do risco"
        required: true
      - name: projeto
        description: Projeto relacionado ao risco
        type: string
        example: "Nome do projeto"
        required: true
      - name: metier
        description: Metier relacionado ao risco
        type: integer
        example: 1
        required: true
      - name: jalon
        description: Jalon relacionado ao risco
        type: integer
        example: 1
        required: true
      - name: probabilidade
        description: Probabilidade do risco
        type: integer
        example: 1
        required: false
      - name: impacto
        description: Impacto do risco
        type: integer
        example: 1
        required: false
      - name: estrategia
        description: Estratégia para mitigação do risco
        type: integer
        example: 1
        required: false
      - name: acao
        description: Ação a ser tomada
        type: string
        example: "Descrição da ação"
        required: false
      - name: nomePiloto
        description: Nome do piloto
        type: string
        example: "Nome do piloto"
        required: false
      - name: idPiloto
        description: ID do piloto
        type: string
        example: "ID do piloto"
        required: false
      - name: dataResposta
        description: Data de resposta
        type: string
        format: date
        example: "2023-06-25"
        required: false
      - name: dataAlerta
        description: Data de alerta
        type: string
        format: date
        example: "2023-06-26"
        required: false
      - name: comentarios
        description: Comentários adicionais
        type: string
        example: "Comentários adicionais"
        required: false
      - name: probResidual
        description: Probabilidade residual
        type: integer
        example: 1
        required: false
      - name: impacResidual
        description: Impacto residual
        type: integer
        example: 1
        required: false
      - name: acaoValidacao
        description: Ação de validação
        type: integer
        example: 1
        required: false
      - name: riscoValidacao
        description: Risco de validação
        type: integer
        example: 1
        required: false
      - name: dataResolucao
        description: Data de resolução
        type: string
        example: "2023-06-27"
        required: false
      - name: captalizacao
        description: Capitalização
        type: integer
        example: 1
        required: false
    responses:
      200:
        description: Risco salvo com sucesso
        examples:
          application/json: {
              "mensagem": "Risco salvo com sucesso",
              "code": 200
          }
      500:
        description: Erro ao salvar o risco
        examples:
          application/json: {
              "mensagem": "Erro ao salvar o risco, tente novamente mais tarde.",
              "code": 500
          }
    """
    received_parameters = {
        "risco": request.form.get("risco"),
        "tipoRisco": request.form.get("tipoRisco"),
        "areaIdentificacao": request.form.get("areaIdentificacao"),
        "dataEntrada": request.form.get("dataEntrada"),
        "consequencias": request.form.get("consequencias"),
        "projeto": request.form.get("projeto"),
        "metier": request.form.get("metier"),
        "jalon": request.form.get("jalon"),
        "probabilidade": request.form.get("probabilidade"),
        "impacto": request.form.get("impacto"),
        "estrategia": request.form.get("estrategia"),
        "acao": request.form.get("acao"),
        "nomePiloto": request.form.get("nomePiloto"),
        "idPiloto": request.form.get("idPiloto"),
        "dataResposta": request.form.get("dataResposta"),
        "dataAlerta": request.form.get("dataAlerta"),
        "comentarios": request.form.get("comentarios"),
        "probResidual": request.form.get("probResidual"),
        "impacResidual": request.form.get("impacResidual"),
        "acaoValidacao": request.form.get("acaoValidacao"),
        "riscoValidacao": request.form.get("riscoValidacao"),
        "dataResolucao": request.form.get("dataResolucao"),
        "captalizacao": request.form.get("captalizacao")
    }

    validation, parameters, code = paramatters.wizzard(salvar_risco.__doc__, received_parameters)
    if code == 400:
        return jsonify(validation), 400
    
    try:
        riscos_dbc.salvar_risco(parameters)
        return jsonify({
            "mensagem": "Risco salvo com sucesso",
            "code": 200
        }), 200
    except Exception as e:
        handle.error(f"Erro ao salvar o risco: {e}")
        return jsonify({
            "mensagem": "Erro ao salvar o risco, tente novamente mais tarde.",
            "code": 500
        }), 500
