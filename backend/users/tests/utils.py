from http import HTTPStatus

invalid_data_for_required_fields = [
    (
        {
            'email': ('a' * 244) + '@foodgram.ru',
            'first_name': 'valid_name',
            'last_name': 'valid_surname',
            'password': '1|2|3|a|A|',
            'username': 'valid_username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `email`: его содержимое не должно быть '
            'длиннее 254 символа.'
        ),
         (
            'Проверьте, что при обработке {request_method}-запроса '
            'администратора к `{url}` '
            'проверяется длина поля `email`: его содержимое не должно быть '
            'длиннее 254 символа.'
         )
        )
    ),
    (
        {
            'email': 'valid_email@yfoodgram.ru',
            'first_name': 'valid_first_name',
            'last_name': 'valid_lastname',
            'password': '1|2|3|a|A|',
            'username': ('a' * 151)
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `username`: его содержимое не должно быть '
            'длиннее 150 символов.'
        ),
         (
            'Проверьте, что при обработке {request_method}-запроса '
            'администратора к `{url}` '
            'проверяется длина поля `username`: его содержимое не должно быть '
            'длиннее 150 символов.'
         )
        )
    ),
    (
        {
            'email': 'valid_email@foodgram.ru',
            'first_name': ('a' * 151),
            'last_name': 'valid_surname',
            'password': '1|2|3|a|A|',
            'username': 'valid_username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `first_name`: '
            'его содержимое не должно быть длиннее 150 символов.'
        ),
         (
            'Проверьте, что при обработке {request_method}-запроса '
            'администратора к `{url}` '
            'проверяется длина поля `first_name`: '
            'его содержимое не должно быть длиннее 150 символов.'
         )
        )
    ),
    (
        {
            'email': 'valid_email@foodgram.ru',
            'first_name': 'valid_firstname',
            'last_name': ('a' * 151),
            'password': '1|2|3|a|A|',
            'username': 'valid_username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'проверяется длина поля `last_name`: '
            'его содержимое не должно быть длиннее 150 символов.'
        ),
         (
            'Проверьте, что при обработке {request_method}-запроса '
            'администратора к `{url}` '
            'проверяется длина поля `last_name`: '
            'его содержимое не должно быть длиннее 150 символов.'
         )

        )
    ),
    (
        {
            'email': 'valid_email@foodgram.ru',
            'first_name': 'valid_firstname',
            'last_name': 'valid_lastname',
            'password': '1|2|3|a|A|',
            'username': '|A|z|-|+|@|.|_|1|'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `username` проверяется на соответствие '
            'паттерну, указанному в спецификации: ^[\\w.@+-]+\\z'
        ),
         (
            'Проверьте, что при обработке {request_method}-запроса '
            'администратора к `{url}` '
            'содержание поля `username` проверяется на соответствие '
            'паттерну, указанному в спецификации: ^[\\w.@+-]+\\z'
         )
        )
    ),
    (
        {
            'email': 'valid_email@foodgram.ru',
            'first_name': 'valid_firstname',
            'last_name': 'valid_lastname',
            'password': '1|2|3|a|',
            'username': 'valid_username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `password` проверяется на наличие '
            'хотя бы одной заглавной буквы.'
        ),
         (
            'Проверьте, что при обработке {request_method}-запроса '
            'администратора к `{url}` '
            'содержание поля `password` проверяется на наличие '
            'хотя бы одной заглавной буквы.'
         )
        )
    ),
    (
        {
            'email': 'valid_email@yamdb.fake',
            'first_name': 'valid_name',
            'last_name': 'valid_surname',
            'password': '1|2|3|A|',
            'username': 'valid_username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `password` проверяется на наличие '
            'хотя бы одной строчной буквы.'
        ),
         (
            'Проверьте, что при обработке {request_method}-запроса '
            'администратора к `{url}` '
            'содержание поля `password` проверяется на наличие '
            'хотя бы одной строчной буквы.'
         )
        )
    ),
    (
        {
            'email': 'valid_email@foodgram.ru',
            'first_name': 'valid_name',
            'last_name': 'valid_surname',
            'password': 'a|b|c|d|',
            'username': 'valid_username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `password` проверяется на наличие '
            'хотя бы одной цифры.'
        ),
         (
            'Проверьте, что при обработке {request_method}-запроса '
            'администратора к `{url}` '
            'содержание поля `password` проверяется на наличие '
            'хотя бы одной цифры.'
         )
        )
    ),
    (
        {
            'email': 'valid_email@yamdb.fake',
            'first_name': 'valid_name',
            'last_name': 'valid_surname',
            'password': '1234Abcd',
            'username': 'valid_username'
        },
        ((
            'Проверьте, что при обработке {request_method}-запроса к `{url}` '
            'содержание поля `password` проверяется на наличие '
            r'хотя бы одного символа ()[]{}|\`~!@#$%^&*_-+=;:\'",<>./?.'
        ),
         (
            'Проверьте, что при обработке {request_method}-запроса '
            'администратора к `{url}` '
            'содержание поля `password` проверяется на наличие '
            r'хотя бы одного символа ()[]{}|\`~!@#$%^&*_-+=;:\'",<>./?.'
         )
        )
    ),
]


def check_for_page_found(response, url, username=None, search=False):
    if username:
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{url}'
            '{username}/` не найден. Проверьте настройки в *urls.py*.'
        )
    if search:
        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{url}'
            '?search={username}` не найден. Проверьте настройки в *urls.py*.'
        )
    assert response.status_code != HTTPStatus.NOT_FOUND, (
        f'Эндпоинт `{url}` не найден. Проверьте настройки '
        'в *urls.py*.'
    )


def check_for_bad_request(response, url, msg_modifier=''):
    assert response.status_code == HTTPStatus.BAD_REQUEST, (
        f'Если POST-запрос, отправленный {msg_modifier}на эндпоинт `{url}`, '
        'не содержит необходимых данных, должен вернуться ответ со '
        'статусом 400.'
    )


def check_for_created(response, url, msg_modifier=''):
    assert response.status_code == HTTPStatus.CREATED, (
        f'POST-запрос {msg_modifier}с корректными данными, отправленный на эндпоинт '
        f'`{url}`, должен вернуть ответ со статусом 201.'
    )


def check_for_valid_response(response, valid_response, url, msg_modifier=''):
    assert response == valid_response, (
        f'POST-запрос {msg_modifier}с корректными данными, отправленный на эндпоинт '
        f'`{url}`, должен вернуть ответ, содержащий '
        'информацию о `id`, `email`, `first_name`, `last_name`, и '
        '`username` созданного пользователя.'
    )


def check_for_token_request(response, url, msg_modifier=''):
    assert response.status_code == HTTPStatus.OK, (
        f'Проверьте, что GET-запрос {msg_modifier}к `{url}` с токеном '
        'авторизации возвращает ответ со статусом 200.'
    )


def check_for_no_token_request(response, url, msg_modifier=''):
    assert response.status_code == HTTPStatus.UNAUTHORIZED, (
        f'Проверьте, что GET-запрос {msg_modifier}к `{url}` без токена '
        'авторизации возвращается ответ со статусом 401.'
    )


def check_for_new_user_exists(new_user, url, msg_modifier=''):
    assert new_user.exists(), (
        f'POST-запрос {msg_modifier}с корректными данными, '
        f'отправленный на эндпоинт `{url}`, '
        'должен создать нового пользователя.'
    )


def check_pagination(expected_count, response, url, post_data=''):
    expected_keys = ('count', 'next', 'previous', 'results')
    for key in expected_keys:
        assert key in response, (
            f'Проверьте, что для эндпоинта `{url}` настроена '
            f'пагинация и ответ на GET-запрос содержит ключ {key}.'
        )
    assert response['count'] == expected_count, (
        f'Проверьте, что для эндпоинта `{url}` настроена '
        f'пагинация. Сейчас ключ `count` содержит некорректное значение.'
    )
    assert isinstance(response['results'], list), (
        f'Проверьте, что для эндпоинта `{url}` настроена '
        'пагинация. Значением ключа `results` должен быть список.'
    )
    assert len(response['results']) == expected_count, (
        f'Проверьте, что для эндпоинта `{url}` настроена пагинация. Сейчас '
        'ключ `results` содержит некорректное количество элементов.'
    )
    if post_data:
        assert post_data in response['results'], (
            f'Проверьте, что для эндпоинта `{url}` настроена пагинация. '
            'Значение параметра `results` отсутствует или содержит '
            'некорректную информацию о существующем объекте.'
        )
