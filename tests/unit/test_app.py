import json

from hello_world.app import get_actors_for_franchise


def test():
    event = {}
    context = {}
    response = get_actors_for_franchise(event, context)
    assert response['body'][0]['id'] == '0000160'


def build_body_from_response(response):
    return json.loads(response['Payload'].read().decode('utf-8'))['body']