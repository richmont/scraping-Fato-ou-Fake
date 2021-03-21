import sqlite3
import math
from sqlite3 import Error
# conectando...
# Adicionar parametro do nome do banco a partir do dotenv
conn = sqlite3.connect('posts.db')
# definindo um cursor
cursor = conn.cursor()


def tamanho_numero(numero):
    if numero == 0:
        return None
    elif isinstance(numero, int):
        digits = int(math.log10(numero))+1
        return digits
    else:
        return None

def criar_tabela(cursor):
    # criando a tabela (schema)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts (
            _id TEXT NOT NULL PRIMARY KEY,
            titulo TEXT NOT NULL,
            data_publicacao DATETIME NOT NULL,
            resumo     TEXT NOT NULL,
            post_url TEXT NOT NULL
    );
    """)
    print('Tabela criada com sucesso.')
    # desconectando...
    conn.close()

def inserir(cursor, conteudo, **kwargs):
    """
    Parâmetros:
    cursor (Cursor do SQLite)
    conteudo (json)
    id (str)
    Em caso de ausência do id, programa retorna erro

    retorna o id da entrada inserido
    """
    _id = kwargs.get("_id")
    titulo = conteudo['titulo']
    data_publicacao = conteudo['data_publicacao']
    resumo = conteudo['resumo']
    post_url = conteudo['post_url']

    query_inserir = f"INSERT INTO posts (_id, titulo, data_publicacao, resumo, post_url) VALUES ('{_id}','{titulo}','{data_publicacao}','{resumo}','{post_url}')"
    
    try:
        cursor.execute(query_inserir)
        conn.commit()
    # exceção ao erro de entrada duplicada no banco
    except sqlite3.IntegrityError:
        print("Documento já existe no banco")
        return None
    
    consulta_id_query = f"SELECT _id from posts where _id = '{_id}'"
    cursor.execute(consulta_id_query)
    resultado = cursor.fetchone()
    cursor.close()
    # cursor retorna uma tupla, com o valor que interessa na primeira posição
    return resultado[0]
    


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
    pass

conteudo = {'titulo': 'É #FAKE que mensagens de bom dia no WhatsApp escondam códigos para hackear celulares', 'data_publicacao': '2021-03-17T19:59:22.655Z', 'resumo': 'WhatsApp nega boato. Nome de veículo de imprensa usado em texto falso nem sequer existe.', 'post_url': 'https://g1.globo.com/fato-ou-fake/noticia/2021/03/17/e-fake-que-mensagens-de-bom-dia-no-whatsapp-escondam-codigos-para-hackear-celulares.ghtml'}
_id = '9487d7a8daad626328aca18a2982b087'
res = inserir(cursor, conteudo, _id=_id)