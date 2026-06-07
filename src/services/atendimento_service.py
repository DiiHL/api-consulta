from repositories.atendimento_repository import AtendimentoRespository
from schemas.atendimento_response import AtendimentoResponse


class AtendimentoService:
    def __init__(self, repository: AtendimentoRespository) -> None:
        self.repository = repository

    def buscar_atendimento(self) -> list[AtendimentoResponse]:
        atendimentos = self.repository.buscar_atendimento()

        return [AtendimentoResponse(**atendimento) for atendimento in atendimentos]
