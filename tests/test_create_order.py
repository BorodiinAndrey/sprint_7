import pytest
import requests
import allure
from data.endpoints import CREATE_COURIER_URL, CREATE_ORDER_URL
from helpers.courier_helper import register_new_courier_and_return_login_password


@allure.feature('Проверка создания заказа')
class TestCreateOrder:

    @allure.title('Тест создания заказа')
    @pytest.mark.parametrize(
        'first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color',
        [
            ('Naruto', 'Uzumaki', 'Konoha, 142 apt.', 4, '+7 800 355 35 35', 5, '2020-06-06', 'Saske, come back to Konoha', ['BLACK']),
            ('Naruto', 'Uzumaki', 'Konoha, 142 apt.', 4, '+7 800 355 35 35', 5, '2020-06-06', 'Saske, come back to Konoha', ['GREY']),
            ('Naruto', 'Uzumaki', 'Konoha, 142 apt.', 4, '+7 800 355 35 35', 5, '2020-06-06', 'Saske, come back to Konoha', ['BLACK', 'GREY']),
            ('Naruto', 'Uzumaki', 'Konoha, 142 apt.', 4, '+7 800 355 35 35', 5, '2020-06-06', 'Saske, come back to Konoha', [])
        ]
    )
    def test_create_order_success(self, first_name, last_name, address, metro_station, phone, rent_time, delivery_date, comment, color):
        with allure.step('Создание payload'):
            payload = {'firstName': first_name,
                       'lastName': last_name,
                       'address': address,
                       'metroStation': metro_station,
                       'phone': phone,
                       'rentTime': rent_time,
                       'deliveryDate': delivery_date,
                       'comment': comment,
                       'color': color
            }

        with allure.step('Создание заказа'):
            response = requests.post(CREATE_ORDER_URL, json=payload)

        with allure.step('Проверка, что пришел код 201'):
            assert 201 == response.status_code, f'Пришел код: {response.status_code}'

        with allure.step('Проверка, что в ответе присутствует Track'):
            assert 'track' in response.json(), 'Track отсутствует'

