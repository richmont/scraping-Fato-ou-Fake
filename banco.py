from pymongo import MongoClient
import json
import requests
url = "https://falkor-cda.bastian.globo.com/tenants/g1/instances/9a0574d8-bc61-4d35-9488-7733f754f881/posts/page/"


def requisicao(url, pagina):
    url = url + str(pagina)
    resposta = requests.get(url)
    json_data = json.loads(resposta.text)
    tamanho_resposta = len(json_data["items"])
    if tamanho_resposta <= 0:
        return None
    else:
        return json_data


def inserir(colecao, id, conteudo):
    """
    Parâmetros:
    colecao (MongoDB Collection)
    id (int)
    conteudo (set)

    retorna o id do documento inserido
    """
    resposta = colecao.find_one({"_id": id})
    if resposta is None:
        # elemento com id informado não existe no banco, inserir
        # retorna o id inserido
        campo = {}
        id_campo = {"_id": id}
        campo.update(id_campo)
        campo.update(conteudo)
        inserir = campo
        resultado = colecao.insert_one(inserir)
        return resultado.inserted_id
    else:
        # elemento com id já existe no banco, retorna None
        return None


def alterar(colecao, busca, alterado):
    """
    Parãmetros:
    colecao (MongoDB Collection)
    busca (json)
    alterado (json)

    Altera um documento já existente no banco
    localiza o campo correto pelo parâmetro de busca

    retorna o conteúdo do campo alterado
    """
    resposta = colecao.find_one(busca)
    if resposta is None:
        # elemento não encontrado, não alterar nada e retornar none
        return None
    else:
        mudanca = {"$set": alterado}
        resultado = colecao.update_one(busca, mudanca)
        return resultado


"""
dados = requisicao(url, 60)
if dados is not None:
    print("dados válidos 60")
dados = requisicao(url, 59)
if dados is not None:
    print("dados válidos 59")

"""
#controle = {"_id": 1, "pagina_mais_antiga": 60}
local = "mongodb://python:penis@localhost"
cliente = MongoClient(local)
banco = cliente.fato_ou_fake
colecao = banco.dados_brutos
# resultado = inserir(colecao, 1, {"ultima_pagina_verificada": 60})
resultado = inserir(colecao, 12, {"pintos": 1212, "kkkk": True})
if resultado is None:
    print("erro")
else:
    print(resultado)
    
"""
busca = {"_id": 1}
alterado = {"pagina_mais_antiga": 59}
resultado = alterar(colecao, busca, alterado)
if resultado is None:
    print("Erro")
else:
    print("Alterado com sucesso")
"""
# inserir(colecao, 22, "fodase")
# id_insert = colecao.insert_one(controle).inserted_id

