FILE=spdz-2pc-p$1-throughput.out
MULT="$(($1-1))"
./pairwise-offline.x -N 2 -p $2 -f 64 -x $3 -h $4 | sed -e '/Throughput:/b' -e d | awk "{print \$2 * $MULT}" > $FILE
