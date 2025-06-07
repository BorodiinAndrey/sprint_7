import pytest
import requests
import allure
from data.endpoints import LOGIN_COURIER_URL, CREATE_COURIER_URL
from helpers.courier_helper import register_new_courier_and_return_login_password


@pytest.fixture()
def courier():
    with allure.step('Регистрация тестового курьера через helper'):
        creds = register_new_courier_and_return_login_password()
        login, password, first_name = creds

    yield creds

    with allure.step('Авторизация для получения ID и удаление курьера'):
        login_resp = requests.post(LOGIN_COURIER_URL, json={"login": login, "password": password})

        if login_resp.status_code == 200 and "id" in login_resp.json():
            courier_id = login_resp.json()["id"]
            delete_resp = requests.delete(f"{CREATE_COURIER_URL}/{courier_id}")
            assert delete_resp.status_code == 200, (f"Не смогли удалить курьера {courier_id}, status_code={delete_resp.status_code}")
