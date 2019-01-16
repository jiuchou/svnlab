#!/bin/bash

getUserInfo() {
    type=$1

    # 获取用户(user)
    userQuery=""
    users=$(cat lineContents | grep -v '@' | grep "${type}$" | awk -F '=' '{print $1}')
    for user in ${users[@]}; do
        userQuery="${user},${userQuery}"
    done
    # 获取用户(group)
    groupUserQuery=""
    groups=$(cat lineContents | grep '@' | grep "${type}$" | awk -F '=' '{print $1}' | awk -F '@' '{print $2}')
    for group in ${groups[@]}; do
        groupUsers=$(grep "^${group}=" ${authFile} | awk -F '=' '{print $2}')
        groupUserQuery="${groupUsers},${groupUserQuery}"
    done
}

getModuleRole() {
    manager=$1

    urls=$(grep "${manager}" ${managerToUrl} | awk -F ',' '{print $2}')
    for url in ${urls[@]}; do
        # get module and path by url
        # http://10.6.5.2/svn/Documents/SETeam
        suffixUrl="${url#*svn*/}"
        module="${suffixUrl%%/*}"
        path="/${suffixUrl#*/}"
        projectDir="\[${module}\:${path}\]"
        # 获取当前projectDir所在配置文件行
        projectDirLineNum=$(grep -rn "${projectDir}" ${authFile} | awk -F ':' '{print $1}')
        if [[ "${projectDirLineNum}" == "" ]]; then
            continue
        fi

        # lineContents
        # 45128=rw
        # @groupname=rw
        sed -n "${projectDirLineNum},/\[/p" ${authFile} | grep -v '\[' > lineContents
        sed -i "/^$/d" lineContents

        getUserInfo "r"
        if [[ "${groupUserQuery}" == "" ]]; then
            readOnlyUser="${userQuery}"
        else
            readOnlyUser="${userQuery},${groupUserQuery}"
        fi
        readOnlyUserNum=$(echo ${readOnlyUser} | tr ',' '\n' | grep -v "^$" | wc -l)
        getUserInfo "rw"
        if [[ "${groupUserQuery}" == "" ]]; then
            readAndWriteUser="${userQuery}"
        else
            readAndWriteUser="${userQuery},${groupUserQuery}"
        fi
        readAndWriteUserNum=$(echo ${readAndWriteUser} | tr ',' '\n' | grep -v "^$" | wc -l)

        # Base on [modules:path] get UserInfo
        # readOnlyUser
        # readAndWriteUser
        echo "module=${module}
path=${path}
url=${url}
manager=${manager}
readOnlyUser=${readOnlyUser}
readOnlyUserNum=${readOnlyUserNum}
readAndWriteUser=${readAndWriteUser}
readAndWriteUserNum=${readAndWriteUserNum}
" > ${moduleRoleFile}

        # insert module role info to DB
        insertModuleRoleToDB ${manager}

        # clean useless file from runtime
        rm -f lineContents
    done
}

manager=$1

currentPath=$(cd $(dirname $0); pwd -P)
managerToUrl="${currentPath}/managerToUrl"
authFile="${currentPath}/dav_svn.authz"
moduleRoleFile="${currentPath}/moduleRoleFile"

source ${currentPath}/insertRoleToDB.sh
getModuleRole ${manager}
