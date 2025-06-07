import requests
import allure
from data.endpoints import GET_ORDERS_URL


@allure.feature('Проверка получения списка заказов')
class TestGetOrders:

    @allure.title('Тест получения списка заказов')
    def test_get_list_orders_success(self):
        with allure.step('Получение списка заказов'):
            response = requests.get(GET_ORDERS_URL)

        with allure.step('Проверка, что пришел код 200'):
            assert 200 == response.status_code, f'Пришел код: {response.status_code}'

        with allure.step('Проверка, что тело ответа — список'):
            body = response.json()['orders']
            assert isinstance(body, list), f'Список заказов не пришел'
