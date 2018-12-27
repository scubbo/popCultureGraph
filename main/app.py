import json
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__))))
from lib.dataFetcher import DataFetcher


def get_actors_for_franchise(event, context):
    fetcher = DataFetcher()

    return {
        'statusCode': 200,
        'body': json.dumps(fetcher.get_actors_for_franchise(event['queryStringParameters']['id']))
    }
