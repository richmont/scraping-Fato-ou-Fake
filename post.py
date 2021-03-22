class Post:
    def __init__(self, conteudo):
        """
        Inicializa o post com um dicionário com o conteúdo do post
        """
        self._id = conteudo['_id']
        self.titulo = conteudo['titulo']
        self.data_publicacao = conteudo['data_publicacao']
        self.resumo = conteudo['resumo']
        self.post_url = conteudo['post_url']