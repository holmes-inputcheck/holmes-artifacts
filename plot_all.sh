#!/bin/bash
python3 plot_bench.py

python3 plot_jl_varying_num_dim.py
python3 plot_jl_varying_size_dim.py

python3 plot_group_check.py
python3 plot_trimmed_mean_check.py
python3 plot_mean_variance.py

python3 plot_real_dataset_graph.py
python3 plot_simulated_dataset_graph.py

python3 plot_marketing_dataset.py
