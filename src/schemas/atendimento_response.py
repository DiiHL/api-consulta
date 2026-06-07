from datetime import datetime

from pydantic import BaseModel


class AtendimentoResponse(BaseModel):
    Unidade: str
    dataHoraBuscada: datetime
    TME_Minutos: float
    primeiroAtendimento: datetime
    UltimoAtendimento: datetime
    TotalAtendimento: int
