from http import HTTPStatus

invalid_data_for_username_and_email_fields = [
    (
        {
            'email': ('a' * 244) + '@yamdb.fake',
            'first_name': 'valid-firstname',
            'last_name': 'valid-lastname',
            'password': '1|2|3|a|A|',
            'username': 'valid-username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `email`: его содержимое не должно быть '
            'длиннее 254 символа.'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'first_name': 'valid_first_name',
            'last_name': 'valid-lastname',
            'password': '1|2|3|a|A|',
            'username': ('a' * 151)
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `username`: его содержимое не должно быть '
            'длиннее 150 символов.'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'first_name': ('a' * 151),
            'last_name': 'valid-lastname',
            'password': '1|2|3|a|A|',
            'username': 'valid-username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `first_name`: '
            'его содержимое не должно быть длиннее 150 символов.'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'first_name': 'valid-firstname',
            'last_name': ('a' * 151),
            'password': '1|2|3|a|A|',
            'username': 'valid-username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `last_name`: '
            'его содержимое не должно быть длиннее 150 символов.'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'first_name': 'valid-firstname',
            'last_name': 'valid-lastname',
            'password': '1|2|3|a|A|',
            'username': '|A|z|-|+|@|.|_|1|'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `username` проверяется на соответствие '
            'паттерну, указанному в спецификации: ^[\\w.@+-]+\\z'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'first_name': 'valid-firstname',
            'last_name': 'valid-lastname',
            'password': '1|2|3|a|',
            'username': 'valid-username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `password` проверяется на наличие '
            'хотя бы одной заглавной буквы.'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'first_name': 'valid-firstname',
            'last_name': 'valid-lastname',
            'password': '1|2|3|A|',
            'username': 'valid-username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `password` проверяется на наличие '
            'хотя бы одной строчной буквы.'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'first_name': 'valid-firstname',
            'last_name': 'valid-lastname',
            'password': 'a|b|c|d|',
            'username': 'valid-username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `password` проверяется на наличие '
            'хотя бы одной цифры.'
        ),)
    ),
    (
        {
            'email': 'valid-email@yamdb.fake',
            'first_name': 'valid-firstname',
            'last_name': 'valid-lastname',
            'password': '1234Abcd',
            'username': 'valid-username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `password` проверяется на наличие '
            r'хотя бы одного символа ()[]{}|\`~!@#$%^&*_-+=;:\'",<>./?.'
        ),)
    ),
]


def check_for_page_not_found(response, url_signup):
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'Эндпоинт `{url_signup}` не найден. Проверьте настройки '
        'в *urls.py*.'
    )


def check_for_bad_request(response, url_signup):
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Если POST-запрос, отправленный на эндпоинт `{url_signup}`, '
        'не содержит необходимых данных, должен вернуться ответ со '
        'статусом 400.'
    )


def check_for_created(response, url_signup):
    assert response.status_code == HTTPStatus.CREATED, (
        'POST-запрос с корректными данными, отправленный на эндпоинт '
        f'`{url_signup}`, должен вернуть ответ со статусом 201.'
    )
