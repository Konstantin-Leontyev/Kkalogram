from http import HTTPStatus
from sqlite3 import IntegrityError

import pytest

from .utils import (check_for_bad_request, check_for_created,
                    check_for_page_not_found,
                    invalid_data_for_username_and_email_fields)


@pytest.mark.django_db(transaction=True)
class TestUserRegistration:
    URL_SIGNUP = '/api/users/'
    URL_TOKEN = '/api/auth/token/'

    def test_01_nodata_signup(self, client, django_user_model,
                              fields, url_signup):
        users_count = django_user_model.objects.count()

        response = client.post(path=url_signup)

        check_for_page_not_found(response=response, url_signup=url_signup)
        check_for_bad_request(response=response, url_signup=url_signup)

        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{url_signup}` '
            'без данных не создаёт нового пользователя.'
        )

        response_json = response.json()
        for field in fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в POST-запросе к `{url_signup}` не переданы '
                'необходимые данные, в ответе должна возвращаться информация '
                'об обязательных для заполнения полях.'
            )

    def test_02_blank_data_signup(self, client, django_user_model,
                                  fields, url_signup):
        blank_data = {
            'email': '',
            'first_name': '',
            'last_name': '',
            'username': '',
            'password': '',
        }
        users_count = django_user_model.objects.count()

        response = client.post(path=url_signup, data=blank_data)

        check_for_page_not_found(response=response, url_signup=url_signup)
        check_for_bad_request(response=response, url_signup=url_signup)

        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{url_signup}` с '
            'пустыми данными не создаёт нового пользователя.'
        )

        response_json = response.json()
        info = 'Это поле не может быть пустым.'
        for field in fields:
            response_json_field = response_json.get(field)
            assert (field in response_json
                    and isinstance(response_json_field, list)
                    and response_json_field[0] == info), (
                f'Если в  POST-запросе к `{url_signup}` переданы '
                'пустые данные, в ответе должно возвращаться уведомление: '
                f'{info}'
            )

    def test_03_invalid_data_signup(self, client, django_user_model,
                                    invalid_data, url_signup):
        users_count = django_user_model.objects.count()

        response = client.post(path=url_signup, data=invalid_data)

        check_for_page_not_found(response=response, url_signup=url_signup)
        check_for_bad_request(response=response, url_signup=url_signup)

        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{url_signup}` с '
            'некорректными данными не создаёт нового пользователя.'
        )

        response_json = response.json()
        invalid_fields = [
            'email',
            'username',
        ]
        for field in invalid_fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в  POST-запросе к `{url_signup}` переданы '
                'некорректные данные, в ответе должна возвращаться информация '
                'о неправильно заполненных полях.'
            )

    def test_04_no_required_data_signup(self, client, django_user_model,
                                        fields, valid_data, url_signup):
        users_count = django_user_model.objects.count()

        for field in fields:
            no_field_data = valid_data.copy()
            del no_field_data[field]

            response = client.post(path=url_signup, data=no_field_data)

            check_for_page_not_found(response=response, url_signup=url_signup)
            check_for_bad_request(response=response, url_signup=url_signup)

            assert users_count == django_user_model.objects.count(), (
                f'Проверьте, что POST-запрос к `{url_signup}` с '
                'некорректными данными не создаёт нового пользователя.'
            )
            assert users_count == django_user_model.objects.count(), (
                f'Проверьте, что POST-запрос к `{url_signup}`, '
                'не содержащий данных о `password`, '
                'не создаёт нового пользователя.'
            )

    def test_05_valid_data_user_signup(self, client, django_user_model,
                                       valid_data, url_signup):
        valid_response = {
            'id': 1,
            'email': 'valid@foodgram.ru',
            'first_name': 'valid_name',
            'last_name': 'valid_surname',
            'username': 'valid_username'
        }

        response = client.post(path=url_signup, data=valid_data)

        check_for_page_not_found(response=response, url_signup=url_signup)
        check_for_created(response=response, url_signup=url_signup)

        assert response.json() == valid_response, (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{url_signup}`, должен вернуть ответ, содержащий '
            'информацию о `id`, `email`, `first_name`, `last_name`, и '
            '`username` созданного пользователя.'
        )

        new_user = django_user_model.objects.filter(
            email=valid_data['email']
        )
        assert new_user.exists(), (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{url_signup}`, должен создать нового пользователя.'
        )
        new_user.delete()

    @pytest.mark.parametrize(
        'data, message', invalid_data_for_username_and_email_fields
    )
    def test_06_signup_fields_length_and_simbols_validation(self, client, data,
                                                            django_user_model,
                                                            message,
                                                            url_signup):
        request_method = 'POST'
        users_count = django_user_model.objects.count()
        response = client.post(path=url_signup, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            message[0].format(
                url=url_signup, request_method=request_method
            )
        )
        assert django_user_model.objects.count() == users_count, (
            f'Если в POST-запросе к эндпоинту `{url_signup}` '
            'значения полей не соответствуют ограничениям по длине или '
            'содержанию - новый пользователь не должен быть создан.'
        )

    def test_07_registration_me_username_restricted(self, client,
                                                    valid_data, url_signup):
        me_data = valid_data.copy()
        me_data['username'] = 'me'
        response = client.post(path=url_signup, data=me_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Если в POST-запросе, отправленном на эндпоинт '
            f'`{url_signup}`, значением поля `username` указано `me` - '
            'должен вернуться ответ со статусом 400.'
        )

    def test_08_registration_same_email_and_username_restricted(self, client,
                                                                valid_data,
                                                                url_signup):
        valid_email_2 = 'test_duplicate_2@yamdb.fake'
        valid_username_2 = 'valid_username_2'

        response = client.post(path=url_signup, data=valid_data)
        check_for_created(response=response, url_signup=url_signup)

        duplicate_email_data = valid_data.copy()
        duplicate_email_data['username'] = valid_username_2

        assert_msg = (
            f'Если POST-запрос, отправленный на эндпоинт `{url_signup}`, '
            'содержит `email` зарегистрированного пользователя и незанятый '
            '`username` - должен вернуться ответ со статусом 400.'
        )
        try:
            response = client.post(path=url_signup, data=duplicate_email_data)
        except IntegrityError:
            raise AssertionError(assert_msg)
        assert response.status_code == HTTPStatus.BAD_REQUEST, assert_msg

        duplicate_username_data = valid_data.copy()
        duplicate_username_data['email'] = valid_email_2

        assert_msg = (
            f'Если POST-запрос, отправленный на эндпоинт `{url_signup}`, '
            'содержит `username` зарегистрированного пользователя и '
            'несоответствующий ему `email` - должен вернуться ответ со '
            'статусом 400.'
        )
        try:
            response = client.post(
                path=url_signup, data=duplicate_username_data
            )
        except IntegrityError:
            raise AssertionError(assert_msg)
        assert response.status_code == HTTPStatus.BAD_REQUEST, assert_msg
