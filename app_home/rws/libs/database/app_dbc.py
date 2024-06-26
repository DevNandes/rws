from libs.database import mysql
from libs.tools import handle

def get_senha(**kwargs):
    """
    Retorne a senha criptografada do usuario para login

    Parametros
    ----------
    email : string
        O email do usuario ultilizado para logar

    Retornos
    --------
    senhaUsuario
    """

    email = kwargs.get("email")

    try:
        sql = ("""SELECT 
        senhaUsuario, temaUsuario, nomeUsuario, idUsuario, linguagemUsuario, CadUsuarios.idPerfil, CadPerfil.nomePerfil
        FROM RenaultRisk.CadUsuarios 
        INNER JOIN RenaultRisk.CadPerfil
            ON CadPerfil.idPerfil = CadUsuarios.idPerfil
        WHERE emailUsuario = %s 
        LIMIT 1""")
        sql_parameters = (email)
        response = mysql.get(sql, sql_parameters)
        response = response["data"]
    except Exception as error:
        handle.error(f"Falhou ao buscar a senha: {error}")

    return response


def cadastrar_usuario(nome, email, senha):
    """
    Cadastra um novo usuario no banco de dados

    Parametros
    ----------
    username : string
        Nome do usuario
    email : string
        Email do usuario
    senha : string
        Senha criptografada do usuario
    """

    try:
        sql = ("INSERT INTO `RenaultRisk`.`CadUsuarios` "
               "(`nomeUsuario`, `emailUsuario`, `idPerfil`, `senhaUsuario`, `situacaoUsuario`) "
               "VALUES (%s, %s, %s, %s, %s)")
        sql_parameters = (nome, email, 2, senha, 'A')
        mysql.insert(sql, sql_parameters)
    except Exception as error:
        handle.error(f"Falhou ao cadastrar o usuario: {error}")
        raise


def busca_menus_usuario(idUsuario):
    """
    Busca menus que usuario tem acesso

    Parametros
    ----------
    idUsuario : string
        Id do Usuario
    """

    try:
        sql = ("""SELECT 
                    CadMenu.*
                FROM RenaultRisk.CadMenu
                INNER JOIN RenaultRisk.CadUsuarios
                    ON CadUsuarios.idUsuario = %s
                INNER JOIN RenaultRisk.MenuPerfil
                    ON CadUsuarios.idPerfil = MenuPerfil.idPerfil
                    AND MenuPerfil.idMenu = CadMenu.idMenu""")
        sql_parameters = (idUsuario)
        response = mysql.get(sql, sql_parameters)
        return response["data"]
    except Exception as error:
        handle.error(f"Falhou ao buscar os menus: {error}")
        raise
