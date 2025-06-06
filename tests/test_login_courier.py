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
        with allure.step('Проверка, что присвоен id'):
            assert 'id' in response.json(), f'ID не присвоен'
