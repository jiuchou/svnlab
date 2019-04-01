ps -ef | grep uwsgi | awk '{print $2}' | xargs -i kill -9 {}
ps -ef | grep nginx | awk '{print $2}' | xargs -i kill -9 {}

service nginx reload
service nginx restart
uwsgi --ini /etc/uwsgi/apps-enabled/uwsgi.ini