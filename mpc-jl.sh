#!/bin/bash
FILE0=jl_10000_mpc.txt
t1="jl_10k_dim1_size10"
t2="jl_10k_dim4_size10"
t3="jl_10k_dim4_size50"

FILE1=jl_20000_mpc.txt
t4="jl_20k_dim1_size10"
t5="jl_20k_dim4_size10"
t6="jl_20k_dim4_size50"

# Comment bc there will be different outputs in different folders for different parties (2, 6, 10)
#if [ ! -f "$FILE0" ]; then
printf "%s,%s,%s\n" $t1 $t2 $t3 > $FILE0
#fi

#if [ ! -f "$FILE1" ]; then
printf "%s,%s,%s\n" $t4 $t5 $t6 > $FILE1
#fi

./mamba-setup.sh
v1=$(./Player.x $2 Programs/$t1 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v2=$(./Player.x $2 Programs/$t2 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v3=$(./Player.x $2 Programs/$t3 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "%s,%s,%s\n" $v1 $v2 $v3 >> $FILE0

v4=$(./Player.x $2 Programs/$t4 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v5=$(./Player.x $2 Programs/$t5 | sed -e '/Online Time/b' -e d | awk '{print $4}')
v6=$(./Player.x $2 Programs/$t6 | sed -e '/Online Time/b' -e d | awk '{print $4}')
printf "%s,%s,%s\n" $v4 $v5 $v6 >> $FILE1