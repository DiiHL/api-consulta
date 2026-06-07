from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


class AtendimentoRespository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def buscar_atendimento(self) -> list[dict[str, Any]]:
        query = text("""
        SELECT
            u.ID AS IDUnidade,
            u.Descricao AS Unidade,
            CAST(CURRENT_DATE AS VARCHAR(10)) || ' ' ||
            CAST(CURRENT_TIME AS VARCHAR(8)) AS DataHoraBUSCA,
            ROUND(AVG(CAST(s.AtendimentoTempoEspera AS FLOAT)), 2) AS TME_Minutos,
            MIN(
                CAST(s.AtendimentoDataInicio AS VARCHAR(10)) || ' ' ||
                CAST(s.AtendimentoHoraInicio AS VARCHAR(8))
            ) AS PrimeiroAtendimento,
            MAX(
                CAST(s.AtendimentoDataFinal AS VARCHAR(10)) || ' ' ||
                CAST(s.AtendimentoHoraFinal AS VARCHAR(8))
            ) AS UltimoAtendimento,
            COUNT(*) AS TotalAtendimentos
        FROM s10_dado.TblSenhaGerada s
        INNER JOIN s10_dado.TblUnidadeAtendimento u
            ON s.SenhaUnidade = u.ID
        WHERE s.AtendimentoDataInicio >= CURRENT_DATE
          AND s.AtendimentoDataFinal IS NOT NULL
        GROUP BY
            u.Descricao,
            CAST(s.AtendimentoDataInicio AS VARCHAR(10))
        """)

        result = self.db.execute(query)
        linhas = result.mappings().all()

        return [
            {
                "unidade": linha["unidade"],
                "data_hora_busca": linha["data_hora_busca"],
                "tme_minutos": linha["tme_minutos"],
                "primeiro_atendimento": linha["primeiro_atendimento"],
                "ultimo_atendimento": linha["ultimo_atendimento"],
                "total_atendimentos": linha["total_atendimentos"],
            }
            for linha in linhas
        ]
