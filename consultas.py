from pymongo import MongoClient
from pprint import pprint
local = "mongodb://python:penis@localhost"
cliente = MongoClient(local)
banco = cliente.fato_ou_fake
posts = banco.posts


def consulta_campo_regex(colecao, campo, palavra):
    """
    colecao (MongoDB Collection) \n
    campo (str) \n
    palavra (str) \n
    Consulta no banco filtrando pelo campo e seu conteúdo por regex
    """
    query = {campo: {'$regex': palavra}}
    resultado = colecao.find(query)
    return resultado


def consulta_posts_data(colecao=posts, ano=None, mes=None, dia=None):
    """
    colecao (MongoDB Collection)\n
    ano (int{4}) \n
    mes (int{2}) \n
    dia (int{2}) \n
    
    Consulta no banco filtrando pela data do post
    """

    """
    Caso um dos valores de data seja None
    Associa esse valor com a regex para funcionar com um range de números
    """
    if ano is None:
        ano = "\d{4}"
    elif mes is None:
        mes = "\d{2}"
    elif dia is None:
        dia = '\d{2}'

    data = ano + "." + mes + "." + dia
    print("data recebida: ", data)
    query = {'data_publicacao': {'$regex': data}}
    resultado = colecao.find(query)
    return resultado

"""
resultado = consulta_posts_data(colecao=posts, ano='2020', dia='28')
for x in resultado:
    pprint(x)
"""