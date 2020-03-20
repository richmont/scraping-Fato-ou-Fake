from pymongo import MongoClient
from pprint import pprint
import math
local = "mongodb://python:penis@localhost"
cliente = MongoClient(local)
banco = cliente.fato_ou_fake
posts = banco.posts


def tamanho_numero(numero):
    if numero is 0:
        return None
    elif isinstance(numero, int):
        digits = int(math.log10(numero))+1
        return digits
    else:
        return None


def consulta_campo_regex(colecao, consulta, limite=10):
    """
    colecao (MongoDB Collection) \n
    campo (str) \n
    consulta (set) \n
    Consulta no banco filtrando pelo campo e seu conteúdo por regex
    """
    for chave in consulta.keys():
        query = {chave: {'$regex': consulta[chave]}}
        resultado = colecao.find(query).limit(limite)
        return resultado


def consulta_posts_data(colecao=posts, ano=None, mes=None, dia=None, limite=10, pular=None):
    """
    colecao (MongoDB Collection)\n
    ano (int{4}) \n
    mes (int{2}) \n
    dia (int{2}) \n
    limite (int)
    
    Consulta no banco filtrando pela data do post
    """
    """
    verificação rápida se qualquer um dos valores é nulo
    """

        
    """
    Caso um dos valores de data seja None
    Associa esse valor com a regex para funcionar com um range de números
    """
    if dia is None:
        dia = "\d{2}"
    else:
        int_dia = dia
        if tamanho_numero(int_dia) is 1:
            # acrescenta 0 na frente de número de um dígito
            dia = "0" + str(dia)
            # dia ok com 2 digitos
        elif tamanho_numero(int_dia) is 2:
            # número no tamanho correto, dois dígitos
            # checa se o valor do dia está no alcance de dias normais
            if int_dia < 1 or int_dia > 31:
                # retorna None e termina
                print("valor do dia inválido: ", dia)
                return None
        else:
            print("valor do dia inválido: ", dia)
            return None
    if mes is None:
        mes = "\d{2}"
    else:
        int_mes = mes
        if tamanho_numero(int_mes) is 1:
            # acrescenta 0 na frente de número de um dígito
            mes = "0" + str(mes)
            # mes ok com 2 digitos
        elif tamanho_numero(int_mes) is 2:
            # número no tamanho correto, dois dígitos
            # checa se o valor do mes está no alcance de mess normais
            if int_mes < 1 or int_mes > 12:
                # retorna None e termina
                print("valor do mes inválido: ", mes)
                return None
        else:
            print("valor do mes inválido: ", mes)
            return None

    if ano is None:
        ano = "\d{4}"
    else:
        int_ano = ano
        if tamanho_numero(int_ano) is 2:
            ano = "20" + str(ano)
            # ano ok com 4 digitos
        elif tamanho_numero(int_ano) is 4:
            # número no tamanho correto, dois dígitos
            # checa se o valor do ano está no alcance de anos normais
            if int_ano < 1900 or int_ano > 3000:
                print("valor do ano inválido: ", ano)
                return None
        else:
            print("valor do ano inválido: ", ano)
            return None

    data = str(ano) + "." + str(mes) + "." + str(dia)
    # se pular é nulo ou não é um inteiro
    if pular is None or isinstance(pular, int) is not True:
        query = {'data_publicacao': {'$regex': data}}
        resultado = colecao.find(query).limit(limite)
        return resultado
    else:
        # consulta definindo o skip com var pular
        query = {'data_publicacao': {'$regex': data}}
        resultado = colecao.find(query).skip(pular).limit(limite)
        return resultado


def consulta_post_id(colecao, id):
    # recebe o documento compatível com o ID informado
    resultado = colecao.find_one({"_id": id})
    return resultado


def quantidade_total(colecao, consulta=None):
    if consulta is None:
        # consulta vazia para retornar todos os documentos da coleção
        resultado = colecao.count_documents({})
        return resultado
    else:
        # consulta obedecendo a query recebida
        resultado = colecao.count_documents(consulta)
        return resultado

"""
consulta = {"titulo": "#FAKE"}
resultado = consulta_campo_regex(posts, consulta)
for x in resultado:
    print(x)

resultado = consulta_posts_data(colecao=posts, ano=2020)
for x in resultado:
    pprint(x)
"""
