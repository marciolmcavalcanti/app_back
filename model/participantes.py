from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from model import Base


class Participante(Base):
    __tablename__ = 'participantes'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    qtd_cotas = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o participante e um bolão.
    # Aqui está sendo definido a coluna 'bolao' que vai guardar
    # a referencia ao bolao, a chave estrangeira que relaciona
    # um bolao ao participante.
    bolao_id = Column(Integer, ForeignKey("bolao.pk_bolao"), nullable=False)

    def __init__(self, bolao_id: int, nome: str, cotas: int, data_insercao: Union[DateTime, None] = None):
        """
        Adiciona um Participante

        Arguments:
            bolao_id: chave primária do bolão a participar
            nome: o nome do participante
            cotas: a quantidade de cotas desejada
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base            
        """
        self.bolao_id = bolao_id
        self.nome = nome
        self.qtd_cotas = cotas
        if data_insercao:
            self.data_insercao = data_insercao        
