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
            print("Documento já existe no banco")
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
