#!/bin/bash
EMP_MY_PARTY_ID=$1 python3 bench-scripts/bench_trimmed_mean.py
EMP_MY_PARTY_ID=$1 python3 bench-scripts/bench_histogram_numeric.py
EMP_MY_PARTY_ID=$1 python3 bench-scripts/bench_mean_check.py
EMP_MY_PARTY_ID=$1 python3 bench-scripts/bench_variance_check.py

EMP_MY_PARTY_ID=$1 python3 bench-scripts/bench_jl_varying_num_dim.py
EMP_MY_PARTY_ID=$1 python3 bench-scripts/bench_jl_varying_size_dim.py
EMP_MY_PARTY_ID=$1 python3 bench-scripts/bench_strawman_jl_varying_num_dim.py
EMP_MY_PARTY_ID=$1 python3 bench-scripts/bench_strawman_jl_varying_size_dim.py