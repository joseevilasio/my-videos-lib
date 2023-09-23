[![CI](https://github.com/joseevilasio/my-videos-lib/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/joseevilasio/my-videos-lib/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/joseevilasio/CRUD-Challenge-Alura/graph/badge.svg?token=VK8Z1CJZ6J)](https://codecov.io/gh/joseevilasio/CRUD-Challenge-Alura)

# MY VIDEOS LIB - API CRUD - ALURA CHALLENGE 

Uma biblioteca para armazenar as informações sobre os seus vídeos favoritos. O projeto faz parte de um desafio da Alura. 
Para saber mais sobre o desafio, [clique aqui.](#-desafio)

| :placard: Vitrine.Dev |   [Vitrine Dev José Junior](https://cursos.alura.com.br/vitrinedev/joseevilasio/project/CRUD-Challenge-Alura/3844433) |
| -------------  | --- |
| :sparkles: Nome        | **MY VIDEOS LIB - API - CRUD**
| :label: Tecnologias | python, flask, mongodb, dynaconf
| :rocket: URL         | https://github.com/joseevilasio/my-videos-lib
| :fire: Desafio     | [Alura](https://www.alura.com.br/challenges/back-end-5/semana-01-implementando-api-rest?utm_source=ActiveCampaign&utm_medium=email&utm_content=%5BChallenge+Back-End%5D+Comece+agora%21&utm_campaign=%5BCHALLANGE%5D+%28Back-End+5a+ed+%29+Liberação+da+aula+01++%2B+convite+live+dive+coding&vgo_ee=kJRPc3gXJKD3%2FdmGS%2B55mMe9HldV2%2BVjsIQZGqVXtPc%3D)

<!-- Inserir imagem com a #vitrinedev ao final do link -->
![](https://github.com/joseevilasio/CRUD-Challenge-Alura/blob/main/assets/%20thumbnail.gif)

### 📋 Pré-requisitos

```
Python
Poetry
Docker
```
### 🔧 Instalação

Fazer um clone do repositório do projeto:
```
$ gh repo clone joseevilasio/my-videos-lib
```
Instalar as dependências do projeto com o Poetry:
```
$ poetry install
```
O projeto utiliza mongoDB como banco de dados, então temos que iniciar um container:
```
$ docker container run -d -p 27017:27017 --name mongo-myvideoslib mongo:latest
```
Agora é rodar o projeto em localhost para gerenciar e consumir a API:
```
$ poetry run gunicorn -w 4 'api.app:create_app()'
```
Uma outra opção para gerenciar a API através da linha de comando:
```
$ poetry run flask controller --help
```

### 🔧 Instalação Docker Compose
Para instalação com o Docker basta utilizar o Docker compose:
```
$ sudo docker compose up --build
```

### 📦 Como funciona
É preciso criar uma conta para utilizar a aplicação, é possível fazer isso através do CLI e ```/register``` com a conta criada terá acesso ao ```token```, para utilizar nas requisições, ao acessar ```/admin```.

Consumindo a API:

CREATE - POST ```/videos/new``` adicionar um video no banco de dados.

exemplo json:
```
{       
    "title": "Introdução à programação Python",
    "description": "Comece a aprender Python com a Alura",
    "url": "https://www.youtube.com/watch?v=8485663",
    "categoryId": "1"
}
```
CREATE - POST ```/category/new``` adicionar uma categoria no banco de dados.
exemplo json :
```
{       
    "title": "Game",
    "color": "red",
}
```

READ - GET ```/videos``` devolve um json com todos os vídeos no banco de dados, outra forma é ```/videos/id``` repassar o id do vídeo.

READ - GET ```/videos/?search=game``` devolve um json com todos os vídeos no banco de dados relacionado com o termo procurado.

READ - GET ```/category``` devolve um json com todas as categorias no banco de dados, outra forma é ```/category/id``` repassar o id da categoria.

READ - GET ```/category/id/videos``` devolve um json com todas vídeos relacionado a categoria indicado com id.

UPDATE - PUT ```/videos/id``` atualiza as informações o vídeo.

UPDATE - PUT ```/category/id``` atualiza as informações da categoria.

DELETE - DELETE ```/videos/id``` deleta o vídeo.

DELETE - DELETE ```/category/id``` deleta a categoria.


### 💡 Desafio

O desafio consiste em criar um CRUD (Create, Read, Update, Delete)

Documentação do inicio ao fim do projeto no dev.to/josejunior, status indicando o andamento. 

Exemplo: Não iniciado ❌ / Iniciado ✅ 

## Semana 1 - Implementando uma API REST ✅
**Implementação inicial:** Modelar o banco de dados conforme regra de neǵocio e roteamento. 🔍 [https://github.com/joseevilasio/CRUD-Challenge-Alura/issues/1#issue-1629409758]

## Semana 2 - Adicionando entidades e relacionamentos  ✅
**Implementação de Categorias:** Adicionar table em database com categoria e relacionar com database já existente e rotear novas rotas.  🔍[https://github.com/joseevilasio/CRUD-Challenge-Alura/issues/2#issue-1629629636]

## Semana 3 - Implementando serviços de autenticação ✅
**Segurança:** Nesta semana, o desafio será implementar um mecanismo de autenticação na API, para que apenas usuários autenticados possam interagir com ela. 🔍 [https://github.com/joseevilasio/CRUD-Challenge-Alura/issues/3#issue-1638409239]

## Semana 4 - Deploy ❌
**Deploy:** Será necessário realizar o deploy da API em algum provedor Cloud, como o Heroku. 🔍 [https://github.com/joseevilasio/CRUD-Challenge-Alura/issues/3#issue-1638409239]
 
