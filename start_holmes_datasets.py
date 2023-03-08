import sys, string, json, os
from benchClient import generateRemoteCmdStr
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

print("Note: this script is (intended to be) synchronous")
print("This script will take approximately 15 minutes long")
print("You will need your computer to be continuously connected to the AMI.")

print("Starting HOLMES dataset integration tests.")

zk_config = open("host_ip.hpp", "w")
zk_config.write('#ifndef EMP_ZK_HOST_IP_H\n')
zk_config.write('#define EMP_ZK_HOST_IP_H\n')
zk_config.write(('\n#define BENCH_HOST_IP "%s"\n') % followerPublicAddrs[0])
zk_config.write('\n#endif //EMP_ZK_HOST_IP_H')
zk_config.close()

cmd = ("scp -i %s -o StrictHostKeyChecking=no host_ip.hpp ubuntu@%s:~/HOLMES/holmes-library/bench/") % (keyPath, followerPublicAddrs[1])
process = subprocess.Popen(cmd, shell=True)
process.wait()

for i in range(2):
    # kill all zk scripts
    cmd = ("pkill -f test_check -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

print("Running dataset 1")
party_processes = []
for i in range(2):
    cmd = ("cd ~/HOLMES/holmes-library; EMP_MY_PARTY_ID=%d python3 bench-scripts/bench_dataset1.py") % (i + 1)
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True)
    party_processes.append(process)

for process in party_processes:
    process.wait()

print("Running dataset 2")
party_processes = []
for i in range(2):
    cmd = ("cd ~/HOLMES/holmes-library; EMP_MY_PARTY_ID=%d python3 bench-scripts/bench_dataset2.py") % (i + 1)
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True)
    party_processes.append(process)

for process in party_processes:    
    process.wait()

print("Running dataset 3")
party_processes = []
for i in range(2):
    cmd = ("cd ~/HOLMES/holmes-library; EMP_MY_PARTY_ID=%d python3 bench-scripts/bench_dataset2.py") % (i + 1)
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True)
    party_processes.append(process)

for process in party_processes:    
    process.wait()

print("Finished HOLMES integration tests.")