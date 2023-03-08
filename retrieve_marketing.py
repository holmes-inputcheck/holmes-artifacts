import sys, string, json, os
from benchClient import *
import subprocess

username = "ubuntu"

f_config = open('system.config')
config = json.load(f_config)
f_config.close()

followerPublicAddrs = [config["Followers"][i]["PublicAddr"] for i in range(len(config["Followers"]))]
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
throughputs = {2: getThroughput(), 6: getMPC6Throughput(), 10: getMPC10Throughput()}

num_entries = 41188

cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/HOLMES/holmes-library/all_results.txt .") % (keyPath, followerPublicAddrs[0])
process = subprocess.Popen(cmd, shell=True)
process.wait()

zk_times = {}
f = open('all_results.txt', 'r')
f_lines = f.readlines()
for i in range(len(f_lines)):
    line = f_lines[i].rstrip()
    if line == "dataset_1":
        input_load_time = num_entries / 2 / throughputs[2]
        online_time = float(f_lines[i + 1].rstrip()) / 1000 / 1000 / 2
        zk_times[2] = online_time
        break
zk_times[6] = 5 * zk_times[2]
zk_times[10] = 9 * zk_times[2]
f_config.close()

dataset1_triples = 28195600
num_parties=[2,6,10]
mpc_times = {}
for parties in num_parties:
    mpc_file = "marketing_mpc.txt"
    cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/SCALE-MAMBA-%d/%s .") % (keyPath, followerPublicAddrs[0], parties, mpc_file)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    f = open(mpc_file, 'r')
    online_time = float(f.readline().rstrip())
    offline_time = dataset1_triples / throughputs[parties]
    mpc_times[parties] = parties * (online_time + offline_time) 
    f.close()

f = open("marketing.csv", 'w')
f.write("num_parties,zk,mpc\n")
for parties in num_parties:
    f.write(str(parties)+","+str(zk_times[parties])+","+str(mpc_times[parties])+"\n")
f.close()