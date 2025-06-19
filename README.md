[![CI](https://github.com/joseevilasio/my-videos-lib/actions/workflows/main.yml/badge.svg?branch=main)](https://github.com/joseevilasio/my-videos-lib/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/joseevilasio/CRUD-Challenge-Alura/graph/badge.svg?token=VK8Z1CJZ6J)](https://codecov.io/gh/joseevilasio/CRUD-Challenge-Alura)

# MY VIDEOS LIB - API CRUD - ALURA CHALLENGE

A library to store information about your favorite videos. This project is part of an Alura challenge.  
To learn more about the challenge, [click here.](#-challenge)

| :placard: Vitrine.Dev |   [Vitrine Dev José Junior](https://cursos.alura.com.br/vitrinedev/joseevilasio/project/CRUD-Challenge-Alura/3844433) |
| -------------  | --- |
| :sparkles: Project Name  | **MY VIDEOS LIB - API - CRUD**
| :label: Tech Stack       | Python, Flask, MongoDB, Dynaconf
| :rocket: URL             | https://github.com/joseevilasio/my-videos-lib
| :fire: Challenge         | [Alura](https://www.alura.com.br/challenges/back-end-5/semana-01-implementando-api-rest)

<!-- Insert image with #vitrinedev at the end of the link -->
![](https://github.com/joseevilasio/my-videos-lib/blob/main/assets/myvideoslib-logo.png)

### 📋 Requirements

```
Python
Poetry
Docker
```

### 🔧 Installation

Clone the project repository:
```
$ gh repo clone joseevilasio/my-videos-lib
```
Install project dependencies with Poetry:
```
$ poetry install
```
The project uses MongoDB as the database, so we need to start a container:
```
$ docker container run -d -p 27017:27017 --name mongo-myvideoslib mongo:latest
```
Create a `.secrets.toml` file inside the `api` folder with the following content:
```
[secrets]

[development]
secret_key = "your secret key"
JWT_SECRET_KEY = "your secret key"
```
Run the project locally to manage and consume the API:
```
$ poetry run gunicorn -w 4 'api.app:create_app()'
```
Alternative way to manage the API via CLI:
```
$ poetry run flask controller --help
```

### 🔧 Docker Compose Installation
To run with Docker Compose:
```
$ sudo docker compose up --build
```

### 📆 How It Works
You must create an account to use the application, either through the CLI or via the `/register` route. Once registered, you'll receive a token to authenticate requests, especially for accessing `/admin`.

API usage examples:

**CREATE** - POST `/videos/new` to add a new video to the database.
Example JSON:
```
{       
    "title": "Python Programming Introduction",
    "description": "Start learning Python with Alura",
    "url": "https://www.youtube.com/watch?v=8485663",
    "categoryId": "1"
}
```
**CREATE** - POST `/category/new` to add a new category.
Example JSON:
```
{       
    "title": "Game",
    "color": "red"
}
```
**READ** - GET `/videos` returns all videos; `/videos/id` fetches a video by its ID.

**READ** - GET `/videos/?search=game` returns videos matching a keyword.

**READ** - GET `/category` returns all categories; `/category/id` fetches a category by ID.

**READ** - GET `/category/id/videos` returns all videos associated with a given category.

**UPDATE** - PUT `/videos/id` updates a video's information.

**UPDATE** - PUT `/category/id` updates a category.

**DELETE** - DELETE `/videos/id` removes a video.

**DELETE** - DELETE `/category/id` removes a category.

![](https://github.com/joseevilasio/my-videos-lib/blob/main/assets/usage-api.gif)

### 💡 Challenge

The challenge was to build a full CRUD (Create, Read, Update, Delete) API.

Documentation for each development week is available on [dev.to/josejunior](https://dev.to/josejunior). Status: Not Started ❌ / Completed ✅

## Week 1 - Implementing a REST API ✅
**Initial implementation:** Design the database and implement routing logic. 🔍 [Issue #1](https://github.com/joseevilasio/CRUD-Challenge-Alura/issues/1#issue-1629409758)

## Week 2 - Adding Entities and Relationships ✅
**Category implementation:** Add category collection and establish relationships with existing data. 🔍 [Issue #2](https://github.com/joseevilasio/CRUD-Challenge-Alura/issues/2#issue-1629629636)

## Week 3 - Implementing Authentication ✅
**Security:** Implement authentication mechanism to restrict access to registered users. 🔍 [Issue #3](https://github.com/joseevilasio/CRUD-Challenge-Alura/issues/3#issue-1638409239)

## Week 4 - Deploy ✅
**Deployment:** Deploy the API using a cloud platform like Heroku. 🔍 [Issue #3](https://github.com/joseevilasio/CRUD-Challenge-Alura/issues/3#issue-1638409239)
