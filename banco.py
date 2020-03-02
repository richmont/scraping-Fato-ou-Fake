from pymongo import MongoClient


def inserir(colecao, conteudo, **kwargs):
    """
    Parâmetros:
    colecao (MongoDB Collection)
    conteudo (json)
    id (str)
    Em caso de ausência do id, programa continua e
    deixa que o MongoDB gerencie o registro chave

    retorna o id do documento inserido
    """

    # se recebemos um id
    id = kwargs.get("id")
    if id is not None:
        # verifique se este id já existe no banco
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
    else:
        # se não recebemos uma id o Mongo cria automaticamente
        resultado = colecao.insert_one(conteudo)
        return resultado.inserted_id


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


def lista_chave_banco(colecao, chave, chave_interna):
    """
    colecao (MongoDB Collection)
    chave (str)
    chave_interna (str)

    Busca no banco o conteúdo de uma chave dentro de outra
    Por enquanto é o bastante pra colher metadados
    """
    # filtra apenas os documentos que contém o campo "items"
    bruto = colecao.distinct(chave)
    conteudo = []
    for x in bruto:
        # agora pega o conteúdo e passa pra uma lista
        conteudo.append(x[chave_interna])
    return conteudo


local = "mongodb://python:penis@localhost"
cliente = MongoClient(local)
banco = cliente.fato_ou_fake
col_dados_brutos = banco.dados_brutos
col_posts = banco.posts


def bruto_json(col_dados_brutos):
    json_post = {}
    conteudo_bruto1 = lista_chave_banco(col_dados_brutos, "items", "id")
    conteudo_bruto2 = lista_chave_banco(col_dados_brutos, "items", "publication")
    conteudo_bruto3 = lista_chave_banco(col_dados_brutos, "items", "content")
    for x in conteudo_bruto1:
        id = x
        # json_id = {"id": x}
        # json_post.update(json_id)
        for y in conteudo_bruto2:
            json_publication = {"publication": y}
            json_post.update(json_publication)
            for z in conteudo_bruto3:
                json_title = {"title": z["summary"]}
                json_summary = {"summary": z["summary"]}
                json_title = {"url": z["url"]}
                json_post.update(json_title)
                json_post.update(json_summary)
                json_post.update(json_title)
                break
            break
        inserir(col_posts, json_post, id=id)
        break


bruto_json(col_dados_brutos)


"""
# pegar os ids dos posts
conteudo = lista_chave_banco(colecao, "items", "id")
for x in conteudo:
    print(x)

conteudo = lista_chave_banco(colecao, "items", "content")
for x in conteudo:
    # print(x["title"])
    print("tamanho: ", len(x["title"]) )        




dados = requisicao(url, 60)
if dados is not None:
    print("dados válidos 60")
dados = requisicao(url, 59)
if dados is not None:
    print("dados válidos 59")


# controle = {"_id": 1, "pagina_mais_antiga": 60}



busca = {"_id": 1}
alterado = {"pagina_mais_antiga": 59}
resultado = alterar(colecao, busca, alterado)
if resultado is None:
    print("Erro")
else:
    print("Alterado com sucesso")
"""
