# API Bolões para Loterias

Esta API administra bolões para loterias, permitindo incluir, consultar e excluir bolões e seus respectivos participantes cadastrados.

## Requisitos

Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal.

Eexecute o comando abaixo para instalar as bibliotecas necessárias, descritas no arquivo `requirements.txt`:

```
(env)$ pip install -r requirements.txt
```

Certifique-se de que você tenha  todas as libs python listadas no `requirements.txt` instaladas.

## Como Usar

Para utilizar esta API, siga os passos abaixo:

1. Para executar esta API, execute o comando abaixo no terminal dentro do diretório raiz:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

2. Acesse a documentação Swagger para obter detalhes sobre as rotas e os parâmetros necessários.

3. Use as rotas listadas na documentação Swagger para adicionar, visualizar ou remover bolões e seus respectivos participantes.

## Documentação Swagger

Para obter a documentação completa desta API no estilo Swagger, [use este link](http://localhost:5000//openapi/swagger#/)

## Notas de Versão

### Versão 1.0.0 (setembro/2023)

- Criação da API.
- Funcionalidades implementadas: adicionar, visualizar e remover bolões e seus respectivos participantes.

## Autor

Este projeto foi desenvolvido por Marcio Motta e pode ser encontrado no [GitHub](https://github.com/marciolmcavalcanti/app_back).
