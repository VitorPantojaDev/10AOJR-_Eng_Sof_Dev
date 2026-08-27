import json
import unicodedata
from pathlib import Path

CAMINHO_DADOS = Path(__file__).parent / "data" / "pontos.json"


def _normalizar(texto: str) -> str:
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