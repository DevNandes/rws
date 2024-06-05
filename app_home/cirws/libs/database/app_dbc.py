from libs.database import mysql
from libs.tools import handle

def get_documents(**kwargs):
    """
    Retorne uma lista de documentos, de acordo com parametros

    Parametros
    ----------
    document_type : string
        O tipo do documento (checklist, view...)
    
    Retornos
    --------
    array de dicionarios
    """

    document_type = kwargs.get("document_type")

    try:
        sql = ("CALL outputs_sp.get_documents(%s)")
        sql_parameters = (document_type)
        response = mysql.get(sql, sql_parameters)
        response = response["data"]
    except Exception as error:
        handle.error(f"Falhou ao listar os documentos: {error}")

    return response
