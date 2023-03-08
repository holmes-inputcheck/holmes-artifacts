#!/bin/bash
FILE0=marketing_mpc.txt

./mamba-setup.sh
v1=$(./Player.x $2 Programs/dataset_1 | sed -e '/Online Time/b' -e d | awk '{print $4}') 
printf "%s\n" $v1  > $FILE0