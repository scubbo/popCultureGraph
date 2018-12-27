# TODO - proper testing framework without having to duplicate this in every file
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))
import json

from main.app import get_actors_for_franchise


def test():
    event = {
        'queryStringParameters': {
            'id': '2397535'
        }
    }
    context = {}
    response = get_actors_for_franchise(event, context)
    assert json.loads(response['body'])[0]['id'] == '0000160'
