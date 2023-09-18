from flask import Flask, request, send_from_directory, render_template
from flask_openapi3 import OpenAPI, Info, Tag

from flask import redirect

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from model import Session
from model.bolao import Bolao
from model.participantes import Participante
from schemas import *
from logger import logger
from flask_cors import CORS
from urllib.parse import unquote


info = Info(title="Bolões para Loterias", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)


# definindo tags
home_tag = Tag(name="Documentação Swagger", description="Documentação estilo Swagger.")
bolao_tag = Tag(name="Bolão", description="Adição, visualização e remoção de bolões e participantes na base de dados.")
participante_tag = Tag(name="Participante", description="Adição de um participante à um Bolão cadastrado na base")


@app.route('/')
def home():
    """Redireciona para documentação da API no estilo Swagger.
    """
    return redirect('/openapi/swagger')


# Carrega o favicon da aplicação
@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/x-icon')


# Adiciona um Bolão
@app.post('/add_bolao', tags=[bolao_tag],
          responses={"200": BolaoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_bolao(form: BolaoSchema):
    
    bolao = Bolao(
        nome = request.form.get("nome"),
        qtd_cotas = int(request.form.get("qtd_cotas")),
        valor = request.form.get("valor")
    )

    logger.debug(f"Adicionando um Bolão: '{bolao.nome}'")
    try:
        # cria a conexão com a base
        session = Session()

        # adiciona o bolão
        session.add(bolao)

        # efetiva o camando de adição de novo item na tabela
        session.commit()

        logger.debug(f"Bolão adicionado: '{bolao.nome}'")
        return apresenta_bolao(bolao), 200
    
    except IntegrityError as e:
        # Ocorreu duplicidade do nome
        error_msg = "Um Bolão de mesmo nome já existe na base!"
        return {"mensagem": error_msg}, 409    
    
    except Exception as e:
        # Se erro não previsto
        error_msg = "Não foi possível adicionar o novo bolão!"
        logger.warning(f"Erro ao adicionar bolão '{bolao.nome}', {error_msg}")
        return {"message": error_msg}, 400
    

# Busca todos os bolões cadastrados
@app.get('/boloes', tags=[bolao_tag],
         responses={"200": ListagemBoloesSchema, "404": ErrorSchema})
def get_boloes():
    """Faz a busca por todos os Produto cadastrados

    Retorna uma representação da listagem de Bolões.
    """
    logger.debug(f"Buscando bolões ")

    # cria conexão com a base
    session = Session()

    # fazo a busca por todos
    boloes = session.query(Bolao).all()        

    if not boloes:
        # se não há bolões cadastrados retorna vazio
        return {"bolões": []}, 200
    else:
        logger.debug(f"%d Bolões encontrados" % len(boloes))
        # retorna a representação de bolão
        return apresenta_boloes(boloes), 200


# Busca um determinado Bolão cadastrado
@app.get('/bolao', tags=[bolao_tag],
         responses={"200": BolaoViewSchema, "404": ErrorSchema})
def get_bolao(query: BolaoBuscaSchema):
    """Faz a busca por um Bolão a partir do id do bolão

    Retorna uma representação dos bolões e participantes associados.
    """
    bolao_nome = query.nome
    logger.debug(f"Coletando dados sobre bolão #{bolao_nome}")

    # criando conexão com a base
    session = Session()

    # fazendo a busca
    bolao = session.query(Bolao).filter(Bolao.nome == bolao_nome).first()

    if not bolao:
        # se o bolão não foi encontrado
        error_msg = "Bolão não encontrado na base!"
        logger.warning(f"Erro ao buscar bolão '{bolao_nome}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        # retorna a representação de produto
        logger.debug(f"Bolão encontrado: '{bolao.nome}'")        
        return apresenta_bolao(bolao), 200


# Deleta um Bolão cadastrado
@app.delete('/bolao', tags=[bolao_tag],
            responses={"200": BolaoDelSchema, "404": ErrorSchema})
def del_bolao(query: BolaoBuscaSchema):
    """Deleta um Bolão a partir do nome de bolão informado

    Retorna uma mensagem de confirmação da remoção.
    """
    bolao_nome = unquote(unquote(query.nome))
    logger.debug(f"Deletando dados do Bolão #{bolao_nome}")

    # criando conexão com a base
    session = Session()

    # fazendo a remoção
    count = session.query(Bolao).filter(Bolao.nome == bolao_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado o Bolão #{bolao_nome}")
        return {"message": "Bolão removido", "nome": bolao_nome}
    else:
        # se o bolão não foi encontrado
        error_msg = "Bolão não encontrado na base!"
        logger.warning(f"Erro ao deletar o Bolão #'{bolao_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    

# Adiciona um Participante a um bolão
@app.post('/participante', tags=[participante_tag],
          responses={"200": BolaoViewSchema, "404": ErrorSchema})
def add_participante(form: ParticipanteSchema):
    """Adiciona de um novo participante à um bolão cadastrado na base identificado pelo id

    Retorna uma representação dos bolões e participantes associados.
    """
    bolao_id  = int(form.bolao_id)
    logger.debug(f"Adicionando participante ao bolão #{bolao_id}")

    # criando conexão com a base
    session = Session()

    # fazendo a busca pelo produto
    bolao = session.query(Bolao).filter(Bolao.id == bolao_id).first()

    if not bolao:
        # se bolão não encontrado
        error_msg = "Bolão não encontrado na base!"
        logger.warning(f"Erro ao adicionar participante ao bolão '{bolao_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o Participante
    nome = form.nome
    cotas = int(form.cotas)
    participante = Participante(bolao_id, nome, cotas)

    # adicionando o participante ao bolao
    bolao.adiciona_participante(participante)
    session.commit()

    logger.debug(f"Adicionado participante ao bolão #{bolao_id}")

    # retorna a representação de bolão
    return apresenta_bolao(bolao), 200
