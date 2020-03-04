from pymongo import MongoClient
from banco import inserir
from banco import alterar
from scraping import requisicao
import json
local = "mongodb://python:penis@localhost"
cliente = MongoClient(local)
banco = cliente.fato_ou_fake
# brutos = banco.dados_brutos
posts = banco.posts


def dados_posts_banco(colecao, url, paginas):
    """
    Armazena o conteúdo da chave "items" de um json recebido via requisição GET em um banco MongoDB
    colecao (MongoDB Collection)
    url (REST API url)
    paginas (int)
    """
    for x in range(1, paginas):

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
                        post_data_publicacao = item["publication"]
                        post_resumo = item["content"]["summary"]
                        post_url = item["content"]["url"]
                        post_imagem_url = item["content"]["image"]["url"]
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
                        elif post_imagem_url is None:
                            print("URL da imagem do post inválida")
                            continue
                        
                        json_titulo = {"titulo": post_titulo}
                        json_data_publicacao = {"data_publicacao": post_data_publicacao}
                        json_resumo = {"resumo": post_resumo}
                        json_post_url = {"post_url": post_url}
                        json_post_imagem = {"post_imagem": post_imagem_url}
                        json_post.update(json_titulo)
                        json_post.update(json_data_publicacao)
                        json_post.update(json_resumo)
                        json_post.update(json_post_url)
                        json_post.update(json_post_imagem)
                        
                        id_inserido = inserir(posts, json_post, id=post_id)
                        if id_inserido is not None:
                            print("Post inserido com id: ", id_inserido)
                        else:
                            print("inserção falhou com id do post: ", post_id)
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


# endereço da API do Fato ou Fake
url = "https://falkor-cda.bastian.globo.com/tenants/g1/instances/9a0574d8-bc61-4d35-9488-7733f754f881/posts/page/"
dados_posts_banco(posts, url, 70)

