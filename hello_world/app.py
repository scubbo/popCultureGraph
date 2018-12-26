from hello_world.dataFetcher import DataFetcher


def get_actors_for_franchise(event, context):
    # TODO - dynamically get id from event
    fetcher = DataFetcher()
    return {
        'statusCode': 200,
        'body': fetcher.get_actors_for_franchise("2397535")
    }
