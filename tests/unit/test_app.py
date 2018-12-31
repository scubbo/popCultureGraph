# TODO - proper testing framework without having to duplicate this sys.path hack in every file
import os, sys
import json
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from main.app import get_actors_for_franchise, get_franchises_for_actor


def test_get_actors():
    event = {
        'queryStringParameters': {
            'id': '2397535'
        }
    }
    response = get_actors_for_franchise(event, {})
    assert json.loads(response['body'])[0]['id'] == '0000160'


def test_get_franchises():
    event = {
        'queryStringParameters': {
            'id': '0799777'
        }
    }
    response = get_franchises_for_actor(event, {})
    sample_row = json.loads(response['body'])[5]
    assert sample_row == {
        'id':  '4643084',
        'franchise_name': 'Counterpart',
        'char_name': 'Howard Silk'
    }
