#!/bin/bash
if [[ ${UID} != 0 ]];then
    printf "File Must run as ROOT.\n"; exit
fi 

args(){
    NODES="$1"
    USER=root
    KEY_FILE="/${USER}/.ssh/id_ed25519"
}


ssh_keygen(){
    if ssh-keygen -t ed25519 -N '' -f ${KEY_FILE} <<< 'y' &> /dev/null;then
        printf "[+] SSH Key : ${KEY_FILE} generated\n"
    else
        printf "[+] SSH Key Gen Failed\nExiting....\n"
        exit 10
    fi 
}

ssh_keyshare(){
    if sshpass -V &> /dev/null;then
    all_nodes=( $(awk -F':' '{print $NF}' ${NODES}))
    # NF :- NF is used to Print Number of Fields.
    ips=()
        for ip in ${all_nodes[@]};do
            if sshpass -p "1234" ssh-copy-id -o 'StrictHostKeyChecking=no' -f -i ${KEY_FILE} ${USER}@${ip} &> /dev/null;then
                # StrictHostKeyChecking is used for not prompting the figerprint(yes/no) 
                ips+=("${ip}")
                printf "[+] ${ip} : SSH Key shared successfully.\n"
            fi
        done
    else
        printf "[-] Do Install sshpass\n"
        exit
    fi
}


ssh_hosts(){
    for i in $(!ips[@]);do
        if [[ $(grep "${ips[$i]}" ${NODES}) =~ ^m ]];then # =~ is used for Regex matching
            printf "${ips[$i]}\tmaster${i}\n" >> /etc/hosts
        elif [[ $(grep "${ips[$i]}" ${NODES}) =~ ^c ]];then
            printf "${ips[$i]}\tcompute${i}\n" >> /etc/hosts
        fi
    done
    for i in ${!ips[@]};do
        scp -i ${KEY_FILE} -o 'StrictHostKeyChecking=no' -r /etc/hosts "${USER}@${ips[$i]}:/etc/hosts"
    done
}

args $a 


if [[ -f ${NODES} ]] && [[ ! -z ${NODES} ]] && [[ -r ${NODES} ]];then
    # -f :- Is Used to Check whether the File Exists or Not.
    # -z :- Is Used to Check whether the File is Empty or Not.
    # -r :- Is Used to Check whether the File is Readable or Not.
    ssh_keygen
    ssh_keyshare
    ssh_hosts
else
    printf "[-] Please provide correct ip list.\n"
    exit
fi 

