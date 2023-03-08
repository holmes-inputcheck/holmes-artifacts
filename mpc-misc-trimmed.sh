#!/bin/bash
FILE0=trimmed_mpc.csv

t1="trimmed_mean_100k_8"
t2="trimmed_mean_200k_8"

t3="trimmed_mean_100k_12"
t4="trimmed_mean_200k_12"

t5="trimmed_mean_100k_16"
t6="trimmed_mean_200k_16"

t7="trimmed_mean_100k_20"
t8="trimmed_mean_200k_20"

t9="trimmed_mean_100k_24"
t10="trimmed_mean_200k_24"


#if [ ! -f "$FILE0" ]; then
#    printf "protocol,threshold,100k,200k\n" > $FILE0
#fi

printf "protocol,threshold,100k,200k\n" > $FILE0

./mamba-setup.sh
v1=$(./Player.x $1 Programs/$t1 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v2=$(./Player.x $1 Programs/$t2 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "mpc,8,%s,%s\n" $v1 $v2 >> $FILE0

v3=$(./Player.x $1 Programs/$t3 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v4=$(./Player.x $1 Programs/$t4 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
printf "mpc,12,%s,%s\n" $v3 $v4 >> $FILE0

v5=$(./Player.x $1 Programs/$t5 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v6=$(./Player.x $1 Programs/$t6 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "mpc,16,%s,%s\n" $v5 $v6 >> $FILE0

v7=$(./Player.x $1 Programs/$t7 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v8=$(./Player.x $1 Programs/$t8 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "mpc,20,%s,%s\n" $v7 $v8 >> $FILE0

v9=$(./Player.x $1 Programs/$t9 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v10=$(./Player.x $1 Programs/$t10 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
printf "mpc,24,%s,%s\n" $v9 $v10 >> $FILE0

echo "finished trimmed mean checks"
# ~ 10 minutes
