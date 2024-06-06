from libs.tools import handle

def get_only_values_from_dictionary(**kwargs):
  """
  Retorna somente os values de determinado dicionario
  O dicionario deve possuir somente uma key, e diversos valores

  Parametros
  ----------
  dictionary : dict, obrigatorio
    O dicionario contendo os values a serem extraidos
  the_key : string, obrigatorio
    A chave da qual os values serao retirados
  
  Retornos
  --------
  Uma lista contendo todos os values extraidos do dicionario
  """

  dictionary = kwargs.get("dictionary")
  the_key = kwargs.get("the_key")

  try:
    result = [dictionary[the_key] for dictionary in dictionary]
  except Exception as error:
    handle.error(f"Falhou ao retornar somente os valores do dicionario, motivo: {error}")

  return result

