import requests
import json


def requisicao(url, **pagina):
    num_pagina = pagina.get("pagina")
    if num_pagina is not None:
        """
        omitindo a verificação do elemento items,
        para funciona com qualquer requisição
        """
        url = url + str(pagina)
        resposta = requests.get(url)
        json_data = json.loads(resposta.text)
        # tamanho_resposta = len(json_data["items"])
        # if tamanho_resposta <= 0:
        #    return None
        # else:
        return json_data
    else:
        # retornar o json do url apenas
        resposta = requests.get(url)
        json_data = json.loads(resposta.text)
        # tamanho_resposta = len(json_data["items"])
        # if tamanho_resposta <= 0:
        # return None
        # else:
        return json_data


# https://falkor-cda.bastian.globo.com/tenants/g1/instances/9a0574d8-bc61-4d35-9488-7733f754f881/posts/page/33
"""
json_file = open("33.json","r")
dados = json.load(json_file)
for post in dados["items"]:
    print("Título: ", post["content"]["title"])

como acessar o titulo do primeiro post coletado
dados["items"][0]["content"]["title"]
"""
