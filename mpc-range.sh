#!/bin/bash
FILE0=range_100000_mpc.txt
t0="num_parties"
t1="range_check_100k_8"
t2="range_check_100k_12"
t3="range_check_100k_16"
t4="range_check_100k_20"
t5="range_check_100k_24"

FILE1=range_200000_mpc.txt
t6="range_check_200k_8"
t7="range_check_200k_12"
t8="range_check_200k_16"
t9="range_check_200k_20"
t10="range_check_200k_24"

FILE2=range_500000_mpc.txt
t11="range_check_500k_8"
t12="range_check_500k_12"
t13="range_check_500k_16"
t14="range_check_500k_20"
t15="range_check_500k_24"

# Comment bc there will be different outputs in different folders for different parties (2, 6, 10)
#if [ ! -f "$FILE0" ]; then
printf "%s,%s,%s,%s,%s\n" $t1 $t2 $t3 $t4 $t5 > $FILE0
#fi

#if [ ! -f "$FILE1" ]; then
printf "%s,%s,%s,%s,%s\n" $t6 $t7 $t8 $t9 $t10 > $FILE1
#fi

#if [ ! -f "$FILE2" ]; then
printf "%s,%s,%s,%s,%s\n" $t11 $t12 $t13 $t14 $t15 > $FILE2
#fi

./mamba-setup.sh
v1=$(./Player.x $2 Programs/$t1 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v2=$(./Player.x $2 Programs/$t2 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v3=$(./Player.x $2 Programs/$t3 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v4=$(./Player.x $2 Programs/$t4 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v5=$(./Player.x $2 Programs/$t5 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "%s,%s,%s,%s,%s\n" $v1 $v2 $v3 $v4 $v5 >> $FILE0

v6=$(./Player.x $2 Programs/$t6 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v7=$(./Player.x $2 Programs/$t7 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v8=$(./Player.x $2 Programs/$t8 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v9=$(./Player.x $2 Programs/$t9 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v10=$(./Player.x $2 Programs/$t10 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "%s,%s,%s,%s,%s\n" $v6 $v7 $v8 $v9 $v10 >> $FILE1

v11=$(./Player.x $2 Programs/$t11 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v12=$(./Player.x $2 Programs/$t12 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v13=$(./Player.x $2 Programs/$t13 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v14=$(./Player.x $2 Programs/$t14 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v15=$(./Player.x $2 Programs/$t15 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "%s,%s,%s,%s,%s\n" $v11 $v12 $v13 $v14 $v15 >> $FILE2