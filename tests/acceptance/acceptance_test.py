import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..'))

import re, json
import main.app
import responses


@responses.activate
def test():
    responses.add_callback(
        responses.GET,
        re.compile('https://www[.]imdb[.]com.*'),
        callback=_request_callback,
        content_type='application/json'
    )
    response = main.app.get_actors_for_franchise(
        {
            'queryStringParameters': {
                'id': '0472954',
                'chunkNum': '0'
            }
        },
        None)
    body_response = json.loads(response['body'])['response']
    assert len(body_response) == 3
    assert body_response[0] == {
        'name': 'Charlie Day',
        'char_name': '',  # TODO - that's obviously not right! :)
        'id': '0206359'
    }


def _request_callback(request):
    # Yeah, that's right, Benny - be grateful :P
    path = os.path.join('tests', 'resources', os.path.join(*request.path_url.split('/')))
    # cast to lower here so we don't have to worry about casing in files - though the "live" app should probably query
    # case-sensitively to handle prefixed like "De", "Le", etc.
    if os.path.exists(path.lower()):
        with open(path) as f:
            return 200, {}, f.read()
    else:
        try:
            # TODO - find a way to set the relative path such that this succeeds from `pytest .` *and* from PyCharm
            with open(os.path.join('tests', 'resources', request.path_url.split('/')[1], 'default')) as f:
                return 200, {}, f.read()
        except FileNotFoundError:
            raise Exception("Could not find a static file for path " + request.path_url)
