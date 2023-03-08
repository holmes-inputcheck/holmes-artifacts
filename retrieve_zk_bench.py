import sys, string, json, os
from benchClient import generateRemoteCmdStr, getThroughput
import subprocess

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

range_100k_labels = ["bench_range_check 100000 256", "bench_range_check 100000 4096", "bench_range_check 100000 65536", "bench_range_check 100000 1048576", "bench_range_check 100000 16777216"]
range_200k_labels = ["bench_range_check 200000 256", "bench_range_check 200000 4096", "bench_range_check 200000 65536", "bench_range_check 200000 1048576", "bench_range_check 200000 16777216"]
range_500k_labels = ["bench_range_check 500000 256", "bench_range_check 500000 4096", "bench_range_check 500000 65536", "bench_range_check 500000 1048576", "bench_range_check 500000 16777216"]

jl_100k_labels = ["bench_jl varying 1 10 200 100000", "bench_jl varying 4 10 200 100000", "bench_jl varying 4 50 200 100000"]
jl_200k_labels = ["bench_jl varying 1 10 200 200000", "bench_jl varying 4 10 200 200000", "bench_jl varying 4 50 200 200000"]
jl_500k_labels = ["bench_jl varying 1 10 200 500000", "bench_jl varying 4 10 200 500000", "bench_jl varying 4 50 200 500000"]

range_times = {"bench_range_check 100000 256": -1, "bench_range_check 100000 4096": -1, "bench_range_check 100000 65536": -1, "bench_range_check 100000 1048576": -1, "bench_range_check 100000 16777216": -1,
               "bench_range_check 200000 256": -1, "bench_range_check 200000 4096": -1, "bench_range_check 200000 65536": -1, "bench_range_check 200000 1048576": -1, "bench_range_check 200000 16777216": -1,
               "bench_range_check 500000 256": -1, "bench_range_check 500000 4096": -1, "bench_range_check 500000 65536": -1, "bench_range_check 500000 1048576": -1, "bench_range_check 500000 16777216": -1}

jl_times = {"bench_jl varying 1 10 200 100000": -1, "bench_jl varying 4 10 200 100000": -1, "bench_jl varying 4 50 200 100000": -1,
            "bench_jl varying 1 10 200 200000": -1, "bench_jl varying 4 10 200 200000": -1, "bench_jl varying 4 50 200 200000": -1,
            "bench_jl varying 1 10 200 500000": -1, "bench_jl varying 4 10 200 500000": -1, "bench_jl varying 4 50 200 500000": -1}

f_config = open('all_results.txt', 'r')
f_config_lines = f_config.readlines()
for i in range(len(f_config_lines)):
    line = f_config_lines[i].rstrip()
    if line in range_times.keys():
        # offline input cost for consistency check (SPDZ)
        range_times[line] = float(line.split()[1]) / 2 / throughput
        # online time (QuickSilver)
        range_times[line] += float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
    elif line in jl_times.keys():
        # offline input cost for consistency check (SPDZ)
        jl_times[line] = float(line.split()[5]) * float(line.split()[2]) / 2 / throughput
        # online time (QuickSilver)
        jl_times[line] += float(f_config_lines[i + 1].rstrip()) / 1000 / 1000 * 2
f_config.close()

for time in range_times.values():
    if time == -1:
        print("QuickSilver benchmarks didn't finish! Please re-run `python3 start_coordinator_zk_bench.py` or `python3 start_zk_bench.py`")
        exit

for time in jl_times.values():
    if time == -1:
        print("QuickSilver benchmarks didn't finish! Please re-run `python3 start_coordinator_zk_bench.py` or `python3 start_zk_bench.py`")
        exit

range_header = "protocol,2p_8,2p_12,2p_16,2p_20,2p_24,"
range_header += "6p_8,6p_12,6p_16,6p_20,6p_24,"
range_header += "10p_8,10p_12,10p_16,10p_20,10p_24\n"

f = open('range_100000_quicksilver.csv', 'w')
f.write(range_header)
# 2-party: 1, 6-party: 5, 10-party: 9
f.write('QuickSilver,')
w = []
for mult in (1, 5, 9):
    w.extend(["%.1f" % (range_times[label] * mult) for label in range_100k_labels])
f.write(','.join(w))
f.close()

f = open('range_200000_quicksilver.csv', 'w')
f.write(range_header)
# 2-party: 2, 6-party: 5, 10-party: 9
f.write('QuickSilver,')
w = []
for mult in (1, 5, 9):
    w.extend(["%.1f" % (range_times[label] * mult) for label in range_200k_labels])
f.write(','.join(w))
f.close()

f = open('range_500000_quicksilver.csv', 'w')
f.write(range_header)
# 2-party: 2, 6-party: 5, 10-party: 9
f.write('QuickSilver,')
w = []
for mult in (1, 5, 9):
    w.extend(["%.1f" % (range_times[label] * mult) for label in range_500k_labels])
f.write(','.join(w))
f.close()

jl_header = "protocol,2p_1s10s,2p_4d10s,2p_4d50s,"
jl_header += "6p_1s10s,6p_4d10s,6p_4d50s,"
jl_header += "10p_1s10s,10p_4d10s,10p_4d50s\n"

f = open('jl_100000_quicksilver.csv', 'w')
f.write(jl_header)
# 2-party: 1, 6-party: 5, 10-party: 9
f.write('QuickSilver,')
w = []
for mult in (1, 5, 9):
    w.extend(["%.1f" % (jl_times[label] * mult) for label in jl_100k_labels])
f.write(','.join(w))
f.close()

f = open('jl_200000_quicksilver.csv', 'w')
f.write(jl_header)
# 2-party: 2, 6-party: 5, 10-party: 9
f.write('QuickSilver,')
w = []
for mult in (1, 5, 9):
    w.extend(["%.1f" % (jl_times[label] * mult) for label in jl_200k_labels])
f.write(','.join(w))
f.close()

f = open('jl_500000_quicksilver.csv', 'w')
f.write(jl_header)
# 2-party: 2, 6-party: 5, 10-party: 9
f.write('QuickSilver,')
w = []
for mult in (1, 5, 9):
    w.extend(["%.1f" % (jl_times[label] * mult) for label in jl_500k_labels])
f.write(','.join(w))
f.close()