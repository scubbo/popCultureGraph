import json
import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__))))
from lib.dataFetcher import DataFetcher


class App(object):
    def __init__(self, fetcher=None):
        if not fetcher:
            fetcher = DataFetcher()
        self._fetcher = fetcher

    def get_actors_for_franchise(self, event, context):
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': 'http://pop-culture-graph.s3-website-us-east-1.amazonaws.com'},
            'body': json.dumps(self._fetcher.get_actors_for_franchise(event['queryStringParameters']['id']))
        }

    def get_franchises_for_actor(self, event, context):
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': 'http://pop-culture-graph.s3-website-us-east-1.amazonaws.com'},
            'body': json.dumps(self._fetcher.get_franchises_for_actor(event['queryStringParameters']['id']))
        }


app = App()


def get_actors_for_franchise(event, context):
    return app.get_actors_for_franchise(event, context)


def get_franchises_for_actor(event, context):
    return app.get_franchises_for_actor(event, context)
