from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories.atendimento_repository import AtendimentoRespository
from schemas.atendimento_response import AtendimentoResponse
from services.atendimento_service import AtendimentoService

router = APIRouter()

DbSession = Annotated[Session, Depends(get_db)]


@router.get("/atendimentos", response_model=list[AtendimentoResponse])
def buscar_atendimento(db: DbSession):

    repository = AtendimentoRespository(db)
    service = AtendimentoService(repository)

    return service.buscar_atendimento()
