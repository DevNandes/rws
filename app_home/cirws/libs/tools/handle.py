"""
Modulo responsavel por lidar com os erros e warns gerados durante a execucao do programa

Todos os handles sao armazenados em um arquivo de logs
"""

from flask import abort, make_response
from datetime import datetime
from os import environ

def error(error_message, code = 500):
    """
    Aborte a execucao do codigo e retorna um erro no formato
    JSON para o usuario

    Registre um log do tipo ERRO

    Parametros
    ----------
    error_message : str, obrigatorio
        A mensagem de erro
    code : int
        O codigo de erro (500, 404 ....)
    """ 

    error_message = str(error_message)

    message = {
        "code": code,
        "message": {
            "error": error_message
        }
    }
    log_message = format_message("ERRO", error_message)
    write_to_log(log_message)
    abort(make_response(message, code))


def warn(message):
    """
    Registre um log do tipo WARN

    Parametros
    ----------
    message : str, obrigatorio
        A mensagem de erro a ser registrada no log
    """

    message = str(message)

    message = format_message("WARN", message)
    write_to_log(message)


def info(message):
    """
    Registre um log do tipo INFO

    Parametros
    ----------
    message : str, obrigatorio
        A mensagem de erro a ser registrada no log
    """

    message = str(message)

    message = format_message("INFO", message)
    write_to_log(message)


def format_message(message_type, message):
    """
    Retorne a mensagem formatada no padrao do log

    Parametros
    ----------
    message_type : str, obrigatorio
        O tipo de mensagem a ser registrado no log
    message : str, obrigatorio
        A mensagem a ser registrada no log

    Retornos
    --------
    string
        A mensagem formatada no padrao do log
    """

    current_date = get_current_date()
    log_message = message_type + "|" + current_date + "|" + message
    return log_message


def get_current_date():
    """
    Retorne a data atual, no formato dd/mm/aaaa hh:mm:ss

    Retornos
    --------
    string
        A data atual no padrao do log
    """

    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y %H:%M:%S")
    return current_date


def write_to_log(message):
    """
    Registre a mensagem no arquivo de logs

    Parametros
    ----------
    message : str, obrigatorio
        A mensagem a ser registrada no log
    """    
    try:
        log_path = f"{environ['LOGS_DIR']}/app.log"
        log_file = open(log_path, 'a')
        log_file.write(message + "\n")
        log_file.flush()
        log_file.close()
    except Exception as error:
        err_message = {
            "code": 500,
            "message": {
                "error": f"Falhou ao abrir o arquivo de logs para escrita, motivo: {error}"
            }
        }
        abort(make_response(err_message, 500))
