#! /bin/bash
make
if [[ $# -ne 2 ]]; then
    echo "usage:bash $0 [n_host] [n_player]"
    exit 1
fi #error check

ans=(0 0 0 0 0 0 0 0)  # initial  
host=(0 0 0 0 0 0 0 0 0 0)
score=(0 0 0 0 0 0 0 0 0 0 0 0 0)
M=$1 #host
N=$2 #player

function perm(){
    if (( ${2} > 8 )); then return; fi #check 
    if (( ${1} > $N )) && (( ${2} != 8 )); then return; fi #check 
    if (( ${2} == 8 )); then
        (( count++ ))
        found=0
        for i in $(seq 1 $M); do
            if (( host[$i] == 0 )); then
                host[$i]=1
                echo ${ans[*]} >"fifo_$i.tmp"
                found=1
                break
            fi
        done
        if (( found == 0 )); then
            read key <"fifo_0.tmp"
            for i in $(seq 1 8); do
                read -a playa <"fifo_0.tmp"
                ((score[playa[0]] += 8 - ${playa[1]}))
            done
            for i in $(seq 1 $M); do
                if (( $key == i )); then
                    echo ${ans[*]} >"fifo_$i.tmp"
                    break
                fi
            done
        fi
        return
    fi
    ans[((${2}))]=${1}
    perm $((${1}+1)) $((${2}+1))
    perm $((${1}+1)) $((${2}))
}

for i in $(seq 0 $M); do
    mkfifo "./fifo_$i.tmp"
    exec {fds[$i]}<>"fifo_$i.tmp"#開fifo
done
for i in $(seq 1 $M); do
    ./host $i $i 0 & #開host
done
perm 1 0 #呼叫function  perm 第  組合的第?個數
for i in $(seq 1 $M); do
    if (( host[$i] == 1 )); then
        host[$i]=0
        read key <fifo_0.tmp
        for j in $(seq 1 8); do
            read -a playa <fifo_0.tmp
            (( score[${playa[0]}] += 8 - ${playa[1]} ))
        done
    fi
    echo "-1 -1 -1 -1 -1 -1 -1 -1" >"fifo_$i.tmp"
done
wait
for i in $(seq 1 $N); do
    echo $i ${score[$i]}
done
rm *.tmp