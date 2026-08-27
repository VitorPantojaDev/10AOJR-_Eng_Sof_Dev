"""
Repository: isola o acesso aos dados dos pontos de auriculoterapia/acupressão.

Hoje os dados vêm de um arquivo JSON (data/pontos.json).
Se um dia migrar para um banco (ex.: SQLite), só essa classe muda —
o resto do código (service, rotas) não precisa saber de onde os dados vêm.
"""

import json
import unicodedata
from pathlib import Path

CAMINHO_DADOS = Path(__file__).parent / "data" / "pontos.json"


def _normalizar(texto: str) -> str:
    """
    Deixa o texto em minúsculas, sem espaços nas pontas e sem acentos,
    para que "Dor de Cabeça", "dor de cabeça " e "dor de cabeca" sejam
    todos tratados como o mesmo sintoma na hora de comparar.
    """
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))


class PontoRepository:
    def __init__(self, caminho_dados: Path = CAMINHO_DADOS):
        self._caminho_dados = caminho_dados
        self._pontos = self._carregar()

    def _carregar(self) -> list[dict]:
        with open(self._caminho_dados, encoding="utf-8") as arquivo:
            return json.load(arquivo)

    def listar_todos(self) -> list[dict]:
        return self._pontos

    def buscar_por_id(self, ponto_id: str) -> dict | None:
        for ponto in self._pontos:
            if ponto["id"] == ponto_id:
                return ponto
        return None

    def buscar_por_sintomas(self, sintomas: list[str]) -> list[dict]:
        """
        Retorna os pontos cujo campo 'sintomas' tenha ao menos um item em
        comum com os sintomas recebidos, comparando por igualdade após
        normalizar o texto (minúsculas, sem espaços nas pontas, sem acentos).

        Um mesmo ponto nunca é retornado duas vezes, mesmo que combine com
        mais de um sintoma da lista recebida.

        Evoluções possíveis (não necessárias para a entrega):
        - dicionário de sinônimos (ex.: "insônia" ~ "dificuldade para dormir")
        - correspondência por substring ou fuzzy matching (ex. lib rapidfuzz)
        """
        sintomas_buscados = {_normalizar(s) for s in sintomas}

        resultado = []
        ids_ja_adicionados = set()

        for ponto in self._pontos:
            sintomas_do_ponto = {_normalizar(s) for s in ponto["sintomas"]}

            houve_match = sintomas_buscados & sintomas_do_ponto
            if houve_match and ponto["id"] not in ids_ja_adicionados:
                resultado.append(ponto)
                ids_ja_adicionados.add(ponto["id"])

        return resultado

    def adicionar(self, ponto: dict) -> dict:
        """
        TODO (opcional): validar campos obrigatórios (id, nome, sintomas,
        localizacao, orientacao) e persistir de volta no JSON, se quiser
        que o cadastro via POST /pontos seja permanente.
        """
        self._pontos.append(ponto)
        return ponto