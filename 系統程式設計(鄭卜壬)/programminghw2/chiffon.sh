#!/bin/bash
#bash chiffon.sh -m [n_hosts] -n [n_players] -l [lucky_number]

if [ $# -ne 6 ]; then # check argc==6 / -ne-->兩數值不等 / $#-->argc
    echo "usage:bash chiffon.sh -m [n_hosts] -n [n_players] -l [lucky_number]"
    exit 1
fi

declare -i Host
declare -i player
declare -i lucky

if [ "${1}" == "-m" ]; then # check host
    Host=${2}
elif [ "${3}" == "-m" ]; then
    Host=${4}
elif [ "${5}" == "-m" ]; then
    Host=${6}
else
    echo "ID error"
    exit 1
fi

if [ "${1}" == "-n" ]; then # check player
    player=${2}
elif [ "${3}" == "-n" ]; then
    player=${4}
elif [ "${5}" == "-n" ]; then
    player=${6}
else
    echo "player error"
    exit 1
fi

if [ "${1}" == "-l" ]; then # check lucky
    lucky=${2}
elif [ "${3}" == "-l" ]; then
    lucky=${4}
elif [ "${5}" == "-l" ]; then
    lucky=${6}
else
    echo "lucky error"
    exit 1
fi

for i in $(seq 0 10); do # 開fifo，維持fifo
    mkfifo fifo_$i.tmp
done

exec 3<>fifo_0.tmp
exec 4<>fifo_1.tmp
exec 5<>fifo_2.tmp
exec 6<>fifo_3.tmp
exec 7<>fifo_4.tmp
exec 8<>fifo_5.tmp
exec 9<>fifo_6.tmp
exec 10<>fifo_7.tmp
exec 11<>fifo_8.tmp
exec 12<>fifo_9.tmp
exec 13<>fifo_10.tmp

for i in $(seq 1 $Host); do # 開host
    ./host "-m" ${i} "-d" 0 "-l" ${lucky} &
    #echo ${i} ${lucky}
done
#echo "ddddd"
declare -i cnt=1
declare -a player8

for a in $(seq 1 ${player}); do
for b in $(seq $((${a} + 1))  ${player}); do
for c in $(seq $((${b} + 1))  ${player}); do
for d in $(seq $((${c} + 1))  ${player}); do
for e in $(seq $((${d} + 1))  ${player}); do
for f in $(seq $((${e} + 1))  ${player}); do
for g in $(seq $((${f} + 1))  ${player}); do
for h in $(seq $((${g} + 1))  ${player}); do
player8[${cnt}]="${a} ${b} ${c} ${d} ${e} ${f} ${g} ${h}" #列出所有組合
#echo ${player8[${cnt}]} "check player8"
cnt=$((${cnt}+1))
done;done;done;done;done;done;done;done



cnt=$((${cnt}-1))
#echo ${cnt} "cnt"
if [ ${cnt} -lt ${Host} ]; then
    for i in $(seq $((${cnt}+1)) ${Host}); do
    echo "-1 -1 -1 -1 -1 -1 -1 -1" > fifo_${i}.tmp
done
     Host=${cnt}
fi

declare -i hostid=0
declare -i playerid=0
declare -i score=0
declare -i totalscore=0
declare -a finalscore

#for i in $(seq 1 ${Host}); do
   # echo ${player8[$[i]]} "check 8"
#done

for i in $(seq 1 ${Host}); do
    echo ${player8[$[i]]} > fifo_${i}.tmp
done

for i in $(seq 1 ${player}); do
    finalscore[${i}]=0
done


for i in $(seq $((${Host}+1)) ${cnt}); do
     read hostid < fifo_0.tmp
     for j in $(seq 1 8); do
         read playerid totalscore < fifo_0.tmp
         finalscore[${playerid}]=$((${finalscore[${playerid}]}+${totalscore}))
    done
    #echo ${player8[$[i]]}
    echo ${player8[$[i]]}  > fifo_${hostid}.tmp
done

for i in $(seq 1 ${Host}); do
    read hostid<fifo_0.tmp
    #echo ${hostid} "hostid"
     for j in $(seq 1 8); do
         read playerid totalscore<fifo_0.tmp
         #echo ${playerid} ${totalscore} "bb"
         finalscore[${playerid}]=$((${finalscore[${playerid}]}+${totalscore}))
    done
    echo "-1 -1 -1 -1 -1 -1 -1 -1" > fifo_${hostid}.tmp
done

#echo ${finalscore[*]}

declare -a rank

for i in $(seq 1 ${player}); do
     rank[${i}]=0
done

declare -i max=1
declare -i i=1
while  [ ${i} -le ${player} ]
do
    # echo $i "i start"
     for j in $(seq 1 ${player}); do
            if [ ${finalscore[${max}]} -lt  ${finalscore[${j}]} ]; then
                max=${j}
            fi
     done
     
     # echo ${max} ${finalscore[${max}]} ${i} "check max"
      #echo ${finalscore[*]}
     if [ ${finalscore[${max}]} -lt 0 ]; then
     break
     fi
     declare -i maxscore=${finalscore[${max}]}
     declare -i consi=${i}
     #echo ${consi}
     for j in $(seq 1 ${player}); do
            if [ ${finalscore[${j}]} -eq ${maxscore} ]; then
                rank[${j}]=${consi}
                finalscore[${j}]=-1
                i=$((${i}+1))
            fi
     done
     #echo $i "i"
done

for i in $(seq 1 ${player}); do
      echo -e ${i} ${rank[${i}]}
done

wait
rm *.tmp