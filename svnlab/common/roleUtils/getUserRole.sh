#!/bin/bash

getUserRoleByIdentify() {
    # 10:11111=rw
    # 10:@group=rw
    lineContent=$1

    # roleContent: rw
    roleContent=$(echo ${lineContent} | awk -F '=' '{print $2}')
    if [[ "${roleContent}" == "" ]]; then
        role=0
    elif [[ "${roleContent}" == "r" ]]; then
        role=1
    elif [[ "${roleContent}" == "rw" ]]; then
        role=3
    else
        role=-1
    fi

    # projectDir
    lineNumber=$(echo ${lineContent} | awk -F ':' '{print $1}')
    sed -n "1,${lineNumber} p" ${authFile} > temp
    # [Document:/test]
    module=$(grep "]" temp | tail -n 1 | awk -F ':' '{print $1}' | awk -F '[' '{print $2}')
    path=$(grep "]" temp | tail -n 1 | awk -F ':/' '{print $2}' | awk -F ']' '{print $1}')
    prefix_url=$(sed -n "/${module}/p" ${prefixUrl} | awk -F '=' '{print $2}')
    url=${prefix_url}${module}/${path}
    echo "username,${role},${module},${path},${url},manager" >> ${userRoleFile}
}

getUserRole() {
    username=$1
    lineContents=$(grep -rn "${username}" ${authFile})
    for lineContent in ${lineContents[@]}; do
        identify=$(echo "${lineContent}" | awk -F ':' '{print $2}' | awk -F '=' '{print $1}')
        if [[ "${identify}" == "${username}" ]]; then
            # 用户
            getUserRoleByIdentify "${lineContent}"
        else
            # 组
            groupname=${identify}
            groupLineContents=$(grep -rn "^@${groupname}=" ${authFile})
            for groupLineContent in ${groupLineContents[@]}; do
                getUserRoleByIdentify "${groupLineContent}"
            done
        fi
    done
}

username=$1
currentPath=$(cd $(dirname $0); pwd -P)
authFile="${currentPath}/dav_svn.authz"
prefixUrl="${currentPath}/prefixUrl"
userRoleFile="${currentPath}/userRoleFile"

rm -f ${userRoleFile}
getUserRole ${username}
sed -i "s/username/${username}/g" ${userRoleFile}

source ${currentPath}/insertRoleToDB.sh
insertUserRoleToDB ${username}
