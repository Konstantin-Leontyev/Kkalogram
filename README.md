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
* Ресурс **auth**: аутентификация.
* Ресурс **users**: пользователи.
* Ресурс **titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
* Ресурс **categories**: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
* Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
* Ресурс **reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.
* Ресурс **comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, когда это необходимо.

Документация доступна  по ссылке http://127.0.0.1:8000/redoc/ после запуска проекта.

<p align="right">(<a href="#description">Вернуться в начало</a>)</p>

<a name="start"><h3>Как запустить проект:</h3></a>
___

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Konstantin-Leontyev/api_yamdb.git
```

Создать и активировать виртуальное окружение:

```
python3 -m venv .venv
```

* Если у вас Linux/macOS

    ```
    source .venv/bin/activate
    ```

* Если у вас windows

    ```
    source .venv/scripts/activate
    ```

Обновить версию инсталлятора pip
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:


```
pip install -r requirements.txt
```

Дождаться завершения установки. Выполнить миграции:
```
cd api_yamdb/
```

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
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


