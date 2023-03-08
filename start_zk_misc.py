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

print("Note: this script is synchronous")
print("This script will take approximately 45 minutes long")
print("You will need your computer to be continuously connected to the AMI.")

print("Starting ZK bench misc (group, trimmed mean, mean + variance, JL vs. Strawman JL) tests.")

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
    cmd = ("scp -i %s -o StrictHostKeyChecking=no zk-misc-checks.sh ubuntu@%s:~/HOLMES/holmes-library/") % (keyPath, followerPublicAddrs[i])
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    # kill all zk scripts
    cmd = ("pkill -f zk-misc-checks -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

    # kill all current bench checks
    cmd = ("pkill -f bench -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

    # kill all current histogram checks
    cmd = ("pkill -f histogram -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

    # kill all current trimmed mean checks
    cmd = ("pkill -f trimmed -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

    # kill all current mean checks
    cmd = ("pkill -f mean -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

    # kill all current variance checks
    cmd = ("pkill -f variance -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

    # kill all current jl checks
    cmd = ("pkill -f jl -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

party_processes = []
for i in range(2):
    cmd = ("cd ~/HOLMES/holmes-library; chmod 755 zk-misc-checks.sh; ./zk-misc-checks.sh %d") % (i + 1)
    #cmd = ("cd ~/HOLMES/holmes-library; chmod 755 zk-misc-checks.sh; nohup ./zk-misc-checks.sh %d &> /dev/null &") % (i + 1)
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True)
    party_processes.append(process)

for process in party_processes:    
    process.wait()