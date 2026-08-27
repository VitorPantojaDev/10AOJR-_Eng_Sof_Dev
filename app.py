from flask import Flask, jsonify, render_template, request

from repository import PontoRepository
from service import RecomendacaoService

app = Flask(__name__)

repository = PontoRepository()
service = RecomendacaoService(repository)


@app.get("/")
def pagina_de_teste():
    return render_template("index.html")


@app.get("/pontos")
def listar_pontos():
    return jsonify(service.listar_pontos())


@app.get("/pontos/<ponto_id>")
def detalhar_ponto(ponto_id):
    ponto = service.detalhar_ponto(ponto_id)
    if ponto is None:
        return jsonify({"erro": "Ponto não encontrado."}), 404
    return jsonify(ponto)


@app.post("/pontos/recomendar")
def recomendar():
    corpo = request.get_json(silent=True) or {}
    sintomas = corpo.get("sintomas")

    if not sintomas or not isinstance(sintomas, list):
        return jsonify({"erro": "Envie 'sintomas' como uma lista de strings."}), 400

    try:
        pontos = service.recomendar_por_sintomas(sintomas)
    except ValueError as erro:
        return jsonify({"erro": str(erro)}), 400

    return jsonify(pontos)


@app.post("/pontos")
def cadastrar_ponto():
    # TODO (opcional): validar o corpo recebido antes de cadastrar.
    ponto = request.get_json(silent=True) or {}
    ponto_criado = repository.adicionar(ponto)
    return jsonify(ponto_criado), 201


if __name__ == "__main__":
    app.run(debug=True)
