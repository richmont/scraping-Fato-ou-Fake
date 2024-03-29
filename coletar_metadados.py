from pymongo import MongoClient, errors
from db.mongo import inserir
from db.mongo import alterar
from scraping import requisicao
from db.sqlite import conectar, Banco
from post import Post
import json
from conf.settings import MONGO_URL, GLOBO_URL_INICIO, GLOBO_URL_FIM, GLOBO_ID, NUM_PAG, SGBD
local = MONGO_URL
try:
    cliente = MongoClient(local)
except errors.InvalidURI:
    raise errors.InvalidURI("Verifique o endereço de acesso ao banco")
banco = cliente.fato_ou_fake
posts = banco.posts
cursor = conectar('posts.db')
banco_sqlite = Banco(cursor)
banco_sqlite.criar_tabela()

class Coletor_metadados:
    def __init__(self, url, paginas, sgbd):
        self.url = url
        self.paginas = paginas
        self.sgbd = sgbd
    
    def dados_posts_banco(self):
        """
        Armazena o conteúdo da chave "items" de um json recebido via requisição GET em um banco MongoDB
        colecao (MongoDB Collection)
        url (REST API url)
        paginas (int)
        """
        for x in range(1, self.paginas):

            print("iniciando requisição na linha ", x)
            # requere usando o URL e o número de páginas, guarda o conteúdo da requisição em json_data
            json_data = requisicao(url, pagina=x)
            # se a requisição não vier vazia
            if json_data is not None:
                # checa se o campo "items" tem elementos a serem colhidos
                tamanho_resposta = len(json_data["items"])
                if tamanho_resposta > 0:
                    # se for maior que zero, continua e insere no banco
                    # começa o processo de filtragem
                    items = json_data["items"]
                    
                    for item in items:
                        try:
                            json_post = {}
                            post_id = item["id"]
                            post_titulo = item["content"]["title"]
                            #post_titulo.replace("'","''")
                            
                            
                            post_data_publicacao = item["publication"]
                            post_resumo = item["content"]["summary"]
                            post_url = item["content"]["url"]
                            if post_id is None and post_titulo is not None:
                                print("ID do post inválido")
                                pass
                            elif post_titulo is None:
                                print("Título do post inválido")
                                continue
                            elif post_data_publicacao is None:
                                print("Data da publicação inválida")
                                continue
                            elif post_resumo is None:
                                print("Resumo do post inválido")
                                continue
                            elif post_url is None:
                                print("URL do post inválido")
                                continue
                            json_id = {"_id": post_id}
                            json_titulo = {"titulo": post_titulo}
                            json_data_publicacao = {"data_publicacao": post_data_publicacao}
                            json_resumo = {"resumo": post_resumo}
                            json_post_url = {"post_url": post_url}
                            json_post.update(json_id)
                            json_post.update(json_titulo)
                            json_post.update(json_data_publicacao)
                            json_post.update(json_resumo)
                            json_post.update(json_post_url)
                            # cria um objeto post com o conteúdo coletado em json
                            post = Post(json_post)
                            
                            if self.sgbd == 'sqlite':
                                # inicializa a variavel caso ela não seja ocupada por causa de exceção
                                id_inserido = None
                                try:
                                    id_inserido = banco_sqlite.inserir(post)
                                except TypeError:
                                    print("inserção falhou com id do post: ", post_id)
                                if id_inserido == None:
                                    print("inserção falhou com id do post: ", post_id)
                                # se retornou um id não vazio, inserção ocorreu sem problemas
                                else:
                                    print("Post inserido com id: ", id_inserido)
                            """
                            Comentar o trecho que trata do mongo, pois não vamos usar por enquanto
                            elif self.sgbd == 'mongodb':
                                pass
                            else:
                                print("SGBD inválido, não consigo salvar os dados")
                                break
                            
                            if id_inserido is not None:
                                print("Post inserido com id: ", id_inserido)
                            else:
                                print("inserção falhou com id do post: ", post_id)
                            """
                            del post
                        except KeyError as e:
                            print("Chave não encontrada", e)
                            

                else:
                    # página não tem elemento "items", exibe erro e interrompe o programa
                    print("Resposta do servidor sem conteúdo na página ", x)
                    break
            else:
                # requisição não recebeu nenhum dado, interrompe o programa
                print("requisição vazia recebida na linha ", x)
                break
# URL formada pelos endereços e ID localizadas no arquivo .env
url = GLOBO_URL_INICIO+GLOBO_ID+GLOBO_URL_FIM
# número máximo de páginas para localizar também configurado no arquivo .env
#dados_posts_banco(posts, url, int(NUM_PAG))
coletor = Coletor_metadados(url, int(NUM_PAG), SGBD)
coletor.dados_posts_banco()
banco_sqlite.cursor.close()


