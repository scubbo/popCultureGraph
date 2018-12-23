import os
import json
import boto3
import botocore


def test():
    # Set "running_locally" flag if you are running the integration test locally
    running_locally = bool(os.getenv('RUNNING_LOCALLY', 'false'))

    print('DEBUG - running locally=' + str(running_locally))

    if running_locally:

        # Create Lambda SDK client to connect to appropriate Lambda endpoint
        lambda_client = boto3.client(
            'lambda',
            region_name="us-west-2",
            endpoint_url="http://127.0.0.1:3001",
            use_ssl=False,
            verify=False,
            config=botocore.client.Config(
                signature_version=botocore.UNSIGNED,
                read_timeout=10,
                retries={'max_attempts': 0},
            )
        )
    else:
        lambda_client = boto3.client('lambda')

    # Invoke your Lambda function as you normally usually do. The function will run
    # locally if it is configured to do so
    response = lambda_client.invoke(FunctionName="HelloWorldFunction")
    body = json.loads(build_body_from_response(response))
    assert body[0]['id'] == 1


def build_body_from_response(response):
    return json.loads(response['Payload'].read().decode('utf-8'))['body']