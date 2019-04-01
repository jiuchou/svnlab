#!/bin/bash

ROOTPATH=$(cd $(dirname $0); pwd -P)

# export http_proxy=
# export https_proxy=
pip=$(which pip)
pip_path=$(${pip} show svnlab | grep 'Location' | awk '{print $2}')
svnlab_path=$(pip_path)/svnlab

uwsgi_config_file=/etc/uwsgi/apps-enabled/uwsgi.ini
nginx_config_file=/etc/nginx/sites-enabled/default

install_rely() {
    which nginx || apt-get install nginx && echo `nginx -v`
    which uwsgi || ${pip} install uWSGI && echo `uwsgi --version`
}

config_uwsgi() {
    cp ${ROOTPATH}/uwsgi.ini ${uwsgi_config_file}
    sed -i "s#CHDIR#${svnlab_path}#g" ${uwsgi_config_file}
    uwsgi --ini ${uwsgi_config_file}
}

config_nginx() {
    cp ${ROOTPATH}/nginx.ini ${nginx_config_file}
    sed -i "s#CHDIR#${svnlab_path}#g" ${nginx_config_file}
    service nginx restart
}

install_rely
config_uwsgi
config_nginx
