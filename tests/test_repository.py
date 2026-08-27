"""
Testes de unidade da camada de dados (repository.py).

Testam a lógica de matching de sintomas -> pontos diretamente,
sem passar pelo Flask (mais rápidos e focados só na regra de negócio).
"""

import sys
from pathlib import Path

# Garante que o Python encontra os módulos da raiz do projeto (repository.py
# etc.), independentemente de onde o pytest for executado.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from repository import PontoRepository


def _ids(pontos: list[dict]) -> list[str]:
    """Facilita comparar resultados olhando só os ids dos pontos."""
    return [p["id"] for p in pontos]


def test_busca_por_sintoma_unico_retorna_ponto_esperado():
    repository = PontoRepository()

    resultado = repository.buscar_por_sintomas(["insônia"])

    assert _ids(resultado) == ["C7"]


def test_busca_por_sintoma_com_multiplos_pontos_nao_duplica():
    repository = PontoRepository()

    resultado = repository.buscar_por_sintomas(["ansiedade aguda"])

    assert sorted(_ids(resultado)) == sorted(["IG4", "C7", "Extra3"])
    # confere que nenhum id se repete no resultado
    assert len(_ids(resultado)) == len(set(_ids(resultado)))


def test_busca_ignora_maiusculas_e_acentos():
    repository = PontoRepository()

    resultado = repository.buscar_por_sintomas(["Dor de Cabeça"])

    assert "IG4" in _ids(resultado)


def test_busca_por_sintoma_inexistente_retorna_lista_vazia():
    repository = PontoRepository()

    resultado = repository.buscar_por_sintomas(["febre"])

    assert resultado == []