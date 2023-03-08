#!/bin/bash
python3 retrieve_2pc_bench.py;
python3 retrieve_mpc_bench.py;
python3 retrieve_nizk_bench.py;
python3 retrieve_snark_bench.py;
python3 retrieve_zk_bench.py;

python3 retrieve_mpc_misc.py;
python3 retrieve_zk_misc.py;

python3 retrieve_marketing.py