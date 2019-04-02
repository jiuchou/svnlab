#!/bin/bash

authfile=$1
module=$2
path=$3
user=$4
new_role=$5

cp ${authfile} ${authfile}_backup
path_position=$(grep -rn "\[${module}\:\/${path}\]" ${authfile}_backup | awk -F ':' '{print $1}')
user_positions=$(grep -rn ${user} ${authfile}_backup | awk -F ':' '{print $1}')
for user_position in ${user_positions[@]}; do
    if [[ ${path_position} -lt ${user_position} ]]; then
        break
    fi
done

echo ${user_position}
if [[ ${new_role} -eq 1 ]]; then
    sed -i "${user_position}s/${user}=.*/${user}=r/" ${authfile}_backup
elif [[ ${new_role} -eq 0 ]]; then
    sed -i "${user_position} d" ${authfile}_backup
fi

change_line=$(diff ${authfile}_backup ${authfile} | grep '>' | wc -l)
if [[ ${change_line} -eq 1 ]]; then
    cp ${authfile}_backup ${authfile}
    exit 0
else
    exit 1
fi
