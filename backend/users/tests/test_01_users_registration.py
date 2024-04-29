from http import HTTPStatus
from sqlite3 import IntegrityError

import django
import pytest

from .utils import invalid_data_for_username_and_email_fields

django.setup()


@pytest.mark.django_db(transaction=True)
class TestUserRegistration:
    URL_SIGNUP = '/api/users/'
    URL_TOKEN = '/api/auth/token/'

    fields = [
        'email',
        'first_name',
        'last_name',
        'password',
        'username'
    ]

    valid_data = {
        'email': 'valid@yamdb.fake',
        'username': 'valid_username',
        'last_name': 'username',
        'first_name': 'valid',
        'password': '1dE(45wef'
    }

    invalid_data = {
        'email': 'invalid_email',
        'first_name': 'valid_name',
        'last_name': 'valid_surname',
        'username': 'invalid username',
        'password': 'invalid_password'
    }

    def test_01_nodata_signup(self, client):
        response = client.post(self.URL_SIGNUP)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.URL_SIGNUP}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос, отправленный на эндпоинт `{self.URL_SIGNUP}`, '
            'не содержит необходимых данных, должен вернуться ответ со '
            'статусом 400.'
        )

        response_json = response.json()
        unused_fields = [
            'email',
            'first_name',
            'last_name',
            'password',
            'username'
        ]
        for field in unused_fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в POST-запросе к `{self.URL_SIGNUP}` не переданы '
                'необходимые данные, в ответе должна возвращаться информация '
                'об обязательных для заполнения полях.'
            )

    def test_02_blank_data_signup(self, client, django_user_model):
        blank_data = {
            'email': '',
            'first_name': '',
            'last_name': '',
            'username': '',
            'password': '',
        }
        users_count = django_user_model.objects.count()

        response = client.post(self.URL_SIGNUP, data=blank_data)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.URL_SIGNUP}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос к эндпоинту `{self.URL_SIGNUP}` содержит '
            'некорректные данные, должен вернуться ответ со статусом 400.'
        )
        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{self.URL_SIGNUP}` с '
            'пустыми данными не создаёт нового пользователя.'
        )

        response_json = response.json()

        info = 'Это поле не может быть пустым.'
        for field in self.fields:
            response_json_field = response_json.get(field)
            assert (field in response_json
                    and isinstance(response_json_field, list)
                    and response_json_field[0] == info), (
                f'Если в  POST-запросе к `{self.URL_SIGNUP}` переданы '
                'пустые данные, в ответе должно возвращаться уведомление: '
                f'{info}'
            )

    def test_03_invalid_data_signup(self, client, django_user_model):
        users_count = django_user_model.objects.count()

        response = client.post(self.URL_SIGNUP, data=self.invalid_data)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.URL_SIGNUP}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос к эндпоинту `{self.URL_SIGNUP}` содержит '
            'некорректные данные, должен вернуться ответ со статусом 400.'
        )
        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос к `{self.URL_SIGNUP}` с '
            'некорректными данными не создаёт нового пользователя.'
        )

        response_json = response.json()
        invalid_fields = [
            'email',
            # 'password',
            'username'
        ]
        for field in invalid_fields:
            assert (field in response_json
                    and isinstance(response_json.get(field), list)), (
                f'Если в  POST-запросе к `{self.URL_SIGNUP}` переданы '
                'некорректные данные, в ответе должна возвращаться информация '
                'о неправильно заполненных полях.'
            )

    def test_04_no_required_data_signup(self, client, django_user_model):
        users_count = django_user_model.objects.count()

        for field in self.fields:
            no_field_data = self.valid_data.copy()
            del no_field_data[field]

            response = client.post(self.URL_SIGNUP, data=no_field_data)

            assert response.status_code != HTTPStatus.NOT_FOUND, (
                f'Эндпоинт `{self.URL_SIGNUP}` не найден. Проверьте настройки '
                'в *urls.py*.'
            )
            assert response.status_code == HTTPStatus.BAD_REQUEST, (
                f'Если POST-запрос к эндпоинту `{self.URL_SIGNUP}` содержит '
                'некорректные данные, должен вернуться ответ со статусом 400.'
            )
            assert users_count == django_user_model.objects.count(), (
                f'Проверьте, что POST-запрос к `{self.URL_SIGNUP}` с '
                'некорректными данными не создаёт нового пользователя.'
            )
            assert users_count == django_user_model.objects.count(), (
                f'Проверьте, что POST-запрос к `{self.URL_SIGNUP}`, '
                'не содержащий данных о `password`, '
                'не создаёт нового пользователя.'
            )

    def test_05_valid_data_user_signup(self, client, django_user_model):
        valid_response = {
            'id': 1,
            'email': 'valid@yamdb.fake',
            'username': 'valid_username',
            'last_name': 'username',
            'first_name': 'valid'
        }

        response = client.post(self.URL_SIGNUP, data=self.valid_data)

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            f'Эндпоинт `{self.URL_SIGNUP}` не найден. Проверьте настройки '
            'в *urls.py*.'
        )
        assert response.status_code == HTTPStatus.CREATED, (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.URL_SIGNUP}`, должен вернуть ответ со статусом 201.'
        )
        assert response.json() == valid_response, (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.URL_SIGNUP}`, должен вернуть ответ, содержащий '
            'информацию о `username` и `email` созданного пользователя.'
        )

        new_user = django_user_model.objects.filter(
            email=self.valid_data['email']
        )
        assert new_user.exists(), (
            'POST-запрос с корректными данными, отправленный на эндпоинт '
            f'`{self.URL_SIGNUP}`, должен создать нового пользователя.'
        )
        new_user.delete()

    @pytest.mark.parametrize(
        'data,message', invalid_data_for_username_and_email_fields
    )
    def test_06_signup_fields_length_and_simbols_validation(self, client,
                                                            data, message,
                                                            django_user_model):
        request_method = 'POST'
        users_count = django_user_model.objects.count()
        response = client.post(self.URL_SIGNUP, data=data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            message[0].format(
                url=self.URL_SIGNUP, request_method=request_method
            )
        )
        assert django_user_model.objects.count() == users_count, (
            f'Если в POST-запросе к эндпоинту `{self.URL_SIGNUP}` '
            'значения полей не соответствуют ограничениям по длине или '
            'содержанию - новый пользователь не должен быть создан.'
        )

    def test_07_registration_me_username_restricted(self, client):
        me_data = self.valid_data.copy()
        me_data['username'] = 'me'
        response = client.post(self.URL_SIGNUP, data=me_data)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Если в POST-запросе, отправленном на эндпоинт '
            f'`{self.URL_SIGNUP}`, значением поля `username` указано `me` - '
            'должен вернуться ответ со статусом 400.'
        )

    def test_08_registration_same_email_and_username_restricted(self, client):
        valid_email_2 = 'test_duplicate_2@yamdb.fake'
        valid_username_2 = 'valid_username_2'

        response = client.post(self.URL_SIGNUP, data=self.valid_data)
        assert response.status_code == HTTPStatus.CREATED, (
            f'Проверьте, что POST-запрос к `{self.URL_SIGNUP}` с корректными '
            'возвращает статус-код 201.'
        )

        duplicate_email_data = self.valid_data.copy()
        duplicate_email_data['username'] = valid_username_2

        assert_msg = (
            f'Если POST-запрос, отправленный на эндпоинт `{self.URL_SIGNUP}`, '
            'содержит `email` зарегистрированного пользователя и незанятый '
            '`username` - должен вернуться ответ со статусом 400.'
        )
        try:
            response = client.post(self.URL_SIGNUP, data=duplicate_email_data)
        except IntegrityError:
            raise AssertionError(assert_msg)
        assert response.status_code == HTTPStatus.BAD_REQUEST, assert_msg

        duplicate_username_data = self.valid_data.copy()
        duplicate_username_data['email'] = valid_email_2

        assert_msg = (
            f'Если POST-запрос, отправленный на эндпоинт `{self.URL_SIGNUP}`, '
            'содержит `username` зарегистрированного пользователя и '
            'несоответствующий ему `email` - должен вернуться ответ со '
            'статусом 400.'
        )
        try:
            response = client.post(
                self.URL_SIGNUP, data=duplicate_username_data
            )
        except IntegrityError:
            raise AssertionError(assert_msg)
        assert response.status_code == HTTPStatus.BAD_REQUEST, assert_msg
