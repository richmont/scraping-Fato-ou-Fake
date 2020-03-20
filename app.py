from flask import Flask, request, jsonify
from consultas import *

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"


@app.route('/api/v1/posts/<id>', methods=['GET'])
def get_by_id(id):
    resultado = consulta_post_id(posts, id)
    if resultado is None:
        headers = {"Content-Type": "application/json"}
        return make_response('Post não encontrado', 404, headers=headers)
    else:
        return jsonify(resultado)

@app.route('/api/v1/posts/contador/', methods=['GET'])
def contador():
    resultado = quantidade_total(posts)
    if resultado is None:
        headers = {"Content-Type": "application/json"}
        return make_response('Post não encontrado', 404, headers=headers)
    else:
        return {"Número de posts armazenados no banco": resultado}


@app.route('/api/v1/posts/consulta', methods=['POST'])
def consulta_geral():
    data = request.get_json()
    query = data["query"]
    resultado = consulta_campo_regex(posts, query)
    return jsonify(resultado)


if __name__ == '__main__':
    app.run(debug=True)
