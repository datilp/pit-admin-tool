####
#### loginks test@lbto.org abcd123
#### logout <token>
alias login='./curl_cmds.sh login '
alias loginkx='./curl_cmds.sh loginkx '
alias logout='./curl_cmds.sh logout '
alias dbsh='docker exec -it pit-admin-tool_pit_admin_app_1 sh -c "python manage.py dbshell"'
alias dls='docker container ls -a --no-trunc'
alias dsh='docker exec -it pit-admin-tool_pit_admin_app_1 sh -c "/bin/sh"'
alias droot='docker exec -u 0 -it pit-admin-tool_pit_admin_app_1 sh'
alias cfp_test='docker-compose run --rm pit_admin_app sh -c "python manage.py test CfP_app"'
alias run_mig='docker-compose run --rm pit_admin_app sh -c "python manage.py migrate"'
alias cfp_mk_mig='docker-compose run --rm pit_admin_app sh -c "python manage.py makemigrations CfP_app"'
