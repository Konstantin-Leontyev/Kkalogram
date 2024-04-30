from http import HTTPStatus

import pytest

from .utils import (check_for_bad_request, check_for_created,
                    check_for_page_found,
                    check_for_no_token_request,
                    invalid_data_for_required_fields, check_pagination, check_for_token_request)
#
# from tests.utils import (
#     check_pagination, invalid_data_for_user_patch_and_creation
# )
#
#
@pytest.mark.django_db(transaction=True)
class Test02UserAPI:
#
#     USERS_URL = '/api/v1/users/'
#     USERS_ME_URL = '/api/v1/users/me/'
#     VALID_DATA_FOR_USER_CREATION = [
#         (
#             {
#                 'username': 'TestUser_2',
#                 'role': 'user',
#                 'email': 'testuser2@yamdb.fake'
#             },
#             ''
#         ),
#         (
#             {
#                 'username': 'TestUser_3',
#                 'email': 'testuser3@yamdb.fake'
#             },
#             'без указания роли нового пользователя '
#         )
#     ]
#     PATCH_DATA = {
#         'first_name': 'New User Firstname',
#         'last_name': 'New User Lastname',
#         'bio': 'new user bio'
#     }
#
    # TODO use logic for models authenticated tests
    # def test_01_users_not_authenticated(self, client, url_signup):
    #     response = client.get(path=url_signup)
    #
    #     check_for_page_not_found(response=response, url_signup=url_signup)
    #     check_for_no_token_request(response=response, url_signup=url_signup)

    # TODO use logic for models separate permission tests
    # def test_04_01_users_get_admin_only(self, user_client, moderator_client):
    #     for client in (user_client, moderator_client):
    #         response = client.get(self.USERS_URL)
    #         assert response.status_code != HTTPStatus.NOT_FOUND, (
    #             f'Эндпоинт `{self.USERS_URL}` не найден. Проверьте настройки '
    #             'в *urls.py*.'
    #         )
    #         assert response.status_code == HTTPStatus.FORBIDDEN, (
    #             f'Проверьте, что GET-запрос к `{self.USERS_URL}` от '
    #             'пользователя, не являющегося администратором, возвращает '
    #             'ответ со статусом 403.'
    #         )


    def test_01_users_username_not_authenticated(self, admin, client, users_url):
        response = client.get(path=f'{users_url}{admin.username}/')

        check_for_page_found(response=response, url=users_url,
                             username=admin.username)
        check_for_no_token_request(response=response, url=users_url)

    def test_02_users_me_not_authenticated(self, client, users_me_url):
        response = client.get(path=users_me_url)

        check_for_page_found(response=response, url=users_me_url)
        check_for_no_token_request(response=response, url=users_me_url)

    def test_03_users_get_admin(self, admin, admin_client, users_url):
        response = admin_client.get(path=users_url)

        check_for_page_found(response=response, url=users_url)
        check_for_token_request(response=response, url=users_url)

        data = response.json()
        admin_data = {
            'email': admin.email,
            'first_name': admin.first_name,
            'id': admin.id,
            'last_name': admin.last_name,
            'username': admin.username
        }
        check_pagination(expected_count=1, response=data,
                         url=users_url, post_data=admin_data)

    # TODO в зависимости от прав проверить на user, admin, superuser
    # очевидно в apiyamb доступ к поиску был только у администратора
    def test_04_users_get_search(self, admin, admin_client,
                                 django_user_model, user, users_url):
        search_url = f'{users_url}?search={admin.username}'
        response = admin_client.get(path=search_url)

        check_for_page_found(response=response, url=search_url, search=True)

        response_json = response.json()
        assert ('results' in response_json
                and isinstance(response_json.get('results'), list)), (
            f'Проверьте, что GET-запрос к `{users_url}'
            '?search={username}` возвращает результаты поиска по значению '
            'ключа `results` в виде списка.'
        )
        # users_count = (
        #     django_user_model.objects.filter(username=admin.username).count()
        # )
        # print(search_url)
        # print('response', response_json)
        # print('user_cont', users_count)
        # assert len(response_json['results']) == users_count, (
        #     f'Проверьте, что GET-запрос к `{users_url}'
        #     '?search={username}` возвращает данные только тех пользователей, '
        #     '`username` которых удовлетворяет условию поиска.'
        # )
#         admin_as_dict = {
#             'username': admin.username,
#             'email': admin.email,
#             'role': admin.role,
#             'first_name': admin.first_name,
#             'last_name': admin.last_name,
#             'bio': admin.bio
#         }
#         assert response_json['results'] == [admin_as_dict], (
#             f'Проверьте, что ответ на GET-запрос к `{self.USERS_URL}'
#             '?search={username}` содержит полный перечень данных '
#             'пользователя. Ответ должен содержать следующие ключи с '
#             f'корректными данными: {", ".join(admin_as_dict.keys())}.'
#         )
#

    def test_05_users_post_admin_empty_data(self, admin, admin_client, users_url):
        response = admin_client.post(users_url)

        check_for_page_found(response=response, url=users_url)
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            f'Если POST-запрос администратора к `{users_url}` '
            'не содержит необходимых данных - должен вернуться ответ со '
            'статусом 400.'
        )

    def test_06_users_post_admin_blank_data(self, admin_client, blank_data,
                                            django_user_model, fields, users_url):
        users_count = django_user_model.objects.count()

        response = admin_client.post(path=users_url, data=blank_data)

        check_for_page_found(response=response, url=users_url)
        check_for_bad_request(response=response, url=users_url)

        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос администратора к `{users_url}` с '
            'пустыми данными не создаёт нового пользователя.'
        )

        response_json = response.json()
        info = 'Это поле не может быть пустым.'
        for field in fields:
            response_json_field = response_json.get(field)
            assert (field in response_json
                    and isinstance(response_json_field, list)
                    and response_json_field[0] == info), (
                f'Если в  POST-запросе администратора к `{users_url}` переданы '
                'пустые данные, в ответе должно возвращаться уведомление: '
                f'{info}'
            )

    def test_07_users_post_admin_invalid_fields_in_response(
            self, admin_client, django_user_model, invalid_data, users_url):
        users_count = django_user_model.objects.count()

        response = admin_client.post(path=users_url, data=invalid_data)

        check_for_page_found(response=response, url=users_url)
        check_for_bad_request(response=response, url=users_url)

        assert users_count == django_user_model.objects.count(), (
            f'Проверьте, что POST-запрос администратора к `{users_url}` с '
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
                f'Если в  POST-запросе администратора к `{users_url}` переданы '
                'некорректные данные, в ответе должна возвращаться информация '
                'о неправильно заполненных полях.'
            )

    def test_08_users_post_admin_no_required_data(self, admin_client,
                                                  django_user_model,
                                                  fields, valid_data,
                                                  users_url):
        users_count = django_user_model.objects.count()

        for field in fields:
            no_field_data = valid_data.copy()
            del no_field_data[field]

            response = admin_client.post(path=users_url, data=no_field_data)

            check_for_page_found(response=response, url=users_url)
            check_for_bad_request(response=response, url=users_url)

            assert users_count == django_user_model.objects.count(), (
                f'Проверьте, что POST-запрос к `{users_url}` с '
                'некорректными данными не создаёт нового пользователя.'
            )
            assert users_count == django_user_model.objects.count(), (
                f'Проверьте, что POST-запрос к `{users_url}`, '
                'не содержащий данных о `password`, '
                'не создаёт нового пользователя.'
            )

    @pytest.mark.parametrize(
        'data, message', invalid_data_for_required_fields
    )
    def test_09_users_post_admin_invalid_data(self, admin_client, data,
                                              django_user_model,
                                              message,
                                              users_url):
        users_count = django_user_model.objects.count()

        response = admin_client.post(path=users_url, data=data)

        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            message[1].format(
                url=users_url, request_method='POST'
            )
        )
        assert django_user_model.objects.count() == users_count, (
            f'Если в POST-запросе администратора к эндпоинту `{users_url}` '
            'значения полей не соответствуют ограничениям по длине или '
            'содержанию - новый пользователь не должен быть создан.'
        )




#
#
#     @pytest.mark.parametrize('data,msg_modifier', VALID_DATA_FOR_USER_CREATION)
#     def test_05_02_users_post_admin_user_creation(self, admin_client,
#                                                   data, msg_modifier,
#                                                   django_user_model):
#         response = admin_client.post(self.USERS_URL, data=data)
#         assert response.status_code == HTTPStatus.CREATED, (
#             f'Если POST-запрос администратора к `{self.USERS_URL}` содержит '
#             f'корректные данные {msg_modifier}- должен вернуться ответ со '
#             'статусом 201.'
#         )
#         new_user = django_user_model.objects.filter(email=data['email'])
#         assert new_user.exists(), (
#             'Если POST-запрос администратора, отправленный к '
#             f'`{self.USERS_URL}`, содержит корректные данные {msg_modifier}- '
#             'должен быть создан новый пользователь.'
#         )
#         if msg_modifier:
#             assert new_user.first().role == 'user', (
#                 'Когда администратор создаёт пользователя через POST-запрос к '
#                 f'`{self.USERS_URL}` и не указывает роль для нового '
#                 'пользователя - пользователю должна присваиваться роль `user`.'
#             )
#
#     def test_05_03_users_post_response_has_data(self, admin_client):
#         data = {
#             'first_name': 'First Name',
#             'last_name': 'Last Name',
#             'username': 'test_username',
#             'bio': 'test bio',
#             'role': 'moderator',
#             'email': 'testmoder2@yamdb.fake'
#         }
#         response = admin_client.post(self.USERS_URL, data=data)
#         assert response.status_code == HTTPStatus.CREATED, (
#             f'Если POST-запрос администратора к `{self.USERS_URL}` '
#             'содержит корректные данные - должен вернуться ответ со статусом '
#             '201.'
#         )
#         response_data = response.json()
#         expected_keys = (
#             'first_name', 'last_name', 'username', 'bio', 'role', 'email'
#         )
#         for key in expected_keys:
#             assert response_data.get(key) == data[key], (
#                 f'Если POST-запрос к `{self.USERS_URL}` содержит корректные '
#                 'данные - в ответе должны содержаться данные нового '
#                 f'пользователя. Сейчас ключ {key} отстутствует либо содержит '
#                 'некорректные данные.'
#             )
#
#     def test_05_04_users_post_user_superuser(self, user_superuser_client,
#                                              django_user_model):
#         valid_data = {
#             'username': 'TestUser_3',
#             'role': 'user',
#             'email': 'testuser3@yamdb.fake'
#         }
#         response = user_superuser_client.post(
#             self.USERS_URL, data=valid_data
#         )
#         assert response.status_code == HTTPStatus.CREATED, (
#             f'Если POST-запрос суперпользователя к `{self.USERS_URL}` '
#             'содержит корректные данные - должен вернуться ответ со статусом '
#             '201.'
#         )
#         users_after = (
#             django_user_model.objects.filter(email=valid_data['email'])
#         )
#         assert users_after.exists(), (
#             f'Если POST-запрос суперпользователя к `{self.USERS_URL}` '
#             'содержит корректные данные - должен быть создан новый '
#             'пользователь.'
#         )
#
#     def test_06_users_username_get_admin(self, admin_client, moderator):
#         response = admin_client.get(f'{self.USERS_URL}{moderator.username}/')
#         assert response.status_code != HTTPStatus.NOT_FOUND, (
#             f'Эндпоинт `{self.USERS_URL}'
#             '{username}/` не найден. Проверьте настройки в *urls.py*.'
#         )
#         assert response.status_code == HTTPStatus.OK, (
#             f'Проверьте, что GET-запрос администратора к `{self.USERS_URL}'
#             '{username}/` возвращает ответ со статусом 200.'
#         )
#
#         response_data = response.json()
#         expected_keys = (
#             'first_name', 'last_name', 'username', 'bio', 'role', 'email'
#         )
#         for key in expected_keys:
#             assert response_data.get(key) == getattr(moderator, key), (
#                 'Проверьте, что ответ на GET-запрос администратора к '
#                 f'`{self.USERS_URL}'
#                 '{username}/` содержит данные пользователя.'
#                 f'Сейчас ключ {key} отсутствует в ответе либо содержит '
#                 'некорректные данные.'
#             )
#
#     def test_06_users_username_get_not_admin(self, user_client,
#                                              moderator_client, admin):
#         for test_client in (user_client, moderator_client):
#             response = test_client.get(f'{self.USERS_URL}{admin.username}/')
#             assert response.status_code != HTTPStatus.NOT_FOUND, (
#                 f'Эндпоинт `{self.USERS_URL}'
#                 '{username}/` не найден. Проверьте настройки в *urls.py*.'
#             )
#             assert response.status_code == HTTPStatus.FORBIDDEN, (
#                 'GET-запрос пользователя, не обладающего правами '
#                 f'администратора, отправленный к `{self.USERS_URL}'
#                 '{username}/`, должен вернуть ответ со статусом 403.'
#             )
#
#     def test_07_01_users_username_patch_admin(self, user, admin_client,
#                                               django_user_model):
#         data = {
#             'first_name': 'Admin',
#             'last_name': 'Test',
#             'bio': 'description'
#         }
#         response = admin_client.patch(
#             f'{self.USERS_URL}{user.username}/', data=data
#         )
#         assert response.status_code == HTTPStatus.OK, (
#             'Если PATCH-запрос администратора, отправленный к '
#             f'`{self.USERS_URL}'
#             '{username}/`, содержит корректные данные - должен вернуться '
#             'ответ со статусом 200.'
#         )
#         user = django_user_model.objects.get(username=user.username)
#         for key in data:
#             assert getattr(user, key) == data[key], (
#                 'Проверьте, что PATCH-запрос администратора к '
#                 f'`{self.USERS_URL}'
#                 '{username}/` может изменять данные другого пользователя.'
#             )
#
#         response = admin_client.patch(
#             f'{self.USERS_URL}{user.username}/', data={'role': 'admin'}
#         )
#         assert response.status_code == HTTPStatus.OK, (
#             f'Проверьте, что PATCH-запрос администратора к `{self.USERS_URL}'
#             '{username}/` может изменить роль пользователя.'
#         )
#         response = admin_client.patch(
#             f'{self.USERS_URL}{user.username}/', data={'role': 'owner'}
#         )
#         assert response.status_code == HTTPStatus.BAD_REQUEST, (
#             f'Если в PATCH-запросе администратора к `{self.USERS_URL}'
#             '{username}/` передана несуществующая роль - должен вернуться '
#             'ответ со статусом 400.'
#         )
#
#     def check_user_data_not_changed_with_patch(self, user, client_role):
#         if user:
#             for key in self.PATCH_DATA:
#                 assert getattr(user, key) != self.PATCH_DATA[key], (
#                     f'Проверьте, что PATCH-запрос {client_role} к '
#                     f'`{self.USERS_URL}'
#                     '{username}/` для профиля другого пользователя не '
#                     'изменяет данные этого пользователя.'
#                 )
#         else:
#             raise AssertionError(
#                 f'Проверьте, что PATCH-запрос {client_role} к '
#                 f'`{self.USERS_URL}'
#                 '{username}/` для профиля другого пользователя не удаляет '
#                 'этого пользователя.'
#             )
#
#     def test_07_02_users_username_patch_moderator(self,
#                                                   moderator_client,
#                                                   user,
#                                                   django_user_model):
#         response = moderator_client.patch(
#             f'{self.USERS_URL}{user.username}/', data=self.PATCH_DATA
#         )
#         assert response.status_code == HTTPStatus.FORBIDDEN, (
#             f'Проверьте, что PATCH-запрос модератора к `{self.USERS_URL}'
#             '{username}/` для профиля другого пользователя возвращает ответ '
#             'со статусом 403.'
#         )
#
#         user = (
#             django_user_model.objects.filter(username=user.username).first()
#         )
#         self.check_user_data_not_changed_with_patch(user, 'модератора')
#
#     def test_07_03_users_username_patch_user(self, user_client, user,
#                                              django_user_model):
#         response = user_client.patch(
#             f'{self.USERS_URL}{user.username}/', data=self.PATCH_DATA
#         )
#         assert response.status_code == HTTPStatus.FORBIDDEN, (
#             'Проверьте, что PATCH-запрос пользователя с ролью `user` к '
#             f'`{self.USERS_URL}'
#             '{username}/` возвращает ответ со статусом 403.'
#         )
#
#         user = (
#             django_user_model.objects.filter(username=user.username).first()
#         )
#         self.check_user_data_not_changed_with_patch(
#             user, 'пользователя с ролью `user`'
#         )
#
#     def test_07_05_users_username_put_not_allowed(self, admin_client, user):
#         response = admin_client.put(
#             f'{self.USERS_URL}{user.username}/', data=self.PATCH_DATA
#         )
#         assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
#             f'Проверьте, что PUT-запрос к `{self.USERS_URL}'
#             '{username}/` не предусмотрен и возвращает статус 405.'
#         )
#
#     def test_08_01_users_username_delete_admin(self, user, admin_client,
#                                                django_user_model):
#         users_cnt = django_user_model.objects.count()
#         response = admin_client.delete(f'{self.USERS_URL}{user.username}/')
#         assert response.status_code == HTTPStatus.NO_CONTENT, (
#             f'Проверьте, что DELETE-запрос администратора к `{self.USERS_URL}'
#             '{username}/` возвращает ответ со статусом 204.'
#         )
#         assert django_user_model.objects.count() == (users_cnt - 1), (
#             f'Проверьте, что DELETE-запрос администратора к `{self.USERS_URL}'
#             '{username}/` удаляет пользователя.'
#         )
#
#     def test_08_02_users_username_delete_moderator(self, moderator_client,
#                                                    user, django_user_model):
#         users_cnt = django_user_model.objects.count()
#         response = moderator_client.delete(f'{self.USERS_URL}{user.username}/')
#         assert response.status_code == HTTPStatus.FORBIDDEN, (
#             f'Проверьте, что DELETE-запрос модератора к `{self.USERS_URL}'
#             '{username}/` возвращает ответ со статусом 403.'
#         )
#         assert django_user_model.objects.count() == users_cnt, (
#             f'Проверьте, что DELETE-запрос модератора к `{self.USERS_URL}'
#             '{username}/` не удаляет пользователя.'
#         )
#
#     def test_08_03_users_username_delete_user(self, user_client, user,
#                                               django_user_model):
#         users_cnt = django_user_model.objects.count()
#         response = user_client.delete(f'{self.USERS_URL}{user.username}/')
#         assert response.status_code == HTTPStatus.FORBIDDEN, (
#             'Проверьте, что DELETE-запрос пользователя с ролью `user` к '
#             f'`{self.USERS_URL}'
#             '{username}/` возвращает ответ со статусом 403.'
#         )
#         assert django_user_model.objects.count() == users_cnt, (
#             'Проверьте, что DELETE-запрос пользователя с ролью `user` к'
#             f'`{self.USERS_URL}'
#             '{username}/` не удаляет пользователя.'
#         )
#
#     def test_08_04_users_username_delete_superuser(self, user_superuser_client,
#                                                    user, django_user_model):
#         users_cnt = django_user_model.objects.count()
#         response = user_superuser_client.delete(
#             f'{self.USERS_URL}{user.username}/'
#         )
#         assert response.status_code == HTTPStatus.NO_CONTENT, (
#             'Проверьте, что DELETE-запрос суперпользователя к '
#             f'`{self.USERS_URL}'
#             '{username}/` возвращает ответ со статусом 204.'
#         )
#         assert django_user_model.objects.count() == (users_cnt - 1), (
#             'Проверьте, что DELETE-запрос суперпользователя к '
#             f'`{self.USERS_URL}'
#             '{username}/` удаляет пользователя.'
#         )
#
#     def test_09_users_me_get(self, user_client, user):
#         response = user_client.get(f'{self.USERS_ME_URL}')
#         assert response.status_code == HTTPStatus.OK, (
#             'Проверьте, что GET-запрос обычного пользователя к '
#             f'`{self.USERS_ME_URL}` возвращает ответ со статусом 200.'
#         )
#
#         response_data = response.json()
#         expected_keys = ('username', 'role', 'email', 'bio')
#         for key in expected_keys:
#             assert response_data.get(key) == getattr(user, key), (
#                 f'Проверьте, что GET-запрос к `{self.USERS_ME_URL}` '
#                 'возвращает данные пользователя в неизмененном виде. '
#                 f'Сейчас ключ `{key}` отсутствует либо содержит некорректные '
#                 'данные.'
#             )
#
#     def test_09_02_users_me_delete_not_allowed(self, user_client, user,
#                                                django_user_model):
#         response = user_client.delete(f'{self.USERS_ME_URL}')
#         assert response.status_code == HTTPStatus.METHOD_NOT_ALLOWED, (
#             f'Проверьте, что DELETE-запрос к `{self.USERS_ME_URL}` возвращает '
#             'ответ со статусом 405.'
#         )
#         user = (
#             django_user_model.objects.filter(username=user.username).first()
#         )
#         assert user, (
#             f'Проверьте, что DELETE-запрос к `{self.USERS_ME_URL}` не удаляет '
#             'пользователя.'
#         )
#
#     def test_10_01_users_me_patch(self, django_user_model, admin_client,
#                                   admin, moderator_client, moderator,
#                                   user_client, user):
#         data = {'bio': 'description'}
#
#         for client, user in (
#                 (admin_client, admin),
#                 (moderator_client, moderator),
#                 (user_client, user)
#         ):
#             response = client.patch(f'{self.USERS_ME_URL}', data=data)
#             assert response.status_code == HTTPStatus.OK, (
#                 'Проверьте, что PATCH-запрос к '
#                 f'`{self.USERS_ME_URL}` доступен пользователям всех '
#                 'ролей и возвращает ответ со статусом 200.'
#             )
#             user = django_user_model.objects.filter(
#                 username=user.username
#             ).first()
#             assert user.bio == data['bio'], (
#                 f'Проверьте, что PATCH-запрос к `{self.USERS_ME_URL}` '
#                 'изменяет данные пользователя.'
#             )
#
#     @pytest.mark.parametrize(
#         'data,messege', invalid_data_for_user_patch_and_creation
#     )
#     def test_10_02_users_me_has_field_validation(self, user_client, data,
#                                                  messege):
#         request_method = 'PATCH'
#         response = user_client.patch(self.USERS_ME_URL, data=data)
#         assert response.status_code == HTTPStatus.BAD_REQUEST, (
#             messege[0].format(
#                 url=self.USERS_ME_URL,
#                 request_method=request_method
#             )
#         )
#
#     def test_10_03_users_me_patch_change_role_not_allowed(self,
#                                                           user_client,
#                                                           user,
#                                                           django_user_model):
#         response = user_client.patch(
#             f'{self.USERS_ME_URL}', data=self.PATCH_DATA
#         )
#         assert response.status_code == HTTPStatus.OK, (
#             'Проверьте, что PATCH-запрос пользователя с ролью `user` к '
#             f'`{self.USERS_ME_URL}` возвращает ответ со статусом 200.'
#         )
#
#         current_role = user.role
#         data = {
#             'role': 'admin'
#         }
#         response = user_client.patch(f'{self.USERS_ME_URL}', data=data)
#         user = django_user_model.objects.filter(username=user.username).first()
#         assert user.role == current_role, (
#             f'Проверьте, что PATCH-запрос к `{self.USERS_ME_URL}` с ключом '
#             '`role` не изменяет роль пользователя.'
#         )