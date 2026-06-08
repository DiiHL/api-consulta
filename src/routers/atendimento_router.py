import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database import get_db
from repositories.atendimento_repository import AtendimentoRespository
from schemas.atendimento_response import AtendimentoResponse
from security.api_key import validar_api_key
from services.atendimento_service import AtendimentoService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")

DbSession = Annotated[Session, Depends(get_db)]
ApiKey = Annotated[None, Depends(validar_api_key)]


@router.get("/atendimentos", response_model=list[AtendimentoResponse])
def buscar_atendimento(db: DbSession, _: ApiKey):
    try:
        logging.info("Consultando indicadores de atendimento")

        repository = AtendimentoRespository(db)
        service = AtendimentoService(repository)
        return service.buscar_atendimento()
    except SQLAlchemyError as err:
        logging.exception("Erro ao consultar no banco de dados")

        raise HTTPException(
            status_code=500, detail="Erro ao consultar dados no banco"
        ) from err
