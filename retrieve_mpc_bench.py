import sys, string, json, os
from benchClient import *
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

num_parties = [2, 6, 10]
range_files = ["range_100000_mpc.txt", "range_200000_mpc.txt", "range_500000_mpc.txt"]

range_offline_triples = {100000: [2450000, 3650000, 4850000, 6050000, 7250000], 
                         200000: [4900000, 7300000, 9700000, 12100000, 14500000],
                         500000: [12250000, 18250000, 24250000, 30250000, 36250000]}

throughputs = {2: getThroughput(), 6: getMPC6Throughput(), 10: getMPC10Throughput()}
range_header = "protocol,2p_8,2p_12,2p_16,2p_20,2p_24,"
range_header += "6p_8,6p_12,6p_16,6p_20,6p_24,"
range_header += "10p_8,10p_12,10p_16,10p_20,10p_24\n"

for file in range_files:
    num_records = int(file.split('_')[1])
    fp = open("range_%d_mpc.csv" % (num_records), 'w')
    fp.write(range_header)
    fp.write("mpc,")
    times = []
    for parties in num_parties:
        cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/SCALE-MAMBA-%d/%s .") % (keyPath, followerPublicAddrs[0], parties, file)
        process = subprocess.Popen(cmd, shell=True)
        process.wait()

        f = open(file, 'r')
        pl = f.readlines()[1].rstrip().split(',')
        f.close()
        for i in range(len(pl)):
            online_time = parties * float(pl[i])
            offline_time = range_offline_triples[num_records][i] * parties / throughputs[parties]
            #print("Parties: %d, Offline: %0.2f, Online: %0.2f" % (parties, offline_time, online_time))
            times.append("%0.1f" % (online_time + offline_time))
    fp.write(','.join(times) + "\n")
    fp.close()

jl_files = ["jl_10000_mpc.txt", "jl_20000_mpc.txt"]

jl_header = "protocol,2p_1s10s,2p_4d10s,2p_4d50s,"
jl_header += "6p_1s10s,6p_4d10s,6p_4d50s,"
jl_header += "10p_1s10s,10p_4d10s,10p_4d50s\n"

jl_offline_triples = {100000: [110100000, 110400000, 110400000], 
                         200000: [220200000, 220800000, 220800000],
                         500000: [550500000, 552000000, 552000000]}

jl_start_time = {2: [], 6: [], 10: []}
jl_diff_time = {2: [], 6: [], 10: []}
for it in [0, 1]:
    file = jl_files[it]

    track = 0
    for parties in num_parties:
        cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/SCALE-MAMBA-%d/%s .") % (keyPath, followerPublicAddrs[0], parties, file)
        process = subprocess.Popen(cmd, shell=True)
        process.wait()

        f = open(file, 'r')
        pl = f.readlines()[1].rstrip().split(',')
        f.close()
        for i in range(len(pl)):
            online_time = float(pl[i])
            if it == 0:
                jl_start_time[parties].append(online_time)
            elif it == 1:
                jl_diff_time[parties].append(online_time - jl_start_time[parties][i])

# perform extrapolation with euler's method to estimate online time
assert(len(jl_start_time) == len(jl_diff_time))
assert(len(jl_start_time) == len(jl_offline_triples[100000]))
for num_records in [100000, 200000, 500000]:
    fp = open("jl_%d_mpc.csv" % (num_records), 'w')
    fp.write(jl_header)
    fp.write("mpc,")
    times = []
    for parties in num_parties:
        for i in range(len(jl_start_time[parties])):
            mult = (num_records - 10000) / (20000 - 10000)
            online_time = parties * (jl_start_time[parties][i] + mult * jl_diff_time[parties][i])
            offline_time = jl_offline_triples[num_records][i] * parties / throughputs[parties]
            #print("Parties: %d, Offline: %0.2f, Online: %0.2f" % (parties, offline_time, online_time))
            times.append("%0.1f" % (online_time + offline_time))
    fp.write(','.join(times) + "\n")
    fp.close()