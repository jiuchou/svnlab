#!/bin/bash

HOST="127.0.0.1"
PORT="3306"
USERNAME="root"
PASSWORD="root"
DATABASENAME="svnlab"
roleTableName="user_role"

username=$1

mysql -h${HOST} -P${PORT} -u${USERNAME} -p${PASSWORD} ${DATABASENAME} <<EOF 2>/dev/null
    DELETE FROM ${roleTableName} WHERE username=${username};
EOF

while read line; do
query=$(echo ${line} | awk -F ',' '{printf("%s", \"%s\", \"%s\", \"%s\", \"%s\", "%s", $1, $2, $3, $4, $5, $6}')
mysql -h${HOST} -P${PORT} -u${USERNAME} -p${PASSWORD} ${DATABASENAME} <<EOF 2>/dev/null
    INSERT INTO ${roleTableName}(username, role, module, path, url, manager) VALUES(${query});
EOF
done < userRoleFile
