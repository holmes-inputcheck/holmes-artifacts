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
print("This script will take approximately 1 hour long")
print("You will need your computer to be continuously connected to the AMI.")

for i in range(2):
    cmd = ("scp -i %s -o StrictHostKeyChecking=no mpc-misc-hist.sh ubuntu@%s:~/SCALE-MAMBA") % (keyPath, followerPublicAddrs[i])
    print(cmd)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    cmd = ("scp -i %s -o StrictHostKeyChecking=no mpc-misc-trimmed.sh ubuntu@%s:~/SCALE-MAMBA") % (keyPath, followerPublicAddrs[i])
    print(cmd)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    cmd = ("scp -i %s -o StrictHostKeyChecking=no mpc-misc-mv.sh ubuntu@%s:~/SCALE-MAMBA") % (keyPath, followerPublicAddrs[i])
    print(cmd)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    # kill all mpc scripts
    cmd = ("pkill -f mpc-misc-checks -9")
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

parties = 2

# if you want to select certain scripts, you can break it up by commenting out scripts

# histogram / group check
print("Starting MPC group check [~30 minutes]")
party_processes = []
for i in range(parties):
    cmd = ("cd ~/SCALE-MAMBA; chmod 755 mpc-misc-hist.sh; ./mpc-misc-hist.sh %d &> /dev/null") % (i)
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    party_processes.append(process)

for process in party_processes:
    process.wait()

print("Finished MPC group check")

# trimmed means
print("Starting MPC trimmed mean check [~10 minutes]")
party_processes = []
for i in range(parties):
    cmd = ("cd ~/SCALE-MAMBA; chmod 755 mpc-misc-trimmed.sh; ./mpc-misc-trimmed.sh %d") % (i)
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True)
    party_processes.append(process)

for process in party_processes:
    process.wait()
print("Finished MPC trimmed mean check")

# mean + variance
print("Starting MPC mean+variance check [~15 minutes]")
party_processes = []
for i in range(parties):
    cmd = ("cd ~/SCALE-MAMBA; chmod 755 mpc-misc-mv.sh; ./mpc-misc-mv.sh %d &> /dev/null") % (i)
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    party_processes.append(process)

for process in party_processes:
    process.wait()
print("Finished MPC mean+variance check")