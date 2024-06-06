from libs.database import mysql
from libs.tools import handle

def get_teste(**kwargs):
    """
    Retorne uma lista de documentos, de acordo com parametros

    Parametros
    ----------
    teste : string
        O tipo do documento (checklist, view...)
    
    Retornos
    --------
    array de dicionarios
    """

    teste = kwargs.get("teste")

    try:
        sql = ("SELECT %s")
        sql_parameters = (teste)
        response = mysql.get(sql, sql_parameters)
        response = response["data"]
    except Exception as error:
        handle.error(f"Falhou ao buscar a palavra: {error}")

    return response
