# Проект Kkalogram

### Технологии
![example workflow](https://github.com/Konstantin-Leontyev/kkalogram/actions/workflows/kkalogram.yml/badge.svg)  
  
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

«Ккалограм» — сайт, на котором пользователи могут публиковать свои рецепты, добавлять чужие рецепты в избранное и подписываться на публикации других авторов. 
Пользователям сайта также доступен сервис «Список покупок». Он позволит создавать список продуктов, которые нужно купить для приготовления выбранных блюд.

<p align="center"><img height="425" src="preview.png"></p>

Проект доступен по [ссылке](https://kkalogram.ru/recipes).

Проект состоит из следующих страниц: 
* Главная - список из шести последних опубликован рецептов, отсортированных по дате публикации «от новых к старым»;
* Страница рецепта - полное описание рецепта. У авторизованных пользователей доступна возможность добавить рецепт в избранное и список покупок, а также подписаться на автора рецепта;
* Страница подписок - список подписок пользователя, с возможностью отменить подписку;
* Избранное - список избранных рецептов, с возможностью добавления ингредиентов рецепта в список покупок;
* Список покупок - список ингредиентов необходимых к приобретению для приготовления выбранных рецептов;
* Создание и редактирование рецепта.

<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="resorces"><h3>Ресурсы проекта</h3></a>
___
* Ресурс **users**: пользователи.
* Ресурс **followers**: сервис подписок.
* Ресурс **tags**: теги.
* Ресурс **favorites**: избранное.
* Ресурс **carts**: корзина покупок.
* Ресурс **ingredients**: ингредиенты.
* Ресурс **recipes**: рецепты.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.

Документация доступна по ссылкам [swagger](https://kkalogram.ru/swagger/) и [redoc](https://kkalogram.ru/redoc/).
<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="start"><h3>Как запустить проект:</h3></a>
___
Проведите подготовку своего сервера к запуску проекта.

* Подключитесь к своему удаленному серверу. 

* Обновите систему:
  
  ```angular2html
  sudo apt-get update && sudo apt-get -y install -f && sudo apt-get -y full-upgrade && sudo apt-get -y autoremove && sudo apt-get -y autoclean && sudo apt-get -y clean
  ```

* Установите [docker](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script):

  ```angular2html
  sudo apt install curl &&
  curl -fsSL https://test.docker.com -o test-docker.sh &&
  sudo sh test-docker.sh
  ```

* Проверьте, что Docker работает:

  ```angular2html
  sudo systemctl status docker
  ```

* Установите права пользователя для docker-compose:

  ```angular2html
  sudo chmod +x /usr/local/bin/docker-compose
  ```

* В корневой директории создайте папку kkalogram.

  ```angular2html
  mkdir kkalogram
  ```

Проведите подготовку проекта на локальном компьютере:

* Клонируйте репозиторий проекта на свой локальный компьютер по SSH ссылке:

  ```angular2html
  git@github.com:Konstantin-Leontyev/Kkalogram.git
  ```

* Создайте .env файл и заполните его согласно примеру в .env.example:

* Скопируйте файлы docker-compose.yml и .env в созданную ранее на удаленном сервере папку kkalogram.

  ```angular2html
  scp -i <path_to_your_SSH_key>/<your_SSH_key_name> docker-compose.yml .env \ 
    <your_username>@<your_server_ip>:<directory_path>/kkalogram/
  ```
  
* На удаленном сервере находясь в дирректории с проектом запустите его сборку:

  ```angular2html
  sudo docker compose -f docker-compose.yml up -d
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

Workflow состоит из слудующих четырёх шагов:

* Проверка кода на соответствие PEP8;
* Сборка и публикация бэкенда образа на DockerHub;
* Автоматический деплой на удаленный сервер;
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
