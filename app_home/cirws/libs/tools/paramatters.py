import re

def has_malicious_code(string):
    if (re.search(r"\b(delete|update|insert|into|drop|select|database|where|table|truncate)\b", string, re.IGNORECASE)):
        return True
    else:
        return False

def wizzard(function_documentation, received_parameters):
    """
    Receba o arquivo de documentacao de uma rota, e verifique
    se os parametros recebidos sao validos (de acordo com a documentacao)

    Parametros
    ----------
    function_documentation : docstring, obrigatorio
        A documentacao da rota (obtida da seguinte maneira nome_da_funcao.__doc__)
    received_parameters : dictionary, obrigatorio
        Dicionario contendo os parametros recebidos na rota

    Retornos
    --------
    json
        Objeto json, contendo o resultado da verificacao
        No caso de erro:
        "error": {
            "message": msg_arr
        }
    
    dict
        Dicionario, contendo os parametros ja corrigidos, prontos para uso
    
    integer
        inteiro, contendo o codigo de saida do script (400 para falha ou 200 para sucesso)
    """

    new_parameters = {}
    # vamos montar um array de dicionarios com a seguinte estrutura
    # [0] = {name: xxxx, type: xxxx, required: xxxx}
    def get_array_of_dictionaries_from_array(my_array):
        element_dict = {}
        doc_elements = []
        for element in my_array:
            # vamos primeiro "limpar" a string, deixando-a sem espacos em branco ou new lines
            element = element.replace("\n", " ")
            element = element.replace(" ", "")

            # split para obter key e value
            element_split = element.split(":")
            element_key = element_split[0]
            element_value = element_split[-1]

            # caso inicie com o caracter "-" significa que temos o nome do parametro
            # neste caso, vamos gravar no nosso array, ate que ele encontre um novo "-"
            if (element_value == ""):
                element_dict["name"] = element_key
            elif (element_key.startswith("-")):
                element_dict["name"] = element_value
            elif (element_key.startswith("description")):
                element_dict["description"] = element_value.lower()
            elif (element_key.startswith("in")):
                element_dict["in"] = element_value.lower()
            elif (element_key.startswith("name")):
                element_dict["name"] = element_value.lower()
            elif (element_key.startswith("type")):
                element_dict["type"] = element_value
            elif (element_key.startswith("example")):
                element_dict["example"] = element_value.lower()
            elif (element_key.startswith("default")):
                element_dict["default"] = element_value.lower()
                # realize o append do dicionario ao array, logo que ja possuimos todos os dados
            elif (element_key.startswith("required")):
                element_dict["required"] = element_value.lower()
                doc_elements.append(element_dict.copy())
                element_dict.clear()

        # retorne o array de dicionarios ja organizado
        return doc_elements

    # trate o doc recebido, muita cautela, pois estamos falando sobre dados inseridos pelo programador
    #que por sua vez, pode ter esquecido de inserir alguma informacao importante
    try:
        parameters_regex = re.findall('parameters:(.+?)responses:', function_documentation, re.DOTALL)
    except:
        parameters_regex = [404]

    try:
        properties_regex = re.findall('properties:(.+?)responses:', function_documentation, re.DOTALL)
    except:
        properties_regex = [404]

    # crie um array baseado nas new lines, novamente com muita cautela
    try:
        parameters_array = parameters_regex[0].split("\n")
        # se regex match, entao significa que estamos tratando de um post, vamos esvaziar esse array
        if (re.findall('- in:', parameters_array[1], re.DOTALL)):
            parameters_array = [404]
    except:
        parameters_array = [404]
    
    try:
        properties_array = properties_regex[0].split("\n")
    except:
        properties_array = [404]

    # remova elementos vazios
    if (properties_array[0] != 404):
        properties_array = [i for i in properties_array if i]
        # organize os parametros em um array de dicionarios
        doc_parameters = get_array_of_dictionaries_from_array(properties_array)

    if (parameters_array[0] != 404):
        parameters_array = [i for i in parameters_array if i]
        # organize os parametros em um array de dicionarios
        doc_parameters = get_array_of_dictionaries_from_array(parameters_array)

    # com o array de dicionario em maos, valide os inputs (received_parameters) 
    #com os dados extraidos da documentacao (doc_parameters)
    msg_arr = []
    not_required_parameters = 0

    if (len(doc_parameters) < 1):
        item1 = "A documentacao esta incorreta, consulte o README.md para mais detalhes"
        item2 = "foram enviados parametros que por sua vez nao foram documentados na docstring"
        new_msg = f"Existem alguns erros na documentacao do software, verifique os seguintes itens: {item1}, ou {item2}"
        msg_arr.append(new_msg)

    for parameter in doc_parameters:
        parameter_name = parameter["name"]
        parameter_type = parameter["type"]
        parameter_required = parameter["required"]
        if "default" in parameter:
            parameter_default = parameter["default"]
        #else:
        #    # dont process empty values
        #    if (not (received_parameters[parameter_name])):
        #        continue

        # Helper function to check for default values
        def get_default():
            default_value = ""
            if "default" in parameter:
                default_value = parameter_default
            return default_value
        
        # verifique se o tipo eh valido
        if (not re.search('^(integer|string|float|file|id|ids|array)$', parameter_type)):
            new_msg = f"O parametro {parameter_name} recebeu um tipo de valor invalido: {parameter_type}"
            msg_arr.append(new_msg)
        
        # verifique se o campo required eh valido
        if (not re.search('^(true|false|mixed)$', parameter_required)):
            new_msg = f"O parametro {parameter_name} recebeu um tipo de valor invalido: {parameter_required}"
            msg_arr.append(new_msg)
        
        if (parameter_required == "false"):
            not_required_parameters += 1

        # cruze os dados com os parametros recebidos na funcao
        # a primeira verificacao, sera no valor, se ele existe ou nao
        received_value = received_parameters[parameter_name]
        if (not (received_value) and (parameter_required == "true")):
            new_msg = f"O parametro {parameter_name} nao foi informado, sendo este um parametro obrigatorio"
            msg_arr.append(new_msg)
        
        # verifique se eh possivel realizar o cast do tipo recebido
        if (received_value):
            if (received_value == "undefined"):
                if "default" in parameter:
                    new_parameters[parameter_name] = parameter_default
                else:   
                    new_parameters[parameter_name] = ""
                continue
            if (parameter_type == "integer"):
                try:
                    received_value = int(received_value)
                    new_parameters[parameter_name] = received_value
                except:
                    new_msg = f"O parametro {parameter_name} deve ser do tipo {parameter_type}, porem o seguinte valor foi informado: {received_value}"
                    msg_arr.append(new_msg)
            elif (parameter_type == "float"):
                try:
                    received_value = float(received_value)
                    new_parameters[parameter_name] = received_value
                except:
                    new_msg = f"O parametro {parameter_name} deve ser do tipo {parameter_type}, porem o seguinte valor foi informado: {received_value}"
                    msg_arr.append(new_msg)
            elif (parameter_type == "string"):
                try: 
                    received_value = str(received_value)
                    # Remove whitespaces from begining and end of the string
                    received_value = received_value.strip()

                    # Check for empty values
                    if (received_value == "null"):
                        default_value = ""
                        if "default" in parameter:
                            default_value = parameter_default
                        received_value = default_value
                        #received_value = get_default()

                    # Check for malicious code
                    elif (has_malicious_code(received_value)):
                        new_msg = f"O parametro {parameter_name} recebeu um valor considerado malicioso: {received_value}"
                        msg_arr.append(new_msg)
                    new_parameters[parameter_name] = received_value
                except:
                    new_msg = f"O parametro {parameter_name} deve ser do tipo {parameter_type}, porem o seguinte valor foi informado: {received_value}"
                    msg_arr.append(new_msg)
            elif (parameter_type == "array"):
                if isinstance(received_value, list):
                    new_parameters[parameter_name] = received_value
                else:
                    new_msg = f"O parametro {parameter_name} deve ser do tipo {parameter_type}, porem o seguinte valor foi informado: {received_value}"
                    msg_arr.append(new_msg)
        else:
            #new_parameters[parameter_name] = get_default()
            default_value = ""
            if "default" in parameter:
                default_value = parameter_default
            new_parameters[parameter_name] = default_value

        # verifique se o numero de parametros enviados assemelha-se ao numero de parametros da documentacao
        if (len(doc_parameters) < (len(received_parameters) - not_required_parameters)):
            new_msg = f"O numero de parametros enviados difere do numero de parametros cadastrados: cadastrados: {len(doc_parameters)} recebidos: {len(received_parameters)}"
            msg_arr.append(new_msg)

    # caso exista algum elemento dentro do array, significa que existe algo de errado
    if (msg_arr):
        return {
            "error": {
                "message": msg_arr,
                "status": 400
            }
        }, new_parameters, 400
    else:
        return "", new_parameters, 200
