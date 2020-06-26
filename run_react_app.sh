#!/bin/sh

docker-compose run --rm -p 3000:3000 pit_admin_app sh -c "cd pit_react_app; npm run start"
