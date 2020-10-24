#!/bin/sh

echo "args: $1"
SAVE="--save"
if [ "$2" == "dev" ]
then
  SAVE="--save-dev"
fi

echo "docker-compose run --rm pit_admin_app sh -c \"cd pit_react_app; npm i $1 $SAVE\""
docker-compose run --rm pit_admin_app sh -c "cd pit_react_app; npm i $1 $2"
