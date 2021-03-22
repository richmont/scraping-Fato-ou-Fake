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
    """
    nome_arquivo (string)
    realiza a conexão SQLite ao arquivo informado nesta variável
    Caso não exista, será criado
    não esqueça de criar as tabelas antes de inserir dados
    """
    conexao = sqlite3.connect(nome_arquivo)
    # definindo um cursor
    cursor = conexao.cursor()
    return cursor


class Banco:
    """
    Objeto que contém todos os métodos para interagir com dados do banco SQLite
    seu parâmetro de criação é o cursor referente ao banco usado
    """
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

    def existe_by_id(self, _id):
        """
        Parâmetros:
        _id (string)

        Consulta o banco e verifica se determinada entrada existe, localizando pelo id
        """
        query_verificar_existe = f"SELECT _id from posts where _id = '{_id}'"
        self.cursor.execute(query_verificar_existe)
        # o resultado do fetchone é None caso não seja encontrado nada no banco
        resultado = cursor.fetchone()
        if resultado == None:
            return False
        else:
            return True

    def criar_tabela(self):
        """
        Cria as tabelas necessárias ao funcionamento do banco, 
        requisito rodar esse método antes de inserir dados
        """
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
        self.cursor.connection.commit()
        print('Tabela criada com sucesso.')
        #self.cursor.close()

    def inserir(self, post):
        """
        Parâmetros:
        Post (objeto post que contém o conteúdo)
        insere as informações de um objeto Post na tabela do banco

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
            # exceção da ausência das tabelas, oo que impede inserção dos dados
            # necessário rodar o método "criar_tabelas" caso haja esse problema
            print("Por favor, crie as tabelas no banco antes de inserir dados")
        # consulta o id recém inserido, retorna caso localize
        consulta_id_query = f"SELECT _id from posts where _id = '{post._id}'"
        self.cursor.execute(consulta_id_query)
        # consulta apenas uma entrada, é o bastante aqui
        resultado = cursor.fetchone()
        # fecha o cursor após terminar de consultar o banco
        self.cursor.close()
        # cursor retorna uma tupla, com o valor que interessa na primeira posição
        return resultado[0]
        
    def alterar(self, _id, alteracao):
        """
        Parãmetros:
        cursor (SQLite cursor)
        _id (string)
        alteracao (lista)

        Altera uma entrada já existente no banco
        localiza o campo pelo _id, o registro chave

        retorna o conteúdo do campo alterado
        """
        if self.existe_by_id(_id):
            string_alteracoes = str()
            # para cada chave da alteração
            for x in alteracao.keys():
                # concatena o trecho da alteração
                # com a chave (x) e seu conteúdo (alteracao[x])
                
                string_alteracoes += f"'{x}' = '{alteracao[x]}'"
            # monta a query incluindo o trecho dos campos alterados e o _id
            # importante ter aspas simples em cada entrada
            query_alterar = str(f"update posts set {string_alteracoes} where _id = '{_id}'")
            try:
                self.cursor.execute(query_alterar)
                self.cursor.connection.commit()
            # tentar alterar uma coluna que não existe retorna esse erro
            except sqlite3.OperationalError as e:
                print("Alteração falhou: ", e)


        else:
            print("_id não localizado, alteração falhou")

    def apagar(self, _id):
        """
        Parâmetros:
        _id (string)

        Apaga do banco de dados a entrada correspondente a _id informada
        """
        if self.existe_by_id(_id):
            query_apagar = f"delete from posts where '_id' = '{_id}'"
            try:
                self.cursor.execute(query_apagar)
                self.cursor.connection.commit()
            except sqlite3.OperationalError as e:
                print("Apagar falhou: verifique as tabelas do banco ou execute criar_tabela ", e)
        else:
            print("Apagar falhou, id não existe")
