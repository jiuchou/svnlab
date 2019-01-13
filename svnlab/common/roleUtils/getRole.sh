#!/bin/bash

getRoleByIdentify() {
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
    path=$(grep "]" temp | tail -n 1 | awk -F ':/' '{print $1}' | awk -F ']' '{print $1}')
    prefix_url=$(sed -n "/${module}/p" prefixUrl | awk -F '=' '{print $2}')
    url=${prefix_url}${module}/${path}
    rm temp

    echo "username,${role},${module},${path},${url},${manager}" >> ${userRoleFile}
}

getRole() {
    username=$1
    lineContents=$(grep -rn "${username}" ${authFile})
    for lineContent in ${lineContents[@]}; do
        identify=$(echo "${lineContent}" | awk -F ':' '{print $2}' | awk -F '=' '{print $1}')
        if [[ "${identify}" == "${username}" ]]; then
            # 用户
            getRoleByIdentify "${lineContent}"
        else
            # 组
            groupname=${identify}
            groupLineContents=$(grep -rn "^@${groupname}=" ${authFile})
            for groupLineContent in ${groupLineContents[@]}; do
                getRoleByIdentify "${groupLineContent}"
            done
        fi
    done
}

username=$1
authFile="dav_svn.authz"
userRoleFile="userRoleFile"

rm -f ${userRoleFile}
getRole ${username}
sed -i "s/username/${username}/g" ${userRoleFile}
