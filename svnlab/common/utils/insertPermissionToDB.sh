#!/bin/bash

HOST="127.0.0.1"
PORT="3306"
USERNAME="root"
PASSWORD="root"
DATABASENAME="svnlab"
userRoleTableName="user_role"

currentPath=$(cd $(dirname $0); pwd -P)

insertToPermissionDeveloper() {
    username=$1

    mysql -h${HOST} -P${PORT} -u${USERNAME} -p${PASSWORD} ${DATABASENAME} <<EOF 2>/dev/null
        DELETE FROM ${userRoleTableName} WHERE username=${username};
EOF

    while read line; do
        query=$(echo ${line} | awk -F ',' '{printf("%s, \"%s\", \"%s\", \"%s\", \"%s\", %s", $1, $2, $3, $4, $5, $6)}')
        mysql -h${HOST} -P${PORT} -u${USERNAME} -p${PASSWORD} ${DATABASENAME} <<EOF 2>/dev/null
            INSERT INTO ${userRoleTableName}(username, role, module, path, url, manager) VALUES(${query});
EOF
    done < ${currentPath}/userRoleFile
}
