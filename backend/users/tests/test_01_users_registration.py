from http import HTTPStatus
from sqlite3 import IntegrityError

import pytest

from .utils import (check_for_bad_request, check_for_created,
                    check_for_new_user_exists, check_for_page_found,
                    check_for_valid_response, invalid_data_for_required_fields)


@pytest.mark.django_db(transaction=True)
class TestUserRegistration:

    def test_01_empty_data_signup(self, client, django_user_model,
                                  fields, signup_url):
        users_count = django_user_model.objects.count()

        response = client.post(path=signup_url)

        check_for_page_found(response=response, url=signup_url)
        check_for_bad_request(response=response, url=signup_url)

        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{signup_url}` '
            'без данных не создаёт нового пользователя.'
        )

        response_json = response.json()
        for field in fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в POST-запросе к `{signup_url}` не переданы '
                'необходимые данные, в ответе должна возвращаться информация '
                'об обязательных для заполнения полях.'
            )

    def test_02_blank_data_signup(self, blank_data, client, django_user_model,
                                  fields, signup_url):
        users_count = django_user_model.objects.count()

        response = client.post(path=signup_url, data=blank_data)

        check_for_page_found(response=response, url=signup_url)
        check_for_bad_request(response=response, url=signup_url, msg_modifier='администратором ')

        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{signup_url}` с '
            'пустыми данными не создаёт нового пользователя.'
        )

        response_json = response.json()
        info = 'Это поле не может быть пустым.'
        for field in fields:
            response_json_field = response_json.get(field)
            assert (field in response_json
                    and isinstance(response_json_field, list)
                    and response_json_field[0] == info), (
                f'Если в  POST-запросе к `{signup_url}` переданы '
                'пустые данные, в ответе должно возвращаться уведомление: '
                f'{info}'
            )

    def test_03_invalid_fields_in_response(self, client, django_user_model,
                                           invalid_data, signup_url):
        users_count = django_user_model.objects.count()

        response = client.post(path=signup_url, data=invalid_data)

        check_for_page_found(response=response, url=signup_url)
        check_for_bad_request(response=response, url=signup_url)

        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{signup_url}` с '
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
                f'Если в  POST-запросе к `{signup_url}` переданы '
                'некорректные данные, в ответе должна возвращаться информация '
                'о неправильно заполненных полях.'
            )

    def test_04_no_required_data_signup(self, client, django_user_model,
                                        fields, signup_url, valid_data):
        users_count = django_user_model.objects.count()

        for field in fields:
            no_field_data = valid_data.copy()
            del no_field_data[field]

            response = client.post(path=signup_url, data=no_field_data)

            check_for_page_found(response=response, url=signup_url)
            check_for_bad_request(response=response, url=signup_url)

            assert users_count == django_user_model.objects.count(), (
                f'Проверьте, что POST-запрос к `{signup_url}` с '
                'некорректными данными не создаёт нового пользователя.'
            )
            assert users_count == django_user_model.objects.count(), (
                f'Проверьте, что POST-запрос к `{signup_url}`, '
                'не содержащий данных о `password`, '
                'не создаёт нового пользователя.'
            )

    def test_05_valid_data_user_signup(self, client, django_user_model,
                                       valid_data, signup_url):
        valid_response = {
            'id': 1,
            'email': 'valid_email@foodgram.ru',
            'first_name': 'valid_name',
            'last_name': 'valid_surname',
            'username': 'valid_username'
        }
        response = client.post(path=signup_url, data=valid_data)

        check_for_page_found(response=response, url=signup_url)
        check_for_created(response=response, url=signup_url)

        response_json = response.json()
        check_for_valid_response(response=response_json,
                                 valid_response=valid_response, url=signup_url)

        new_user = django_user_model.objects.filter(
            email=valid_data['email']
        )
        check_for_new_user_exists(new_user=new_user, url=signup_url)
        new_user.delete()

    @pytest.mark.parametrize(
        'data, message', invalid_data_for_required_fields
    )
    def test_06_invalid_data_user_signup(self, client, data, django_user_model,
                                         message, signup_url):
        request_method = 'POST'
        users_count = django_user_model.objects.count()
        response = client.post(path=signup_url, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            message[0].format(
                url=signup_url, request_method=request_method
            )
        )
        assert django_user_model.objects.count() == users_count, (
            f'Если в POST-запросе к эндпоинту `{signup_url}` '
            'значения полей не соответствуют ограничениям по длине или '
            'содержанию - новый пользователь не должен быть создан.'
        )

    def test_07_registration_me_username_restricted(self, client,
                                                    signup_url, valid_data, ):
        me_data = valid_data.copy()
        me_data['username'] = 'me'
        response = client.post(path=signup_url, data=me_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Если в POST-запросе, отправленном на эндпоинт '
            f'`{signup_url}`, значением поля `username` указано `me` - '
            'должен вернуться ответ со статусом 400.'
        )

    def test_08_registration_same_email_and_username_restricted(self, client,
                                                                signup_url,
                                                                valid_data):
        valid_email_2 = 'test_duplicate_2@yamdb.fake'
        valid_username_2 = 'valid_username_2'

        response = client.post(path=signup_url, data=valid_data)
        check_for_created(response=response, url=signup_url)

        duplicate_email_data = valid_data.copy()
        duplicate_email_data['username'] = valid_username_2

        assert_msg = (
            f'Если POST-запрос, отправленный на эндпоинт `{signup_url}`, '
            'содержит `email` зарегистрированного пользователя и незанятый '
            '`username` - должен вернуться ответ со статусом 400.'
        )
        try:
            response = client.post(path=signup_url, data=duplicate_email_data)
        except IntegrityError:
            raise AssertionError(assert_msg)
        assert response.status_code == HTTPStatus.BAD_REQUEST, assert_msg

        duplicate_username_data = valid_data.copy()
        duplicate_username_data['email'] = valid_email_2

        assert_msg = (
            f'Если POST-запрос, отправленный на эндпоинт `{signup_url}`, '
            'содержит `username` зарегистрированного пользователя и '
            'несоответствующий ему `email` - должен вернуться ответ со '
            'статусом 400.'
        )
        try:
            response = client.post(
                path=signup_url, data=duplicate_username_data
            )
        except IntegrityError:
            raise AssertionError(assert_msg)
        assert response.status_code == HTTPStatus.BAD_REQUEST, assert_msg
