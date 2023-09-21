from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base, Participante


class Bolao(Base):
    __tablename__ = 'bolao'

    id = Column("pk_bolao", Integer, primary_key=True)
    nome = Column(String(140))
    # nome = Column(String(140), unique=True)
    qtd_cotas = Column(Integer)
    valor = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o bolão e o participante.
    # Essa relação é implicita, não está salva na tabela 'bolão',
    # mas aqui estou deixando para SQLAlchemy a responsabilidade
    # de reconstruir esse relacionamento.
    participantes = relationship("Participante")

    def __init__(self, nome: str, qtd_cotas: int, valor: float,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Bolão

        Arguments:
            nome: nome do bolão.
            quantidade: quantidade de cotas que se espera vender daquele bolão
            valor: valor de uma cota do bolão
            data_insercao: data de quando o bolão foi inserido à base
        """
        self.nome = nome
        self.qtd_cotas = qtd_cotas
        self.valor = valor

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_participante(self, participante: Participante):
        """ Adiciona um novo participante ao Bolão
        """
        self.participantes.append(participante)
