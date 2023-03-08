import sys, string, json, os
from benchClient import generateRemoteCmdStr, getThroughput
import subprocess

username = "ubuntu"

f_config = open('system.config')
config = json.load(f_config)
f_config.close()

followerIDs = [config["Followers"][i]["ID"] for i in range(len(config["Followers"]))]
followerPublicAddrs = [config["Followers"][i]["PublicAddr"] for i in range(len(config["Followers"]))]
followerPrivateAddrs = [config["Followers"][i]["PrivateAddr"] for i in range(len(config["Followers"]))]

keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')

cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/SCALE-MAMBA/hist_mpc.csv .") % (keyPath, followerPublicAddrs[0])
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/SCALE-MAMBA/trimmed_mpc.csv .") % (keyPath, followerPublicAddrs[0])
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/SCALE-MAMBA/mv_mpc.csv .") % (keyPath, followerPublicAddrs[0])
process = subprocess.Popen(cmd, shell=True)
process.wait()

parties = 2

# if you want to select certain scripts, you can break it up by commenting out scripts
throughput = getThroughput()

# histogram / group check
hist_offline_triples = {4: [2750000, 5500000, 8500000], 
                        6: [3350000, 6700000, 9700000], 
                        8: [3950000, 7900000, 10900000],
                        10: [4550000, 9100000, 12100000],
                        12: [5150000, 10300000, 13300000]}

f = open('hist_mpc.csv', 'r')
wb = []
h = True
for line in f.readlines():
    if h:
        h = False
        wb.append(line)
    else:
        wb_tmp = []
        vals = line.rstrip().split(',')
        wb_tmp.append(vals[0])
        groupsize = int(vals[1])
        wb_tmp.append(vals[1])
        for i in range(3):
            online_time = float(vals[i + 2])
            offline_time = float(hist_offline_triples[groupsize][i] / throughput)
            wb_tmp.append(str(online_time + offline_time))
        wb.append(','.join(wb_tmp) + "\n")
f.close()

f = open('hist_mpc.csv', 'w')
for line in wb:
    f.write(line)
f.close()

trimmed_offline_triples = {8: [1610350, 3210950], 
                        12: [2210350, 4410950], 
                        16: [2810350, 5610950],
                        20: [3410350, 6810950],
                        24: [4010350, 8010950]}

f = open('trimmed_mpc.csv', 'r')
wb = []
h = True
for line in f.readlines():
    if h:
        h = False
        wb.append(line)
    else:
        wb_tmp = []
        vals = line.rstrip().split(',')
        wb_tmp.append(vals[0])
        threshold = int(vals[1])
        wb_tmp.append(vals[1])
        for i in range(2):
            online_time = float(vals[i + 2])
            offline_time = float(trimmed_offline_triples[groupsize][i] / throughput)
            wb_tmp.append(str(online_time + offline_time))
        wb.append(','.join(wb_tmp) + "\n")
f.close()

f = open('trimmed_mpc.csv', 'w')
for line in wb:
    f.write(line)
f.close()

# mean + variance

# first summand is mean offline triples
# second summand is variance offline triples
mv_offline_triples = {1000000: 530500 + 1592000, 
                      2000000: 1033500 + 3101000, 
                      3000000: 1536500 + 4610000, 
                      4000000: 2036500 + 6110000, 
                      5000000: 2539500 + 7616000}

f = open('mv_mpc.csv', 'r')
wb = []
h = True
for line in f.readlines():
    if h:
        h = False
        wb.append(line)
    else:
        wb_tmp = []
        vals = line.rstrip().split(',')
        wb_tmp.append(vals[0])
        num_records = int(vals[1])
        wb_tmp.append(vals[1])

        online_time = float(vals[2])
        offline_time = float(mv_offline_triples[num_records] / throughput)
        wb_tmp.append(str(online_time + offline_time))
        wb.append(','.join(wb_tmp) + "\n")
f.close()

f = open('mv_mpc.csv', 'w')
for line in wb:
    f.write(line)
f.close()