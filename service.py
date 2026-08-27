from repository import PontoRepository


class RecomendacaoService:
    def __init__(self, repository: PontoRepository):
        self._repository = repository

    def recomendar_por_sintomas(self, sintomas: list[str]) -> list[dict]:
        if not sintomas:
            raise ValueError("Informe ao menos um sintoma.")

        # TODO: aqui é o lugar de aplicar Strategy, se for esse o padrão
        # escolhido no Caminho A (ex.: trocar a estratégia de matching
        # sem mexer no resto do service).
        pontos_encontrados = self._repository.buscar_por_sintomas(sintomas)

        return pontos_encontrados

    def listar_pontos(self) -> list[dict]:
        return self._repository.listar_todos()

    def detalhar_ponto(self, ponto_id: str) -> dict | None:
        return self._repository.buscar_por_id(ponto_id)
