#!/bin/bash
FILE0=hist_mpc.csv

t1="histogram_numeric_100k_16_10b"
t2="histogram_numeric_200k_16_10b"
t3="histogram_numeric_200k_16_20b"

t4="histogram_numeric_100k_64_10b"
t5="histogram_numeric_200k_64_10b"
t6="histogram_numeric_200k_64_20b"

t7="histogram_numeric_100k_256_10b"
t8="histogram_numeric_200k_256_10b"
t9="histogram_numeric_200k_256_20b"

t10="histogram_numeric_100k_1024_10b"
t11="histogram_numeric_200k_1024_10b"
t12="histogram_numeric_200k_1024_20b"

t13="histogram_numeric_100k_4096_10b"
t14="histogram_numeric_200k_4096_10b"
t15="histogram_numeric_200k_4096_20b"


#if [ ! -f "$FILE0" ]; then
#    printf "protocol,groupsize,100k_10b,200k_10b,200k_20b\n" > $FILE0
#fi

printf "protocol,groupsize,100k_10b,200k_10b,200k_20b\n" > $FILE0

./mamba-setup.sh
v1=$(./Player.x $1 Programs/$t1 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v2=$(./Player.x $1 Programs/$t2 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v3=$(./Player.x $1 Programs/$t3 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "mpc,4,%s,%s,%s\n" $v1 $v2 $v3 >> $FILE0

v4=$(./Player.x $1 Programs/$t4 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v5=$(./Player.x $1 Programs/$t5 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v6=$(./Player.x $1 Programs/$t6 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "mpc,6,%s,%s,%s\n" $v4 $v5 $v6 >> $FILE0

v7=$(./Player.x $1 Programs/$t7 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v8=$(./Player.x $1 Programs/$t8 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v9=$(./Player.x $1 Programs/$t9 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "mpc,8,%s,%s,%s\n" $v7 $v8 $v9 >> $FILE0

v10=$(./Player.x $1 Programs/$t10 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v11=$(./Player.x $1 Programs/$t11 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v12=$(./Player.x $1 Programs/$t12 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "mpc,10,%s,%s,%s\n" $v10 $v11 $v12 >> $FILE0

v13=$(./Player.x $1 Programs/$t13 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v14=$(./Player.x $1 Programs/$t14 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v15=$(./Player.x $1 Programs/$t15 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "mpc,12,%s,%s,%s\n" $v13 $v14 $v15 >> $FILE0

echo "finished histogram checks"
# ~ 30 minutes

