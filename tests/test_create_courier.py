import pytest
import requests
import allure
from data.endpoints import CREATE_COURIER_URL
from helpers.courier_helper import register_new_courier_and_return_login_password


@allure.feature('Проверка создания курьера')
class TestCreateCourier:

    @allure.title('Тест на создание курьера')
    def test_create_courier_success(self):
        with allure.step('Регистрация курьера'):
            creds = register_new_courier_and_return_login_password()
        with allure.step('Проверка, что креды вернулись'):
            assert creds, "Регистрация не осуществлена, вернулся пустой список и код 400"

    @allure.title('Тест на создание курьеров с одинаковыми данными')
    def test_create_same_couriers(self):
        with allure.step('Регистрация курьера'):
            creds = register_new_courier_and_return_login_password()
        with allure.step('Возврат данных курьера в переменную'):
            login, password, first_name = creds
        with allure.step('Создание payload'):
            payload = {'login': login, 'password': password}

        with allure.step('Создание курьера с теми же кредами'):
            create_courier = requests.post(CREATE_COURIER_URL, json=payload)

        with allure.step('Проверка, что вернулся код 409'):
            assert create_courier.status_code == 409, f"Получили код: {create_courier.status_code}"

        with allure.step('Проверка сообщения'):
            expected_message = "Этот логин уже используется. Попробуйте другой."
            actual_message = create_courier.json().get("message")

            assert actual_message == expected_message, f"Получили message: {actual_message}"

    @allure.title('Тест с невалидными данными')
    @pytest.mark.parametrize(
        'login, password',
        [
            ('12345', ''),
            ('', '12345'),
            ('', '')
        ]
    )
    def test_create_couriers_with_invalid_data(self, login, password):
        with allure.step('Формирование payload'):
            payload = {"login": login, "password": password}
        with allure.step('Регистрация курьера'):
            create_courier = requests.post(CREATE_COURIER_URL, json=payload)

        with allure.step('Проверка, что вернулся код 400'):
            assert create_courier.status_code == 400, f"Получили код: {create_courier.status_code}"

        with allure.step('Проверка сообщения'):
            expected_message = "Недостаточно данных для создания учетной записи"
            actual_message = create_courier.json().get("message")

            assert actual_message == expected_message, f"Получили message: {actual_message}"