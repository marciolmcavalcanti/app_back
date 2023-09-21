from pydantic import BaseModel
from typing import Optional, List
from model.bolao import Bolao
from schemas import ParticipanteSchema


class BolaoSchema(BaseModel):
    """ Define como um novo bolão a ser inserido deve ser representado
    """
    nome: str = "Mega Sena"
    qtd_cotas: Optional[int] = 15
    valor: float = 10.00


class BolaoBuscaSchemaByName(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita apenas com base no nome do bolão.
    """
    nome: str = "Mega Sena"


class BolaoBuscaSchemaById(BaseModel):
    """ Define como deve ser a estrutura que representa a busca, que será
        feita apenas com base no id do bolão.
    """
    id: int = 1


class ListagemBoloesSchema(BaseModel):
    """ Define como uma listagem de bolões será retornada.
    """
    boloes: List[BolaoSchema]


def apresenta_boloes(boloes: List[Bolao]):
    """ Retorna uma representação do bolão seguindo o schema definido em
        BolaoViewSchema.
    """
    result = []
    for bolao in boloes:
        result.append({
            "id": bolao.id,
            "nome": bolao.nome,
            "cotas": bolao.qtd_cotas,
            "valor": bolao.valor,
        })

    return {"boloes": result}


class BolaoViewSchema(BaseModel):
    """ Define como um bolão será retornado: bolão + participantes.
    """
    id: int = 1
    nome: str = "Bolão Mega Sena"
    cotas: Optional[int] = 15
    valor: float = 10.00
    total_participantes: int = 1
    participantes: List[ParticipanteSchema]


class BolaoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str


def apresenta_bolao(bolao: Bolao):
    """ Retorna uma representação do bolão seguindo o schema definido em
        BolãoViewSchema.
    """
    return {
        "id": bolao.id,
        "nome": bolao.nome,
        "cotas": bolao.qtd_cotas,
        "valor": bolao.valor,
        "total_participantes": len(bolao.participantes),
        "participantes": [{"Participante": p.nome} for p in bolao.participantes]
    }
