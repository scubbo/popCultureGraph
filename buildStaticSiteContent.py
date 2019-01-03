#!/usr/bin/env python3
import os, shutil, argparse

STAGES = {
    'local': {
        'api_prefix': 'http://127.0.0.1:3000'
    },
    'prod': {
        'api_prefix': 'https://qj1ay789xj.execute-api.us-east-1.amazonaws.com/Prod'
    }
}

RESOURCES_SOURCE_DIRECTORY = 'res'
BUILT_RESOURCES_DIRECTORY = 'built_resources'


def main(args):
    if os.path.exists(BUILT_RESOURCES_DIRECTORY):
        shutil.rmtree(BUILT_RESOURCES_DIRECTORY)

    shutil.copytree(RESOURCES_SOURCE_DIRECTORY, BUILT_RESOURCES_DIRECTORY)

    os.remove(os.path.join(BUILT_RESOURCES_DIRECTORY, 'js', 'main.js'))

    with open(os.path.join(RESOURCES_SOURCE_DIRECTORY, 'js', 'main.js')) as index_input, \
            open(os.path.join(BUILT_RESOURCES_DIRECTORY, 'js', 'main.js'), 'a') as index_output:
        index_output.write(index_input.read().replace('{API_PREFIX}', STAGES[args.stage]['api_prefix']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', choices=STAGES)
    main(parser.parse_args())
