import json
import os, sys
import responses

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__))))
from lib.dataFetcher import DataFetcher


class App(object):
    def __init__(self, fetcher=None):
        if not fetcher:
            fetcher = DataFetcher()
        self._fetcher = fetcher
        self._access_control_header = 'http://localhost:8000' if _in_local() \
            else 'http://pop-culture-graph.s3-website-us-east-1.amazonaws.com'

    def get_actors_for_franchise(self, event, context):
        return self._build_response(json.dumps(
            self._fetcher.get_actors_for_franchise(
                event['queryStringParameters']['id'],
                int(event['queryStringParameters']['chunkNum'])
            )
        ))

    def get_franchises_for_actor(self, event, context):
        return self._build_response(json.dumps(
            self._fetcher.get_franchises_for_actor(
                event['queryStringParameters']['id'],
                int(event['queryStringParameters']['chunkNum'])
            )
        ))

    def get_id(self, event, context):
        return self._build_response(json.dumps(
            self._fetcher.get_id(
                event['queryStringParameters']['type'],
                event['queryStringParameters']['name']
            )
        ))

    def _build_response(self, body):
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': self._access_control_header
            },
            'body': body
        }


def get_actors_for_franchise(event, context):
    if _in_local():
        return _get_actors_for_franchise_local(event, context)
    else:
        return app.get_actors_for_franchise(event, context)


def get_franchises_for_actor(event, context):
    if _in_local():
        return _get_franchises_for_actor_local(event, context)
    else:
        return app.get_franchises_for_actor(event, context)


def get_id(event, context):
    if _in_local():
        return _get_id_local(event, context)
    else:
        return app.get_id(event, context)


@responses.activate
def _get_actors_for_franchise_local(event, context):
    _setup_responses()
    return app.get_actors_for_franchise(event, context)


@responses.activate
def _get_franchises_for_actor_local(event, context):
    _setup_responses()
    return app.get_franchises_for_actor(event, context)


@responses.activate
def _get_id_local(event, context):
    # DEBUG for speedy responses
    if event['queryStringParameters']['name'] == 'Charlie Day':
        print('DEBUG speedy response for get_id_local')
        return app._build_response('"0206359"')
    print('DEBUG no speedy response for get_id_local')
    print(event)

    _setup_responses()
    # return app.get_id(event, context)
    resp = app.get_id(event, context)
    print('DEBUG:')
    print(resp)
    return resp


def _in_local():
    return os.environ.get('Stage', '') == 'local'


def _setup_responses():
    import re

    def _request_callback(request):
        path = os.path.join('local-resources', os.path.join(*request.path_url.split('/')))
        # cast to lower here so we don't have to worry about casing in files - though the "live" app should probably query
        # case-sensitively to handle prefixed like "De", "Le", etc.
        if os.path.exists(path.lower()):
            with open(path) as f:
                return 200, {}, f.read()
        else:
            try:
                with open(os.path.join('local-resources', request.path_url.split('/')[1], 'default')) as f:
                    return 200, {}, f.read()
            except FileNotFoundError:
                raise Exception("Could not find a static file for path " + request.path_url)

    responses.add_callback(
        responses.GET,
        re.compile('https://www[.]imdb[.]com.*'),
        callback=_request_callback,
        content_type='application/json'
    )


app = App()
