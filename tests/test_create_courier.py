import pytest
import requests
import allure
from data.endpoints import CREATE_COURIER_URL
from helpers.courier_helper import register_new_courier_and_return_login_password


@allure.feature('Проверка регистрации курьера')
class TestCreateCourier:

    @allure.title('Тест регистрации курьера')
    def test_create_courier_success(self):
        with allure.step('Регистрация курьера'):
            creds = register_new_courier_and_return_login_password()
        with allure.step('Проверка, что креды вернулись'):
            assert creds, "Регистрация не осуществлена, вернулся пустой список и код 400"

    @allure.title('Тест регистрации курьеров с одинаковыми данными')
    def test_create_same_couriers(self):
        with allure.step('Регистрация курьера'):
            creds = register_new_courier_and_return_login_password()
        with allure.step('Возврат данных курьера в переменную'):
            login, password, first_name = creds
        with allure.step('Создание payload'):
            payload = {'login': login, 'password': password}

        with allure.step('Регистрация курьера с теми же кредами'):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        with allure.step('Проверка, что вернулся код 409'):
            assert response.status_code == 409, f"Получили код: {response.status_code}"

        with allure.step('Проверка сообщения'):
            expected_message = "Этот логин уже используется. Попробуйте другой."
            actual_message = response.json().get("message")

            assert actual_message == expected_message, f"Получили message: {actual_message}"

    @allure.title('Тест регистрации курьера с невалидными данными')
    @pytest.mark.parametrize(
        'login, password, expected_status, expected_message',
        [
            ('12345', '', 400, 'Недостаточно данных для создания учетной записи'),
            ('', '12345', 400, 'Недостаточно данных для создания учетной записи'),
            ('', '', 400, 'Недостаточно данных для создания учетной записи')
        ]
    )
    def test_create_couriers_with_invalid_data(self, login, password, expected_status, expected_message):
        with allure.step('Формирование payload'):
            payload = {"login": login, "password": password}
        with allure.step(f'Регистрация курьера c payload {payload}'):
            response = requests.post(CREATE_COURIER_URL, json=payload)

        with allure.step('Проверка, что вернулся код 400'):
            assert response.status_code == 400, f"Получили код: {response.status_code}"

        with allure.step('Проверка сообщения'):
            actual_message = response.json().get("message")
            assert actual_message == expected_message, f"Получили message: {actual_message}"
