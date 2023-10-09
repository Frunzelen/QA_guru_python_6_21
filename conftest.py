import os
import json
import allure

from allure_commons.types import AttachmentType
from curlify import to_curl
from requests import sessions


def load_json_schema(name: str):
    schema_path = os.path.join(os.path.dirname
                               (os.path.abspath(__file__)),
                               'json_schemas', name)
    with open(schema_path) as schema:
        return json.loads(schema.read())


def api_request(project, url, method, **kwargs):
    base_urls = {
        'catfact': 'https://catfact.ninja',
        'reqres': 'https://reqres.in/api'
        }
    new_url = base_urls[project] + url

    with allure.step(f"{method.upper()} {new_url}"):
        with sessions.Session() as session:
            response = session.request(method=method, url=new_url, **kwargs)
            message = to_curl(response.request)

            allure.attach(
                body=message.encode('utf-8'),
                name='Curl',
                attachment_type=AttachmentType.TEXT,
                extension='txt'
            )
        if not response.content:
            allure.attach(
                body='empty response',
                name='Empty Response',
                attachment_type=AttachmentType.TEXT,
                extension='txt'
            )
        else:
            allure.attach(
                body=json.dumps(response.json(), indent=4).encode('utf-8'),
                name='Response Json',
                attachment_type=AttachmentType.JSON,
                extension='json'
            )
    return response
