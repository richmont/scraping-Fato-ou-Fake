import requests
import json

#https://falkor-cda.bastian.globo.com/tenants/g1/instances/9a0574d8-bc61-4d35-9488-7733f754f881/posts/page/33

json_file = open("33.json","r")
dados = json.load(json_file)
for post in dados["items"]:
    print("Título: ", post["content"]["title"])


"""
como acessar o titulo do primeiro post coletado
dados["items"][0]["content"]["title"]
"""