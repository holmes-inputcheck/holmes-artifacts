import sys, string, json, os, math
from benchClient import generateRemoteCmdStr, getThroughput
import subprocess

def checkBenchComplete(labels, d):
    if len(labels) == len(d.keys()):
        return True
    else:
        return False
username = "ubuntu"

f_config = open('system.config')
config = json.load(f_config)
f_config.close()

auxID = config["AuxID"]
followerIDs = [config["Followers"][i]["ID"] for i in range(len(config["Followers"]))]
auxPublicAddr = config["AuxPublicAddr"]
followerPublicAddrs = [config["Followers"][i]["PublicAddr"] for i in range(len(config["Followers"]))]
followerPrivateAddrs = [config["Followers"][i]["PrivateAddr"] for i in range(len(config["Followers"]))]
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
throughput = getThroughput()


cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/HOLMES/holmes-library/all_results.txt .") % (keyPath, followerPublicAddrs[0])
process = subprocess.Popen(cmd, shell=True)
process.wait()

hist_100k_10b_labels = ["bench_histogram_numeric 100000 10 16", "bench_histogram_numeric 100000 10 64", "bench_histogram_numeric 100000 10 256", "bench_histogram_numeric 100000 10 1024", "bench_histogram_numeric 100000 10 4096"]
hist_200k_10b_labels = ["bench_histogram_numeric 200000 10 16", "bench_histogram_numeric 200000 10 64", "bench_histogram_numeric 200000 10 256", "bench_histogram_numeric 200000 10 1024", "bench_histogram_numeric 200000 10 4096"]
hist_200k_20b_labels = ["bench_histogram_numeric 200000 20 16", "bench_histogram_numeric 200000 20 64", "bench_histogram_numeric 200000 20 256", "bench_histogram_numeric 200000 20 1024", "bench_histogram_numeric 200000 20 4096"]

hist_100k_10b_times = {}
hist_200k_10b_times = {}
hist_200k_20b_times = {}
group_sizes = [4, 6, 8, 10, 12]

f_config = open('all_results.txt', 'r')
f_config_lines = f_config.readlines()
for i in range(len(f_config_lines)):
    line = f_config_lines[i].rstrip()
    if line in hist_100k_10b_labels:
        group_size = math.log2(int(line.split(' ')[3]))
        # offline input cost for consistency check (SPDZ)
        hist_100k_10b_times[group_size] = float(line.split()[1]) / 2 / throughput
        # online time (QuickSilver)
        hist_100k_10b_times[group_size] += float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in hist_200k_10b_labels:
        group_size = math.log2(int(line.split(' ')[3]))
        # offline input cost for consistency check (SPDZ)
        hist_200k_10b_times[group_size] = float(line.split()[1]) / 2 / throughput
        # online time (QuickSilver)
        hist_200k_10b_times[group_size] += float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in hist_200k_20b_labels:
        group_size = math.log2(int(line.split(' ')[3]))
        # offline input cost for consistency check (SPDZ)
        hist_200k_20b_times[group_size] = float(line.split()[1]) / 2 / throughput
        # online time (QuickSilver)
        hist_200k_20b_times[group_size] += float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
f_config.close()

if not (checkBenchComplete(hist_100k_10b_labels, hist_100k_10b_times) and checkBenchComplete(hist_200k_10b_labels, hist_200k_10b_times) and checkBenchComplete(hist_200k_20b_labels, hist_200k_20b_times)):
    print("QuickSilver benchmarks didn't finish! Please re-run `python3 start_coordinator_zk_misc.py` or `python3 start_zk_misc.py`!")
    exit

hist_header = "protocol,groupsize,100k_10b,200k_10b,200k_20b\n"
f = open('hist_quicksilver.csv', 'w')
f.write(hist_header)
for group_size in group_sizes:
    f.write('QuickSilver,')
    f.write(str(group_size) + ',' + str(hist_100k_10b_times[group_size]) + ',' + str(hist_200k_10b_times[group_size]) + ',' + str(hist_200k_20b_times[group_size]) + '\n')
f.close()

trimmed_100k_labels = ["bench_trimmed_mean 100000 100 256", "bench_trimmed_mean 100000 100 4096", "bench_trimmed_mean 100000 100 65536", "bench_trimmed_mean 100000 100 1048576", "bench_trimmed_mean 100000 100 16777216"]
trimmed_200k_labels = ["bench_trimmed_mean 200000 100 256", "bench_trimmed_mean 200000 100 4096", "bench_trimmed_mean 200000 100 65536", "bench_trimmed_mean 200000 100 1048576", "bench_trimmed_mean 200000 100 16777216"]

trimmed_100k_times = {}
trimmed_200k_times = {}
thresholds = [8, 12, 16, 20, 24]

f_config = open('all_results.txt', 'r')
f_config_lines = f_config.readlines()
for i in range(len(f_config_lines)):
    line = f_config_lines[i].rstrip()
    if line in trimmed_100k_labels:
        threshold = math.log2(int(line.split(' ')[3]))
        # offline input cost for consistency check (SPDZ)
        trimmed_100k_times[threshold] = float(line.split()[1]) / 2 / throughput
        # online time (QuickSilver)
        trimmed_100k_times[threshold] += float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in trimmed_200k_labels:
        threshold = math.log2(int(line.split(' ')[3]))
        # offline input cost for consistency check (SPDZ)
        trimmed_200k_times[threshold] = float(line.split()[1]) / 2 / throughput
        # online time (QuickSilver)
        trimmed_200k_times[threshold] += float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
f_config.close()

if not (checkBenchComplete(trimmed_100k_labels, trimmed_100k_times) and checkBenchComplete(trimmed_200k_labels, trimmed_200k_times)):
    print("QuickSilver benchmarks didn't finish! Please re-run start_zk_bench.py")
    exit

trimmed_header = "protocol,threshold,100k,200k\n"
f = open('trimmed_quicksilver.csv', 'w')
f.write(trimmed_header)
for threshold in thresholds:
    f.write('QuickSilver,')
    f.write(str(threshold) + ',' + str(trimmed_100k_times[threshold]) + ',' + str(trimmed_200k_times[threshold]) + '\n')
f.close()


mean_labels = ["bench_mean_check 1000000 100", "bench_mean_check 2000000 100", "bench_mean_check 3000000 100", "bench_mean_check 4000000 100", "bench_mean_check 5000000 100"]
variance_labels = ["bench_variance_check 1000000 100", "bench_variance_check 2000000 100", "bench_variance_check 3000000 100", "bench_variance_check 4000000 100", "bench_variance_check 5000000 100"]
instance_sizes = [1000000, 2000000, 3000000, 4000000, 5000000]
mean_times = {}
variance_times = {}
f_config = open('all_results.txt', 'r')
f_config_lines = f_config.readlines()
for i in range(len(f_config_lines)):
    line = f_config_lines[i].rstrip()
    if line in mean_labels:
        instance_size = int(line.split(' ')[1])
        # offline input cost for consistency check (SPDZ)
        mean_times[instance_size] = float(line.split()[1]) / 2 / throughput
        # online time (QuickSilver)
        mean_times[instance_size] += float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in variance_labels:
        instance_size = int(line.split(' ')[1])
        variance_times[instance_size] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
f_config.close()

if not (checkBenchComplete(mean_labels, mean_times) and checkBenchComplete(variance_labels, variance_times)):
    print("QuickSilver benchmarks didn't finish! Please re-run start_zk_bench.py")
    exit

mv_header = "protocol,num_instances,mv\n"
f = open('mv_quicksilver.csv', 'w')
f.write(mv_header)
for instance_size in instance_sizes:
    f.write('QuickSilver,')
    f.write(str(instance_size) + ',' + str(mean_times[instance_size] + variance_times[instance_size]) + '\n')
f.close()


num_dims = [1, 2, 3, 4, 5]
num_sizes = [5, 10, 15, 20, 25]

jl_100k_num_dim_labels = ["bench_jl varying 1 10 200 100000", "bench_jl varying 2 10 200 100000", "bench_jl varying 3 10 200 100000", "bench_jl varying 4 10 200 100000", "bench_jl varying 5 10 200 100000"]
jl_200k_num_dim_labels = ["bench_jl varying 1 10 200 200000", "bench_jl varying 2 10 200 200000", "bench_jl varying 3 10 200 200000", "bench_jl varying 4 10 200 200000", "bench_jl varying 5 10 200 200000"]
jl_500k_num_dim_labels = ["bench_jl varying 1 10 200 500000", "bench_jl varying 2 10 200 500000", "bench_jl varying 3 10 200 500000", "bench_jl varying 4 10 200 500000", "bench_jl varying 5 10 200 500000"]
jl_100k_size_dim_labels = ["bench_jl 4 varying 5 200 100000", "bench_jl 4 varying 10 200 100000", "bench_jl 4 varying 15 200 100000", "bench_jl 4 varying 20 200 100000", "bench_jl 4 varying 25 200 100000"]
jl_200k_size_dim_labels = ["bench_jl 4 varying 5 200 200000", "bench_jl 4 varying 10 200 200000", "bench_jl 4 varying 15 200 200000", "bench_jl 4 varying 20 200 200000", "bench_jl 4 varying 25 200 200000"]
jl_500k_size_dim_labels = ["bench_jl 4 varying 5 200 500000", "bench_jl 4 varying 10 200 500000", "bench_jl 4 varying 15 200 500000", "bench_jl 4 varying 20 200 500000", "bench_jl 4 varying 25 200 500000"]

jl_100k_dim_times = {}
jl_200k_dim_times = {}
jl_500k_dim_times = {}

jl_100k_size_times = {}
jl_200k_size_times = {}
jl_500k_size_times = {}

f_config = open('all_results.txt', 'r')
f_config_lines = f_config.readlines()
for i in range(len(f_config_lines)):
    line = f_config_lines[i].rstrip()
    if line in jl_100k_num_dim_labels:
        num_dim = int(line.split(' ')[2])
        jl_100k_dim_times[num_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in jl_200k_num_dim_labels:
        num_dim = int(line.split(' ')[2])
        jl_200k_dim_times[num_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in jl_500k_num_dim_labels:
        num_dim = int(line.split(' ')[2])
        jl_500k_dim_times[num_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in jl_100k_size_dim_labels:
        size_dim = int(line.split(' ')[3])
        jl_100k_size_times[size_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in jl_200k_size_dim_labels:
        size_dim = int(line.split(' ')[3])
        jl_200k_size_times[size_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in jl_500k_size_dim_labels:
        size_dim = int(line.split(' ')[3])
        jl_500k_size_times[size_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2

f_config.close()

if not (checkBenchComplete(jl_100k_num_dim_labels, jl_100k_dim_times) and checkBenchComplete(jl_200k_num_dim_labels, jl_200k_dim_times) and checkBenchComplete(jl_500k_num_dim_labels, jl_500k_dim_times)):
    print("QuickSilver benchmarks didn't finish! Please re-run start_zk_bench.py")
    exit

if not (checkBenchComplete(jl_100k_size_dim_labels, jl_100k_size_times) and checkBenchComplete(jl_200k_size_dim_labels, jl_200k_size_times) and checkBenchComplete(jl_500k_size_dim_labels, jl_500k_size_times)):
    print("QuickSilver benchmarks didn't finish! Please re-run start_zk_bench.py")
    exit

jl_num_dim_header = "protocol,num_dim,100k,200k,500k\n"
f = open('jl_num_dim_quicksilver.csv', 'w')
f.write(jl_num_dim_header)
for num_dim in num_dims:
    f.write('QuickSilver,')
    f.write(str(num_dim) + ',' + str(jl_100k_dim_times[num_dim]) + ',' + str(jl_200k_dim_times[num_dim]) + ',' + str(jl_500k_dim_times[num_dim]) + '\n')
f.close()

jl_size_dim_header = "protocol,size_dim,100k,200k,500k\n"
f = open('jl_size_dim_quicksilver.csv', 'w')
f.write(jl_size_dim_header)
for size in num_sizes:
    f.write('QuickSilver,')
    f.write(str(size) + ',' + str(jl_100k_size_times[size]) + ',' + str(jl_200k_size_times[size]) + ',' + str(jl_500k_size_times[size]) + '\n')
f.close()

strawman_jl_100_num_dim_labels = ["bench_strawman_jl varying 1 10 200 100", "bench_strawman_jl varying 2 10 200 100", "bench_strawman_jl varying 3 10 200 100", "bench_strawman_jl varying 4 10 200 100", "bench_strawman_jl varying 5 10 200 100"]
strawman_jl_200_num_dim_labels = ["bench_strawman_jl varying 1 10 200 200", "bench_strawman_jl varying 2 10 200 200", "bench_strawman_jl varying 3 10 200 200", "bench_strawman_jl varying 4 10 200 200", "bench_strawman_jl varying 5 10 200 200"]
strawman_jl_100_size_dim_labels = ["bench_strawman_jl 4 varying 5 200 100", "bench_strawman_jl 4 varying 10 200 100", "bench_strawman_jl 4 varying 15 200 100", "bench_strawman_jl 4 varying 20 200 100", "bench_strawman_jl 4 varying 25 200 100"]
strawman_jl_200_size_dim_labels = ["bench_strawman_jl 4 varying 5 200 200", "bench_strawman_jl 4 varying 10 200 200", "bench_strawman_jl 4 varying 15 200 200", "bench_strawman_jl 4 varying 20 200 200", "bench_strawman_jl 4 varying 25 200 200"]

strawman_jl_100_num_dim_times = {}
strawman_jl_200_num_dim_times = {}
strawman_jl_100_size_dim_times = {}
strawman_jl_200_size_dim_times = {}

strawman_jl_100k_num_dim_times = {}
strawman_jl_200k_num_dim_times = {}
strawman_jl_500k_num_dim_times = {}

strawman_jl_100k_size_dim_times = {}
strawman_jl_200k_size_dim_times = {}
strawman_jl_500k_size_dim_times = {}

f_config = open('all_results.txt', 'r')
f_config_lines = f_config.readlines()
for i in range(len(f_config_lines)):
    line = f_config_lines[i].rstrip()
    if line in strawman_jl_100_num_dim_labels:
        num_dim = int(line.split(' ')[2])
        strawman_jl_100_num_dim_times[num_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in strawman_jl_200_num_dim_labels:
        num_dim = int(line.split(' ')[2])
        strawman_jl_200_num_dim_times[num_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in strawman_jl_100_size_dim_labels:
        size_dim = int(line.split(' ')[3])
        strawman_jl_100_size_dim_times[size_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in strawman_jl_200_size_dim_labels:
        size_dim = int(line.split(' ')[3])
        strawman_jl_200_size_dim_times[size_dim] = float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
f_config.close()

if not (checkBenchComplete(strawman_jl_100_num_dim_labels, strawman_jl_100_num_dim_times) and checkBenchComplete(strawman_jl_200_num_dim_labels, strawman_jl_200_num_dim_times)):
    print("QuickSilver benchmarks didn't finish! Please re-run start_zk_bench.py")
    exit

if not (checkBenchComplete(strawman_jl_100_size_dim_labels, strawman_jl_100_size_dim_times) and checkBenchComplete(strawman_jl_200_size_dim_labels, strawman_jl_200_size_dim_times)):
    print("QuickSilver benchmarks didn't finish! Please re-run start_zk_bench.py")
    exit

for dim in num_dims:
    # perform extrapolation with euler's method
    start = strawman_jl_100_num_dim_times[dim]
    diff = strawman_jl_200_num_dim_times[dim] - strawman_jl_100_num_dim_times[dim]

    # 100 + 999 * (200 - 100) = 100000
    strawman_jl_100k_num_dim_times[dim] = start + 999 * diff
    
    # 100 + 1999 * (200 - 100) = 200000
    strawman_jl_200k_num_dim_times[dim] = start + 1999 * diff

    # 100 + 4999 * (200 - 100) = 500000
    strawman_jl_500k_num_dim_times[dim] = start + 4999 * diff


for size in num_sizes:
    # perform extrapolation with euler's method
    start = strawman_jl_100_size_dim_times[size]
    diff = strawman_jl_200_size_dim_times[size] - strawman_jl_100_size_dim_times[size]

    # 100 + 999 * (200 - 100) = 100000
    strawman_jl_100k_size_dim_times[size] = start + 999 * diff

    # 100 + 1999 * (200 - 100) = 200000
    strawman_jl_200k_size_dim_times[size] = start + 1999 * diff

    # 100 + 4999 * (200 - 100) = 500000
    strawman_jl_500k_size_dim_times[size] = start + 4999 * diff

strawman_jl_num_dim_header = "protocol,num_dim,100k,200k,500k\n"
f = open('strawman_jl_num_dim_quicksilver.csv', 'w')
f.write(strawman_jl_num_dim_header)
for num_dim in num_dims:
    f.write('QuickSilver,')
    f.write(str(num_dim) + ',' + str(strawman_jl_100k_num_dim_times[num_dim]) + ',' + str(strawman_jl_200k_num_dim_times[num_dim]) + ',' + str(strawman_jl_500k_num_dim_times[num_dim]) + '\n')
f.close()

jl_size_dim_header = "protocol,size_dim,100k,200k,500k\n"
f = open('strawman_jl_size_dim_quicksilver.csv', 'w')
f.write(jl_size_dim_header)
for size in num_sizes:
    f.write('QuickSilver,')
    f.write(str(size) + ',' + str(strawman_jl_100k_size_dim_times[size]) + ',' + str(strawman_jl_200k_size_dim_times[size]) + ',' + str(strawman_jl_500k_size_dim_times[size]) + '\n')
f.close()