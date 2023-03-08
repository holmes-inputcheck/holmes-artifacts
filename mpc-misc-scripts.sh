# --- start histogram / group checks ---
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

printf "protocol,groupsize,100k_10b,200k_10b,200k_20b\n" > $FILE0

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

# --- start trimmed mean checks ---

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

printf "protocol,threshold,100k,200k\n" > $FILE0

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

# --- start mean + variance checks ---
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