import allure
from jsonschema.validators import validate

import conftest
from conftest import load_json_schema

project = 'catfact'

@allure.title('Успешное заполнение формы list_of_breeds')
def test_successful_list_of_breeds():
    with allure.step(f'Отправили запрос get/breeds'):
        response = conftest.api_request(
            project=project,
            url='/breeds',
            method='get'
        )

    with allure.step(f'Получили в ответ {response.status_code} статус'):
        assert response.status_code == 200

@allure.title('Успешное получение схемы json по list_of_breeds')
def test_successful_list_of_breeds_schema_response_format():
    schema = load_json_schema('get_list_of_breeds_schema_response.json')
    with allure.step(f'Отправили запрос get/breeds для получения схемы json'):
        response = conftest.api_request(
            project=project,
            url='/breeds',
            method='get',
            json=schema
        )

    with allure.step(f'Проверили, соответствует ли полученная схема json шаблону'):
        validate(
            instance=response.json(),
            schema=schema
        )

@allure.title('Отправка валидного лимита в list_of_breeds')
def test_successful_list_of_breeds_with_limit():
    params = {'limit': 3}

    with allure.step(f'Отправляем запрос get/breeds с {params}'):
        response = conftest.api_request(
            project=project,
            url='/breeds',
            method='get',
            params=params
        )

    with allure.step(
            f'Получили в ответ {response.status_code} код и проверили в схеме json '
            f'валидность переданного параметра'):
        assert response.status_code == 200
        assert response.json()['per_page'], [1] == params
