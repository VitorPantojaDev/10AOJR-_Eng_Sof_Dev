"""
Testes de integração das rotas (app.py), usando o test client do Flask.

Simulam requisições HTTP reais contra os endpoints, sem precisar subir
o servidor de verdade.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_recomendar_com_sintoma_valido_retorna_ponto_esperado(client):
    resposta = client.post(
        "/pontos/recomendar",
        json={"sintomas": ["insônia"]},
    )

    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert [ponto["id"] for ponto in corpo] == ["C7"]


def test_recomendar_sem_campo_sintomas_retorna_erro_400(client):
    resposta = client.post("/pontos/recomendar", json={})

    assert resposta.status_code == 400
    corpo = resposta.get_json()
    assert "erro" in corpo


def test_listar_pontos_retorna_todos_os_pontos_cadastrados(client):
    resposta = client.get("/pontos")

    assert resposta.status_code == 200
    corpo = resposta.get_json()
    assert len(corpo) == 4
    assert {"PC6", "IG4", "C7", "Extra3"} == {ponto["id"] for ponto in corpo}