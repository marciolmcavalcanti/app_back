from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# importando os elementos definidos no modelo
from model.base import Base
from model.participantes import Participante
from model.bolao import Bolao

import os

db_path = "database/"
# Cria o diretório da base de dados caso não exista
if not os.path.exists(db_path):
   os.makedirs(db_path)

# url de acesso ao banco (sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# cria a conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
