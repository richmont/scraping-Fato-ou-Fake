from pymongo import MongoClient
from banco import inserir
from banco import alterar
from scraping import requisicao
import json
local = "mongodb://python:penis@localhost"
cliente = MongoClient(local)
banco = cliente.fato_ou_fake
colecao = banco.dados_brutos
# id_ins = inserir(colecao, json_data)
# print("id da inserção:", id_ins)
url = "https://falkor-cda.bastian.globo.com/tenants/g1/instances/9a0574d8-bc61-4d35-9488-7733f754f881/posts/page/"
for x in range(1, 60):
    print("iniciando requisição na linha ", x)
    json_data = requisicao(url, pagina=x)
    if json_data is not None:
        tamanho_resposta = len(json_data["items"])
        if tamanho_resposta > 0:
            id_recebido = inserir(colecao, json_data)
            if id_recebido is None:
                print("erro ao inserir dados da página ", x)
            else:
                print("inserido com sucesso, id: ", id_recebido, " a partir da página ", x)
        else:
            print("Resposta do servidor sem conteúdo na página ", x)
            break
    else:
        print("requisição vazia recebida na linha ", x)
        break
