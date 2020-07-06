#!/bin/bash

loginx() {
  email=$1
  pwd=$2


  curl -X POST -d email=$email -d password=$pwd -H 'Accept: application/json;' http://localhost:8000/api/user/loginx/
}

loginkx() {
  email=$1
  pwd=$2

  # for an inpput such as:
  # ./curl_cmds.sh loginkx hello adios
  # we get an enconding of
  #Basic aGVsbG86YWRpb3M=
  # which gets added to the Authorization header

  encoding=`python <<END_SCRIPT
import base64
def get_basic_auth_header(username, password):
  return 'Basic %s' % base64.b64encode(
    ('%s:%s' % (username, password)).encode('ascii')).decode()

print(get_basic_auth_header("$email","$pwd"))
END_SCRIPT`

  curl -X POST -H "Authorization:$encoding" -H 'Accept: application/json;' http://localhost:8000/api/user/loginkx/
}

mex() {
  token=$1
  curl -X GET -H "Authorization:Token $token" http://localhost:8000/api/user/me/
}

logoutx() {
  token=$1
  curl -X POST -H "Content-Type: application/json" \
    -H "Authorization:Token $token" \
    -d token=$token \
     http://localhost:8000/api/user/logoutx/
}


case "$1" in
  login)
    loginx $2 $3
    ;;
  loginkx)
    loginkx $2 $3
    ;;
  logout)
    logoutx $2
    ;;
  me)
    mex $2
    ;;
  *)
    echo $"Usage: $0 {login email pwd|logout token|me token}"
    exit1
esac
