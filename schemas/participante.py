from pydantic import BaseModel


class ParticipanteSchema(BaseModel):
    """ Define como um novo participante a ser inserido deve ser representado
    """
    bolao_id: int = 1
    nome: str = "Fulano de Tal"
    cotas: int = 1
