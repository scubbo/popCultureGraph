set -e

sam build --use-container
sam local start-lambda >/dev/null 2>&1 &
PID=$! # This assumes that the previous command completed - https://unix.stackexchange.com/questions/90244/bash-run-command-in-background-and-capture-pid

sleep 2

pytest . || kill -9 $PID
