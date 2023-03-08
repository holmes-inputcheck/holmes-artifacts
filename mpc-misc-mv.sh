#!/bin/bash
FILE0=mv_mpc.csv

t1="mean_check_100p_1"
t2="variance_check_100p_1"

t3="mean_check_100p_2"
t4="variance_check_100p_2"

t5="mean_check_100p_3"
t6="variance_check_100p_3"

t7="mean_check_100p_4"
t8="variance_check_100p_4"

t9="mean_check_100p_5"
t10="variance_check_100p_5"


#if [ ! -f "$FILE0" ]; then
#    printf "protocol,num_instances,mv\n" > $FILE0
#fi

printf "protocol,num_instances,mv\n" > $FILE0

./mamba-setup.sh
v1=$(./Player.x $1 Programs/$t1 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v2=$(./Player.x $1 Programs/$t2 | sed -e '/Online Time/b' -e d | awk '{print $4}')
s1=`echo $v1+$v2 | bc`
printf "mpc,1000000,%0.2f\n" $s1 >> $FILE0

v3=$(./Player.x $1 Programs/$t3 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v4=$(./Player.x $1 Programs/$t4 | sed -e '/Online Time/b' -e d | awk '{print $4}')
s2=`echo $v3+$v4 | bc`
printf "mpc,2000000,%0.2f\n" $s2 >> $FILE0

v5=$(./Player.x $1 Programs/$t5 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v6=$(./Player.x $1 Programs/$t6 | sed -e '/Online Time/b' -e d | awk '{print $4}')
s3=`echo $v5+$v6 | bc`
printf "mpc,3000000,%0.2f\n" $s3 >> $FILE0

v7=$(./Player.x $1 Programs/$t7 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v8=$(./Player.x $1 Programs/$t8 | sed -e '/Online Time/b' -e d | awk '{print $4}')
s4=`echo $v7+$v8 | bc`
printf "mpc,4000000,%0.2f\n" $s4 >> $FILE0

v9=$(./Player.x $1 Programs/$t9 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
v10=$(./Player.x $1 Programs/$t10 | sed -e '/Online Time/b' -e d | awk '{print $4}')
s5=`echo $v9+$v10 | bc`
printf "mpc,5000000,%0.2f\n" $s5 >> $FILE0

echo "finished mean+variance checks"
# ~ 15 minutes

