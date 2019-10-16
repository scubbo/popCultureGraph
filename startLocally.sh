#!/bin/bash

set -e

function cleanup {
  kill ${WEB_PID}
  cd ..
  exit
}

trap cleanup SIGINT

python3 buildStaticSiteContent.py --stage local
cd built_resources
python3 -m http.server 8000 &
cd ..

# This assumes that the previous command completed -
# https://unix.stackexchange.com/questions/90244/bash-run-command-in-background-and-capture-pid
WEB_PID=$!

echo "Web Server started on http://localhost:8000"

# TODO - add a flag to conditionally execute the line below.
# You'd think that would be easy, but, well, bash...
# https://stackoverflow.com/questions/192249/how-do-i-parse-command-line-arguments-in-bash/29754866#29754866
# sam build --use-container
sam local start-api --log-file logging.log \
  --env-vars <( echo "{\"Parameters\":{\"Stage\":\"local\"}}" ) \
  --skip-pull-image -d 5858 # -- uncomment this to allow debugging on that port

while true; do sleep 1; done

