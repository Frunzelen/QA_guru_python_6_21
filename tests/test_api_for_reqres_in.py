import allure
from jsonschema.validators import validate

import conftest
from conftest import load_json_schema

project = 'reqres'


@allure.title('Успешное создание пользователя')
def test_successful_create_user():
    data = {'name': 'Elena',
            'job': 'QA Automation Engineer'}

    with allure.step(f'Отправили имя и место работы'):
        response = conftest.api_request(
            project=project,
            url='/users',
            method='post',
            data=data
        )
    with allure.step(
            f'Получили {response.status_code} код, проверили что данные успешно отправлены'):
        assert response.status_code == 201
    assert response.json()['name'] == 'Elena'
    assert response.json()['job'] == 'QA Automation Engineer'


@allure.title('Успешное создание пользователя с проверкой схемы json')
def test_create_user_schema_response_format():
    schema = load_json_schema('post_create_user_schema_response.json')
    data = {'name': 'Elena',
            'job': 'QA Automation Engineer'}

    with allure.step(f'Отправили запрос post/users для получения схемы json'):
        response = conftest.api_request(
            project=project,
            url='/users',
            method='post',
            data=data,
            json=schema
        )
    with allure.step(f'Проверили, соответствует ли полученная схема json шаблону'):
        validate(response.json(), schema)


@allure.title('Успешное удаление пользователя')
def test_successful_test_delete_user():
    with allure.step(f'Отправили запрос delete/users/2'):
        response = conftest.api_request(
            project=project,
            url='/users/2',
            method='delete'
        )
    with allure.step(f' Получили {response.status_code} код'):
        assert response.status_code == 204


@allure.title('Успешное открытие определенной страницы списка пользователей')
def test_successful_get_list_users_by_page():
    params = {'page': 3}

    with allure.step(f'Отправили {params}'):
        response = conftest.api_request(
            project=project,
            url='/users',
            method='get',
            params=params
        )

    with allure.step(
            f' Получили {response.status_code} код и проверили валидность отправленных данных '):
        assert response.status_code == 200
        assert response.json()['page'], [1] == params


@allure.title('Успешный переход на определенную страницу с данными')
def test_successful_get_list_users_data_by_per_page():
    params = {'per_page': 5}

    with allure.step(f'Отправили {params}'):
        response = conftest.api_request(
            project=project,
            url='/users',
            method='get',
            params=params
        )

    with allure.step(
            f' Получили {response.status_code} код и проверили валидность отправленных данных '):
        assert response.status_code == 200
        assert response.json()['per_page'], [1] == params
        assert len(response.json()['data']), [1] == params


@allure.title('Успешное создание списка пользователей с проверкой схемы json')
def test_get_list_users_schema_response_format():
    schema = load_json_schema('get_list_users_schema_response.json')

    with allure.step(f'Отправили запрос get/users для получения схемы json'):
        response = conftest.api_request(
            project=project,
            url='/users',
            method='get',
            json=schema
        )

    with allure.step(f'Проверили, соответствует ли полученная схема json шаблону'):
        validate(
            instance=response.json(),
            schema=schema
        )


@allure.title('Успешная регистрация пользователя')
def test_register_successful_user_():
    data = {'email': 'eve.holt@reqres.in',
            'password': 'pistol'}

    with allure.step(f'Отправили {data}'):
        response = conftest.api_request(
            project=project,
            url='/register',
            method='post',
            data=data
        )

    with allure.step(f'Получили {response.status_code} код'):
        assert response.status_code == 200


@allure.title('Не успешная регистрация пользователя')
def test_register_unsuccessful_user_():
    data = {'email': 'sydney@fife'}

    response = conftest.api_request(
        project=project,
        url='/register',
        method='post',
        data=data
    )

    assert response.json()['error'] == 'Missing password'


@allure.title('Успешная регистрация пользователя с проверкой схемы json')
def test_register_successful_user_schema_response_format():
    schema = load_json_schema('post_register_user_schema_response.json')
    data = {'email': 'eve.holt@reqres.in',
            'password': 'pistol'}

    with allure.step(f'Отправили запрос post/register для получения схемы json'):
        response = conftest.api_request(
            project=project,
            url='/register',
            method='post',
            data=data
        )

    with allure.step(f'Проверили, соответствует ли полученная схема json шаблону'):
        validate(instance=response.json(),
                 schema=schema)


@allure.title('Успешное обновление данных пользователя')
def test_successful_update_user_():
    data = {'name': 'Elena',
            'job': 'QA Automation Engineer'}

    with allure.step(f'Отправили данные пользователя {data}'):
        response = conftest.api_request(
            project=project,
            url='/users/2',
            method='patch',
            data=data
        )

    with allure.step(
            f'Получили {response.status_code} код, проверили что данные успешно отправлены'):
        assert response.status_code == 200
        assert response.json()['name'] == 'Elena'
        assert response.json()['job'] == 'QA Automation Engineer'


@allure.title('Успешное обновление данных пользователя с проверкой схемы json')
def test_update_user_schema_response_format():
    schema = load_json_schema('patch_update_user_schema_response.json')
    data = {'name': 'Elena',
            'job': 'QA Automation Engineer'}

    with allure.step(f'Отправили запрос patch/users/2 для получения схемы json'):
        response = conftest.api_request(
            project=project,
            url='/users/2',
            method='patch',
            data=data,
            json=schema
        )

    with allure.step(f'Проверили, соответствует ли полученная схема json шаблону'):
        validate(instance=response.json(),
                 schema=schema)
