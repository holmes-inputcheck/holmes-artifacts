import sys, string, json, os, math
from benchClient import generateRemoteCmdStr
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

followerIDs = [config["Followers"][i]["ID"] for i in range(len(config["Followers"]))]
followerPublicAddrs = [config["Followers"][i]["PublicAddr"] for i in range(len(config["Followers"]))]
followerPrivateAddrs = [config["Followers"][i]["PrivateAddr"] for i in range(len(config["Followers"]))]
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')


spdz_files = ["spdz-2pc-p2-throughput.out", "spdz-2pc-p6-throughput.out", "spdz-2pc-p10-throughput.out",
              "spdz-mpc-p2-throughput.out", "spdz-mpc-p6-throughput.out", "spdz-mpc-p10-throughput.out"]

for file in spdz_files:
    cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/MP-SPDZ/%s .") % (keyPath, followerPublicAddrs[0], file)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()