import sqlite3
import math
from sqlite3 import Error
# permite importar de diretório acima mesmo sem estar em um pacote
# fonte https://gist.github.com/JungeAlexander/6ce0a5213f3af56d7369
import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
from post import Post

def conectar(nome_arquivo):
    conexao = sqlite3.connect(nome_arquivo)
    # definindo um cursor
    cursor = conexao.cursor()
    return cursor


class Banco:
    def __init__(self, cursor):
        self.cursor = cursor

    def tamanho_numero(self, numero):
        if numero == 0:
            return None
        elif isinstance(numero, int):
            digits = int(math.log10(numero))+1
            return digits
        else:
            return None


    def criar_tabela(self):
        # criando a tabela (schema)
        self.cursor.execute("""
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
        #self.cursor.close()

    def inserir(self, post):
        """
        Parâmetros:
        Post (objeto post que contém o conteúdo)
        Em caso de ausência do id, programa retorna erro

        retorna o id da entrada inserido
        """
        query_inserir = f"INSERT INTO posts (_id, titulo, data_publicacao, resumo, post_url) VALUES ('{post._id}','{post.titulo}','{post.data_publicacao}','{post.resumo}','{post.post_url}')"
        
        try:
            self.cursor.execute(query_inserir)
            # cursor pode commitar a query usando o método "connection"
            # fonte: https://stackoverflow.com/questions/50429589/python-sqlite3-is-commit-used-on-the-connect-or-cursor/50429875
            self.cursor.connection.commit()
        # exceção ao erro de entrada duplicada no banco
        except sqlite3.IntegrityError:
            print("Documento já existe no banco")
            return None
        except sqlite3.OperationalError:
            print("Por favor, crie as tabelas no banco antes de inserir dados")
        # consulta o id recém inserido, retorna caso localize
        consulta_id_query = f"SELECT _id from posts where _id = '{post._id}'"
        self.cursor.execute(consulta_id_query)
        resultado = cursor.fetchone()
        self.cursor.close()
        # cursor retorna uma tupla, com o valor que interessa na primeira posição
        return resultado[0]
        


    def alterar(self, colecao, busca, alterado):
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




    

conteudo = {'titulo': 'É #FAKE que mensagens de bom dia no WhatsApp escondam códigos para hackear celulares', 'resumo': 'WhatsApp nega boato. Nome de veículo de imprensa usado em texto falso nem sequer existe.', 'post_url': 'https://g1.globo.com/fato-ou-fake/noticia/2021/03/17/e-fake-que-mensagens-de-bom-dia-no-whatsapp-escondam-codigos-para-hackear-celulares.ghtml', "_id": '9487d7a8daad626328aca18a2982b087', 'data_publicacao': '2021-03-17T19:59:22.655Z'}
cursor = conectar('posts.db')
banco = Banco(cursor)
post = Post(conteudo)
banco.criar_tabela()
id = banco.inserir(post)
print(id)