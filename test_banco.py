from pymongo import MongoClient
from banco import inserir
from banco import alterar
from scraping import requisicao
import json
#url = 'http://httpbin.org/get'
#json_data = requisicao(url)

# f = open("33.json")
# json_data = json.load(f)

local = "mongodb://python:penis@localhost"
cliente = MongoClient(local)
banco = cliente.fato_ou_fake
colecao = banco.dados_brutos
# id_ins = inserir(colecao, json_data)
# print("id da inserção:", id_ins)
