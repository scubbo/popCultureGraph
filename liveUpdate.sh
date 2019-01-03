#!/bin/bash

# NOTE that this won't pull in dependencies - you'll need to run `sam build` for that

set -e

for target in $(find .aws-sam/build -d 1 -type d)
do
rsync -a main/* ${target} --exclude "*__pycache__*" --exclude "*.pytest_cache*"
# Also copy in the "local mock" files, so we can do local in-browser testing. Uck.
rm -rf ${target}/local-resources
mkdir ${target}/local-resources
rsync -a tests/resources/* ${target}/local-resources
done