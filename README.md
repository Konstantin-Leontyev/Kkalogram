# Проект Foodgram

### Технологии
![example workflow](https://github.com/Konstantin-Leontyev/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)  
  
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

Проект YaMDb собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. 

Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка». Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Жуки» и вторая сюита Баха. Список категорий может быть расширен (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).

Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»).

Добавлять произведения, категории и жанры может только администратор.

Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

Пользователи могут оставлять комментарии к отзывам.

Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="resorces"><h3>Ресурсы проекта</h3></a>
___
* Ресурс **users**: пользователи.
* Ресурс **followers**: сервис подписок.
* Ресурс **tags**: теги
* Ресурс **favorites**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
* Ресурс **carts**: корзина покупок.
* Ресурс **ingredients**: ингредиенты.
* Ресурс **recipes**: рецепты.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.

Документация доступна по ссылке http://127.0.0.1:8000/redoc/ после запуска проекта.

<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="start"><h3>Как запустить проект:</h3></a>
___

Клонируйте репозиторий проекта на свой локальный компьютер по SSH ссылке:

```angular2html
git@github.com:Konstantin-Leontyev/foodgram-project-react.git
```

Подключитесь к своему удаленному серверу:

```angular2html
ssh <server user>@<server IP>
```

Обновите систему:

```angular2html
sudo apt-get update && sudo apt-get -y install -f && sudo apt-get -y full-upgrade && sudo apt-get -y autoremove && sudo apt-get -y autoclean && sudo apt-get -y clean
```

Установите docker на сервер:
```angular2html
sudo apt install docker.io 
```

Установите docker-compose на сервер:

```angular2html
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
```

Установите права пользователя для docker-compose:
```angular2html
sudo chmod +x /usr/local/bin/docker-compose
```
Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP:

Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер:
```angular2html
scp docker-compose.yml <username>@<host>:/home/<username>/docker-compose.yml
```
```angular2html
scp nginx.conf <username>@<host>:/home/<username>/nginx.conf
```

Создайте .env файл и заполните его согласно примеру .env.example:
```angular2html
# Переменные для Django-проекта:
ALLOWED_HOSTS=xxx.xxx.xxx.xxx 127.0.0.1 localhost https://yourdomain
DEBUG=False
SECRET_KEY=key from setting

# Переменные для PostgreSQL:
POSTGRES_DB=postgres_db_name
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=project_db_user_password

# Переменные для Doker контейнера:
DB_HOST=имя контейнера базы данных или 127.0.0.1
DB_PORT=5432

# Переменные для авто тестов:
PROJECT_DIR_NAME=backend
```
Для работы с Workflow добавьте в Secrets GitHub переменные окружения:

```
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>

DOCKER_PASSWORD=<пароль от DockerHub>
DOCKER_USERNAME=<имя пользователя>

SECRET_KEY=<секретный ключ проекта django>

USER=<username для подключения к серверу>
HOST=<IP сервера>
PASSPHRASE=<пароль для сервера, если он установлен>
SSH_KEY=<ваш SSH ключ (для получения команда: cat ~/.ssh/id_rsa)>

TELEGRAM_TO=<ID чата, в который придет сообщение>
TELEGRAM_TOKEN=<токен вашего бота>
```

Workflow состоит из трёх шагов:

Проверка кода на соответствие PEP8
Сборка и публикация образа бекенда на DockerHub.
Автоматический деплой на удаленный сервер.
Отправка уведомления в телеграм-чат.

На удаленном сервере соберите docker-compose:
```angular2html
sudo docker-compose up -d --build
```

После успешной сборки на сервере выполните команды (только после первого деплоя):
Соберите статические файлы:
sudo docker-compose exec backend python manage.py collectstatic --noinput
Примените миграции:
sudo docker-compose exec backend python manage.py migrate --noinput
Загрузите ингридиенты в базу данных (необязательно):
Если файл не указывать, по умолчанию выберется ingredients.json
sudo docker-compose exec backend python manage.py load_ingredients <Название файла из директории data>
Создать суперпользователя Django:
sudo docker-compose exec backend python manage.py createsuperuser
Проект будет доступен по вашему IP


<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="command"><h3>Знакомство с проектом</h3></a>
___

Для ознакомления с функционалом проекта можно:

Создать и заполнить тестовую базу данных.
```
python3 manage.py import_csv
```

<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="team"><h3>Команда проекта</h3></a>
___

[![Gmail Badge](https://img.shields.io/badge/-K.A.Leontyev@gmail.com-c14438?style=flat&logo=Gmail&logoColor=white&link=mailto:K.A.Leontyev@gmail.com)](mailto:K.A.Leontyev@gmail.com)<p align='left'>


