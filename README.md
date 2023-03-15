
## Setup

For our experiments, we will use a cluster of AWS EC2 instances. Reviewers should have been provided with credentials to our AWS environment with compute resources. Reviewers should have also moved `HOLMES.pem` (provided with submission) to `~/.ssh` and set permissions to 400 using `chmod 400 HOLMES.pem`

1. [6 minutes] Make sure python3 is downloaded. 
Install [TexLive/MacTeX](https://tug.org/texlive/), and then run:
```
pip3 install numpy
pip3 install matplotlib
pip3 install scipy
pip3 install pandas
pip3 install latex
```

2. [5 minutes] Install [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) (version 2 works) and run `aws configure` using the instructions [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) (use `us-west-2` as the default region, use `json` as the default output format, and we will directly provide the Access key ID and the secret access key to the reviewers upon submission).

3. [3 minutes] To start a cluster, run the following:
```
cd holmes-artifacts
python3 start_cluster.py
```
This will create the EC2 instances for the experiments using the correct AMI and copy configuration files to each instance. Default TLS keys and certificates are included for testing.

Note: If you see a message that a SSH connection was refused on port 22, then the script was not able to copy over the configuration file because the instance had not fully started yet. In this case, either teardown the cluster and restart (waiting a few minutes between teardown and starting again), or manually copy the configuration files yourself using `scp`.

This will create the EC2 instances for the experiments using the correct AMI and copy the necessary configuration files to each instance.

Note: If you see a message that a SSH connection was refused on port 22, then the script was not able to copy over the configuration file because the instance had not fully started yet. In this case, either teardown the cluster and restart (waiting a few minutes between teardown and starting again), or manually copy the configuration files yourself using `scp`.

4. If you are done for the day, run the following to stop all instances. Note that **stopping the cluster will stop all experiments**, so if your experiments are still running, do not stop the cluster:
```
python3 stop_cluster.py
```
You can then resume the cluster by running the following:
```
python3 resume_cluster.py
```

5. When you are finished with the experiments, tear down the cluster to allow others to run the experiments on the clusters. Note, you can only launch one cluster at once. Otherwise, you will exceed your vCPU limits.
```
python3 teardown_cluster.py
```


## HOLMES Tests

### Unit tests for HOLMES (synchronous only)
```
python3 start_holmes_unit_tests.py
```

### Integration testing workflows for HOLMES (synchronous only)
```
python3 start_holmes_datasets.py
```

## Part 1: Running experiments
We provide an option for those running experiments to run an experiment both asynchronously and synchronously. Asynchronous is recommended over synchronous. We have a coordinator VM that remains online for the entire time, allowing you to disconnect from your local machine whenever you’d like and still have the experiment run. Synchronous requires you to remain connected to the AMI instance on your local machine at all times.

Those who wish to run the scripts asynchronously (recommended) can continue to run experiments without staying connected to the AMI instances over ssh on their local machine, and is the recommended method of running experiments, especially for long experiments. However, you **must run asynchronous scripts one at a time**, since most scripts are designed to kill existing processes and scripts. Furthermore, this will hide any standard output that the experiment script outputs, which can be helpful for debugging.

The only scripts that you are required to run synchronously are the unit tests and the integration tests (dataset testing workflows). This is intended since reading the output is an integral part of these tests.

Run all of these experiments in order, since future experiments can depend on experiments.


### Easy 1-piece script that runs all experiments:
If you want a hands-off approach, we have provided an easy one-run script that will run all the experiments asynchronously with the coordinator. 

It will take over 24 hours for all the experiments to run, and mistakes may occur when running all experiments all at once.

```
python3 start_coordinator_all.py
```

Then, you can skip to the “Retrieving benchmark results”

### SPDZ Offline Throughput Benchmarking [~1 hour]
Most future experiments will depend on the SPDZ offline throughput for computing the offline input loading cost, or for the offline phase commonly associated with MPC. We also compute the pairwise 2PC offline throughput for SPDZ, which will be used for the pairwise 2PC experiments.

To run asynchronously:
```
python3 start_coordinator_spdz_bench.py [30 minutes]
# wait at least 30 minutes for the script to complete
python3 start_coordinator_spdz_2pc_bench.py [15 minutes]
# wait at least 15 minutes for the script to complete
```

To run synchronously:
```
python3 start_spdz_bench.py
python3 start_spdz_2pc_bench.py
```
### Misc Bench Scripts (Experiment E1 + E2)

To run the evaluations for the group check (E1), trimmed mean (E1), mean and variance (E1), and the multidimensional test comparisons (E2), you will need to run the `misc` bench scripts.

To run asynchronously:
```
python3 start_coordinator_mpc_misc.py [1 hour]
# wait at least 1 hour for the script to complete
python3 start_coordinator_zk_misc.py [45 minutes]
# wait at least 45 minutes for the script to complete
```

To run synchronously:
```
python3 start_mpc_misc.py
python3 start_zk_misc.py
```

### Range checks and ZK-friendly sketching against the Baselines (Experiment E3)

To run the main evaluations for HOLMES vs. the baselines, run the `bench` scripts.

To run asynchronously:
```
python3 start_coordinator_mpc_bench.py [7 hours]
# wait at least 7 hours for the script to complete
python3 start_coordinator_2pc_bench.py [2 hours]
# wait at least 2 hours for the script to complete
python3 start_coordinator_spartan.py [3 hours]
# wait at least 3 hours for the script to complete
python3 start_coordinator_zk_bench.py [15 minutes]
# wait at least 15 minutes for the script to complete
```

To run synchronously:
```
python3 start_2pc_bench.py
python3 start_mpc_bench.py
python3 start_spartan_bench.py
python3 start_zk_bench.py
```

### Statistical corruption accuracy graphs (Experiment E4)
To run the graphs, you will just need to run the benchmarks, which will run the graphs for both corrupting the simulated and real dataset on the auxiliary server, and create csv files as output which you can plot further down. For the chi-squared tests, we have decreased the granularity of the tests to 50 poisons per iteration to save time, but you can increase the granularity in the code [here](https://github.com/holmes-inputcheck/holmes-stat/blob/main/graph/graph_chi_squared.cpp#L296) and [here](https://github.com/holmes-inputcheck/holmes-stat/blob/main/graph/graph_chi_squared_dataset1.cpp) by editing the `e_iters` value.

To run asynchronously:
```
python3 start_coordinator_stat_graphs.py [10 minutes]
# wait at least 10 minutes for the script to complete
```

To run synchronously:
```
python3 start_stat_graphs.py
```

### Marketing dataset testing workflow benchmarking (Experiment E5)
This experiment will run the bank marketing dataset with JL value k=40 for both N-party MPC and HOLMES (QuickSilver). In the paper, we have used k=200 for the graph, providing a much higher overhead for the 10-party MPC case, but we decided to lower the value to k=40 to save benchmarking time, and the accuracy threshold suffices for its number of entries (41000 entries).

To run asynchronously:
```
python3 start_coordinator_mpc_marketing.py [35 minutes]
# wait at least 35 minutes for script to complete
python3 start_coordinator_zk_marketing.py [5 minutes]
# wait at least 5 minutes for script to complete
```

To run synchronously:
```
python3 start_mpc_marketing.py
python3 start_zk_marketing.py
```


## Part 2: Retrieving benchmark results

In the section, you will automatically fetch the files and raw, unfiltered benchmark results onto your local machine with the provided scripts, and perform some pre-processing to make it much easier to graph. This will **not** create the plots or the graphs (wait till we get to the "Evaluating the experiment plots" section for that!) directly however, but will create .csv files from the results.

### Easy 1-piece script that retrieves all benchmark results:
If you want a hands-off approach, we have provided an easy one-run script that will retrieve all the benchmark results for all of the experiments. You will need to successfully and completely run all the experiments before you can do this (you should wait at least 24 hours from whenever you ran `python3 start_coordinator_all.py`, or ensure you've run all the experiments above successfully)

```
./retrieve-all.sh
```

### Misc Bench Scripts (Experiment E1 + E2)
```
python3 retrieve_mpc_misc.py [< 1 minute]
python3 retrieve_zk_misc.py [< 1 minute]
```

### Range checks and ZK-friendly sketching against the Baselines (Experiment E3)
```
python3 retrieve_mpc_bench.py [< 1 minute]
python3 retrieve_2pc_bench.py [< 1 minute]
python3 retrieve_nizk_bench.py [< 1 minute]
python3 retrieve_snark_bench.py [< 1 minute]
python3 retrieve_zk_bench.py [< 1 minute]
```

### Statistical corruption accuracy graphs (Experiment E4)
No need for these! :) You can skip straight to "Evaluating the experiment plots"!

### Marketing dataset testing workflow benchmarking (Experiment E5)
```
python3 retrieve_marketing.py [ < 1 minute]
```

## Part 3: Plotting the experiment results

In this section, we transform the CSV files fetched and parsed in the last step into the graphs and plots.

### Easy 1-piece script that plots everything:
If you want a hands-off approach, we have provided an easy one-run script that will plot . If you see that the `./retrieve-all.sh` script has not returned any errors, you can retrieve all the plots in one-shot! Feel free to run this script to make everything easier.

```
./plot-all.sh
```

### Classical distribution tests (Experiment E1)
```
python3 plot_group_check.py
python3 plot_mean_variance.py
python3 plot_trimmed_mean_check.py
```
Produces `plot_group_check_quicksilver.pdf`, `plot_group_check_mpc.pdf`, `plot_mean_variance_quicksilver.pdf`, `plot_mean_variance_mpc.pdf`, `plot_trimmed_mean_quicksilver.pdf`, and `plot_trimmed_mean_mpc.pdf`

### HOLMES Multidimensional Test vs. Naive Multidimensional Test (Experiment E2)
```
python3 plot_jl_varying_num_dim.py
python3 plot_jl_varying_size_dim.py
```
Produces `plot_jl_varying_num_dim.pdf` and `plot_jl_varying_size_dim.pdf`

### Range Checks and ZK-friendly sketching against the baselines (Experiment E3)
```
python3 plot_bench.py
```
Produces `range_all.csv` and `jl_all.csv`

### Statistical p-value accuracy graphs (Experiment E4)
```
python3 plot_simulated_dataset_graph.py
python3 plot_real_dataset_graph.py
```
Produces `simulated_dataset_stat_graph.pdf` and `real_dataset_stat_graph.pdf`

### Marketing dataset graphs (HOLMES vs. MPC Baseline) (Experiment E5)
```
python3 plot_marketing_dataset.py
```
Produces `plot_marketing_dataset_quicksilver.pdf` and `plot_marketing_dataset_mpc.pdf`


