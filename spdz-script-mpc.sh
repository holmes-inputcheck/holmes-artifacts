FILE=spdz-mpc-p$1-throughput.out
./pairwise-offline.x -N $1 -p $2 -f 64 -x 32 -h $3 | sed -e '/Throughput:/b' -e d | awk '{print $2}' > $FILE