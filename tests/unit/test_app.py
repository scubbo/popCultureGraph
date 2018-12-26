# TODO - proper testing framework without having to duplicate this in every file
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

from hello_world.app import get_actors_for_franchise


def test():
    event = {}
    context = {}
    response = get_actors_for_franchise(event, context)
    assert response['body'][0]['id'] == '0000160'
