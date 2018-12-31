import json
import os, sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__))))
from lib.dataFetcher import DataFetcher

fetcher = DataFetcher()


def get_actors_for_franchise(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(fetcher.get_actors_for_franchise(event['queryStringParameters']['id']))
    }


def get_franchises_for_actor(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps(fetcher.get_franchises_for_actor(event['queryStringParameters']['id']))
    }
