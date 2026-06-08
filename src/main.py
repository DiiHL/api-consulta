from fastapi import FastAPI

from routers.atendimento_router import router as atendimento_router

app = FastAPI(
    title="API de Atendimento",
    description="API para consulta de indicadores de atendimentos por unidade",
    version="1.0.0",
)

app.include_router(atendimento_router)
