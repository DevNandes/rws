from libs.database import mysql
from libs.tools import handle

def busca_dashboards_status():
    """
    Busca dados que que gera os 4 dashboards superiores sobre os status
    """

    try:
        sql = ("""SELECT 
    (SELECT COUNT(idRisk) FROM RenaultRisk.RiskMonitoring) AS totalRiscos,
    (SELECT COUNT(idRisk) FROM RenaultRisk.RiskMonitoring WHERE idStatus = 3) AS riscosResolvidos,
    (SELECT COUNT(idRisk) FROM RenaultRisk.RiskMonitoring WHERE idStatus = 2) AS riscosTrajetoria,
    (SELECT COUNT(idRisk) FROM RenaultRisk.RiskMonitoring WHERE idStatus = 4) AS riscosProblema;""")
        sql_parameters = ()
        response = mysql.get(sql, sql_parameters)
        return response["data"]
    except Exception as error:
        handle.error(f"Falhou ao buscar os dashboards: {error}")
        raise


def busca_opcoes():
    """
    Busca todas as opções necessárias para o cadastro de riscos
    """
    try:
        queries = {
            "tipoRiscoOptions": "SELECT idTipoRisco as value, nomeTipoRisco as label FROM RenaultRisk.CadTipoRisco",
            "areaIdentificacaoOptions": "SELECT idArea as value, nomeArea as label FROM RenaultRisk.CadArea",
            "metierOptions": "SELECT idMetier as value, nomeMetier as label FROM RenaultRisk.CadMetier",
            "jalonOptions": "SELECT idJalon as value, nomeJalon as label FROM RenaultRisk.CadJalon",
            "probabilidadeOptions": "SELECT idProbabilit as value, nomeProbabilit as label FROM RenaultRisk.CadProbabilit",
            "impactoOptions": "SELECT idImpact as value, nomeImpact as label FROM RenaultRisk.CadImpact",
            "estrategiaOptions": "SELECT idStrategy as value, nomeStrategy as label FROM RenaultRisk.CadStrategy",
            "probResidualOptions": "SELECT idResidualProb as value, nomeResidualProb as label FROM RenaultRisk.CadResidualProb",
            "impacResidualOptions": "SELECT idResidualImp as value, nomeResidualImp as label FROM RenaultRisk.CadResidualImp",
            "acaoValidacaoOptions": "SELECT idAction as value, nomeAction as label FROM RenaultRisk.CadAction",
            "riscoValidacaoOptions": "SELECT idRiskValidation as value, nomeRiskValidation as label FROM RenaultRisk.CadRiskValidation",
            "captalizacaoOptions": "SELECT idCapitalization as value, nomeCapitalization as label FROM RenaultRisk.CadCapitalization"
        }

        result = {}
        for key, query in queries.items():
            response = mysql.get(query, ())
            result[key] = response["data"]

        return result
    except Exception as error:
        handle.error(f"Falhou ao buscar opções: {error}")
        raise


def salvar_risco(data):
    """
    Salva um novo risco no banco de dados
    """
    try:
        # Lista de todos os campos possíveis
        campos = {
            'risco': None,
            'tipoRisco': None,
            'areaIdentificacao': None,
            'dataEntrada': None,
            'consequencias': None,
            'projeto': None,
            'metier': None,
            'jalon': None,
            'probabilidade': None,
            'impacto': None,
            'estrategia': None,
            'acao': None,
            'nomePiloto': None,
            'idPiloto': None,
            'dataResposta': None,
            'dataAlerta': None,
            'probResidual': None,
            'impacResidual': None,
            'acaoValidacao': None,
            'riscoValidacao': None,
            'dataResolucao': None,
            'captalizacao': None
        }

        # Atualiza o dicionário campos com os valores recebidos em data, substituindo strings vazias por None
        campos.update({key: (data[key] if data[key] != "" else None) for key in data if key in campos})

        sql = ("""
            INSERT INTO RenaultRisk.RiskMonitoring (
                risk, idTipoRisco, idArea, riskEntryDate, consequences, project, idMetier, 
                idJalon, idProbabilit, idImpact, idStrategy, action, pilotName, pilotId, 
                initialDate, alertDate, idResidualProb, idResidualImp, 
                idAction, idRiskValidation, resolutionDate, idCapitalization
            ) VALUES (
                %(risco)s, %(tipoRisco)s, %(areaIdentificacao)s, %(dataEntrada)s, 
                %(consequencias)s, %(projeto)s, %(metier)s, %(jalon)s, %(probabilidade)s, 
                %(impacto)s, %(estrategia)s, %(acao)s, %(nomePiloto)s, %(idPiloto)s, 
                %(dataResposta)s, %(dataAlerta)s, %(probResidual)s, 
                %(impacResidual)s, %(acaoValidacao)s, %(riscoValidacao)s, %(dataResolucao)s, 
                %(captalizacao)s
            )
        """)

        sql_parameters = {
            'risco': campos['risco'],
            'tipoRisco': campos['tipoRisco'],
            'areaIdentificacao': campos['areaIdentificacao'],
            'dataEntrada': campos['dataEntrada'],
            'consequencias': campos['consequencias'],
            'projeto': campos['projeto'],
            'metier': campos['metier'],
            'jalon': campos['jalon'],
            'probabilidade': campos['probabilidade'],
            'impacto': campos['impacto'],
            'estrategia': campos['estrategia'],
            'acao': campos['acao'],
            'nomePiloto': campos['nomePiloto'],
            'idPiloto': campos['idPiloto'],
            'dataResposta': campos['dataResposta'],
            'dataAlerta': campos['dataAlerta'],
            'probResidual': campos['probResidual'],
            'impacResidual': campos['impacResidual'],
            'acaoValidacao': campos['acaoValidacao'],
            'riscoValidacao': campos['riscoValidacao'],
            'dataResolucao': campos['dataResolucao'],
            'captalizacao': campos['captalizacao']
        }

        mysql.insert(sql, sql_parameters)
    except Exception as error:
        handle.error(f"Falhou ao salvar o risco: {error}")
        raise

def busca_risk_monitoring():
    """
    Busca dados dos riscos salvos
    """

    try:
        sql = ("""SELECT 
        idRisk,
        risk,
        CadTipoRisco.nomeTipoRisco,
        CadArea.nomeArea,
        riskEntryDate,
        consequences,
        project,
        CadMetier.nomeMetier,
        CadJalon.nomeJalon,
        CadProbabilit.nomeProbabilit,
        CadImpact.nomeImpact,
        CadStrategy.nomeStrategy,
        action,
        pilotName,
        pilotId,
        initialDate,
        alertDate,
        CadResidualProb.nomeResidualProb,
        CadResidualImp.nomeResidualImp,
        CadAction.nomeAction,
        resolutionDate,
        CadRiskValidation.nomeRiskValidation,
        idCapitalization
    FROM RenaultRisk.RiskMonitoring
    INNER JOIN RenaultRisk.CadTipoRisco
        ON RiskMonitoring.idTipoRisco = CadTipoRisco.idTipoRisco
    INNER JOIN RenaultRisk.CadArea
        ON RiskMonitoring.idArea = CadArea.idArea
    INNER JOIN RenaultRisk.CadMetier
        ON RiskMonitoring.idMetier = CadMetier.idMetier
    INNER JOIN RenaultRisk.CadJalon
        ON RiskMonitoring.idJalon = CadJalon.idJalon
    INNER JOIN RenaultRisk.CadProbabilit
        ON RiskMonitoring.idProbabilit = CadProbabilit.idProbabilit
    INNER JOIN RenaultRisk.CadImpact
        ON RiskMonitoring.idImpact = CadImpact.idImpact
    INNER JOIN RenaultRisk.CadStrategy
        ON RiskMonitoring.idStrategy = CadStrategy.idStrategy
    INNER JOIN RenaultRisk.CadResidualProb
        ON RiskMonitoring.idResidualProb = CadResidualProb.idResidualProb
    INNER JOIN RenaultRisk.CadResidualImp
        ON RiskMonitoring.idResidualImp = CadResidualImp.idResidualImp
    INNER JOIN RenaultRisk.CadAction
        ON RiskMonitoring.idAction = CadAction.idAction
    INNER JOIN RenaultRisk.CadRiskValidation
        ON RiskMonitoring.idRiskValidation = CadRiskValidation.idRiskValidation;""")
        sql_parameters = ()
        response = mysql.get(sql, sql_parameters)
        return response["data"]
    except Exception as error:
        handle.error(f"Falhou ao buscar os riscos: {error}")
        raise