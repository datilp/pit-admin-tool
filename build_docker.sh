#!/bin/bash

mkdir project
docker build .
# The below command will use the docker-compose.yml and will start a django project
docker-compose run --rm pit_admin_app sh -c "django-admin.py startproject app ."

#To rebuild this image you must use `docker-compose build` or `docker-compose up --build`
# create the frontend django app
docker-compose run --rm pit_admin_app sh -c "python manage.py startapp frontend"

# create the react app
docker-compose run --rm pit_admin_app sh -c "create-react-app pit_react_app"

# install npm packages
docker-compose run --rm pit_admin_app sh -c "cd pit_react_app; npm i webpack webpack-cli --save-dev"
docker-compose run --rm pit_admin_app sh -c "cd pit_react_app; npm i @babel/core babel-loader @babel/preset-env @babel/preset-react --save-dev"

docker-compose run --rm pit_admin_app sh -c "cd pit_react_app; npm i babel-eslint eslint eslint-plugin-react eslint-config-airbnb eslint-config-prettier eslint-plugin-import eslint-plugin-jsx-a11y husky prettier pretty-quick  --save-dev"

docker-compose run --rm pit_admin_app sh -c "cd pit_react_app; npm i css-loader ts-loader --save-dev"
docker-compose run --rm pit_admin_app sh -c "cd pit_react_app; npm i svg-inline-loader --save-dev"

#update local files 
cat << 'EOF' >> project/pit_react_app/.babelrc
{
  "presets": ["@babel/preset-env", "@babel/preset-react"],
  "plugins": ["transform-class-properties"]
}
EOF

# apply loaders
cat << 'EOF2' >> project/pit_react_app/webpack.config.js
module.exports = {
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader"
        }
      },
      { test: /\.css$/, use: 'css-loader' },
      { test: /\.ts$/, use: 'ts-loader' },
      { test: /\.svg$/, use: 'svg-inline-loader' }
    ]
  }
}
EOF2
