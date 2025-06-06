import pytest
import requests
import allure
from data.endpoints import LOGIN_COURIER_URL
from helpers.courier_helper import register_new_courier_and_return_login_password


@allure.feature('Проверка авторизации курьера')
class TestLoginCourier:

    @allure.title('Тест на авторизацию курьера')
    def test_login_courier_success(self):
        with allure.step('Регистрация курьера'):
            creds = register_new_courier_and_return_login_password()
        with allure.step('Возврат данных курьера в переменную'):
            login, password, first_name = creds
        with allure.step('Создание payload'):
            payload = {'login': login, 'password': password}
        with allure.step('Авторизация курьера'):
            response = requests.post(LOGIN_COURIER_URL, json=payload)

        with allure.step('Проверка, что пришел код 200'):
            assert 200 == response.status_code, f'Пришел код: {response.status_code}'

        with allure.step('Проверка, что в ответе присутствует ID'):
            assert 'id' in response.json(), f'ID не присвоен'

    @allure.title('Тест на авторизацию курьера с невалидными данными')
    @pytest.mark.parametrize(
        'login, password, expected_status, expected_message',
        [
            ('', '', 400, 'Недостаточно данных для входа'),
            ('sfsdfs', 'fsdfsd', 404, 'Учетная запись не найдена')
        ]
    )
    def test_login_courier_invalid_data(self, login, password, expected_status, expected_message):
        with allure.step('Создание payload'):
            payload = {}
            if login is not None:
                payload['login'] = login
            if password is not None:
                payload['password'] = password

        with allure.step(f'Авторизация курьера c payload {payload}'):
            response = requests.post(LOGIN_COURIER_URL, json=payload)

        with allure.step(f'Проверка, что пришел код {expected_status}'):
            assert expected_status == response.status_code, f'Пришел код: {response.status_code}'

        with allure.step('Проверка сообщения'):
            actual_message = response.json().get("message")
            assert actual_message == expected_message, f"Получили message: {actual_message}"
