# TODO - proper testing framework without having to duplicate this sys.path hack in every file
import os, sys
import json
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from unittest.mock import Mock
import main.app
mockDataFetcher = Mock()
mockDataFetcher.get_actors_for_franchise.return_value = [{'id':'0000160'}]
mockDataFetcher.get_franchises_for_actor.return_value = [
    None,
    {
        'id':'4643084',
        'franchise_name': 'Counterpart',
        'char_name': 'Howard Silk'
     }
]
app = main.app.App(mockDataFetcher)


def test_get_actors():
    event = {
        'queryStringParameters': {
            'id': '2397535'
        }
    }
    response = app.get_actors_for_franchise(event, {})
    assert json.loads(response['body'])[0]['id'] == '0000160'
    mockDataFetcher.get_actors_for_franchise.assert_called_with('2397535')


def test_get_franchises():
    event = {
        'queryStringParameters': {
            'id': '0799777'
        }
    }
    response = app.get_franchises_for_actor(event, {})
    sample_row = json.loads(response['body'])[1]
    assert sample_row == {
        'id':  '4643084',
        'franchise_name': 'Counterpart',
        'char_name': 'Howard Silk'
    }
    mockDataFetcher.get_franchises_for_actor.assert_called_with('0799777')
