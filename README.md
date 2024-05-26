# Проект Foodgram

### Технологии
![example workflow](https://github.com/Konstantin-Leontyev/foodgram-project-react/actions/workflows/foodgram.yml/badge.svg)  
  
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

### Содержание

[Описание](#description)  
[Ресурсы проекта](#resorces)  
[Как запустить проект](#start)  
[Знакомство с проектом](#command)  
[Команда проекта](#team)

<a name="description"><h3>Описание проекта</h3></a>
___

«Фудграм» — сайт, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. 
Пользователям сайта также доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

Проект доступен по [ссылке](https://kkalogram.ru).

Проект состоит из следующих страниц: 
* главная — список из шести последних опубликован рецептов, отсортированных по дате публикации «от новых к старым».
* страница рецепта — полное описание рецепта. У авторизованных пользователей доступна возможность добавить рецепт в избранное и список покупок, а также подписаться на автора рецепта.
автора.
* страница подписок - список подписок пользователя, с возможностью отменить подписку.
* избранное - список избранных рецептов, с возможностью обновления ингредиентов в список покупок.
* список покупок - список ингредиентов необходимых к приобретению для приготовления добавленных рецептов.
* создание и редактирование рецепта.

<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="resorces"><h3>Ресурсы проекта</h3></a>
___
* Ресурс **users**: пользователи.
* Ресурс **followers**: сервис подписок.
* Ресурс **tags**: теги
* Ресурс **favorites**: избранное.
* Ресурс **carts**: корзина покупок.
* Ресурс **ingredients**: ингредиенты.
* Ресурс **recipes**: рецепты.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.

Документация доступна по [ссылке](https://kkalogram/swagger/).

<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="start"><h3>Как запустить проект:</h3></a>
___
Проведите подготовку своего сервера к запуску проекта.

* Подключитесь к своему удаленному серверу. 

* Обновите систему:
  
  ```angular2html
  sudo apt-get update && sudo apt-get -y install -f && sudo apt-get -y full-upgrade && sudo apt-get -y autoremove && sudo apt-get -y autoclean && sudo apt-get -y clean
  ```

* Установите docker:
  ```angular2html
  sudo apt install docker.io 
  ```

* Установите docker-compose:
  
  ```angular2html
  sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
  ```

* Установите права пользователя для docker-compose:
  ```angular2html
  sudo chmod +x /usr/local/bin/docker-compose
  ```

* В домашней директории пользователя /home/<you_user>/, создайте папку foodgram.
  ```angular2html
  mkdir foodgram
  ```

Проведите подготовку проекта на локальном компьютере:

* Клонируйте репозиторий проекта на свой локальный компьютер по SSH ссылке:

  ```angular2html
  git@github.com:Konstantin-Leontyev/foodgram-project-react.git
  ```

* Создайте .env файл и заполните его согласно примеру в .env.example:

* Скопируйте файлы docker-compose.yml .env в папку foodgram на удаленном сервере.

  ```angular2html
  scp -i <path_to_your_SSH_key>/<your_SSH_key_name> docker-compose.yml .env \ 
    <your_username>@<your_server_ip></your_server_ip>:/home/<your_username>/foodgram/
  ```
  
* На удаленном сервере запустите сборку проекта:
  ```angular2html
  sudo docker-compose up -d --build
  ```

Для использования Workflow:

* Добавьте в Secrets GitHub переменные окружения:

  ``` 
  DOCKER_PASSWORD=<your_DockerHub_password>
  DOCKER_USERNAME=<your_DockerHub_username>
  
  TELEGRAM_TO=<your_telegram_ID>
  TELEGRAM_TOKEN=<your_telegram_bot_token>
  
  HOST=<your_remote_server_IP>
  PASSPHRASE=<your_remote_server_passphrase>
  SSH_KEY=<your_privet_ssh_key (для получения команда: cat ~/.ssh/id_rsa)>
  USER=<your_remote_sever_username>
  ```

Workflow состоит из трёх шагов:

* Проверка кода на соответствие PEP8
* Сборка и публикация бэкенда образа на DockerHub.
* Автоматический деплой на удаленный сервер.
* Отправка уведомления о результате в телеграм-чат.

Сбор статики, применение миграций и загрузка базового набора ингредиентов будут выполнены автоматически.

Для доступа и управления административной зоной:

* Создайте суперпользователя Django:

  ```angular2html
  sudo docker exec -it backend python manage.py createsuperuser
  ```

<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="team"><h3>Команда проекта</h3></a>
___

[![Gmail Badge](https://img.shields.io/badge/-K.A.Leontyev@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:K.A.Leontyev@gmail.com)](mailto:K.A.Leontyev@gmail.com)<p align='left'>

Бэкенд - Константин Леонтьев
