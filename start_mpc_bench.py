import sys, string, json, os
from benchClient import generateRemoteCmdStr
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

print("Note: this script is synchronous")
print("This script will take approximately 7 hours long")
print("You will need your computer to be continuously connected to the AMI.")

num_parties = [2, 6, 10]

for i in range(max(num_parties)):
    for parties in num_parties:
        cmd = ("scp -i %s -o StrictHostKeyChecking=no mpc-range.sh ubuntu@%s:~/SCALE-MAMBA-%d") % (keyPath, followerPublicAddrs[i], parties)
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()

    # kill all current range check processes
    cmd = ("pkill -f range -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

    # kill all current jl processes
    cmd = ("pkill -f jl -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()


for parties in num_parties:
    print("Producing range check MPC benchmarks for %d parties." % (parties))
    party_processes = []
    for i in range(parties):
        cmd = ("cd ~/SCALE-MAMBA-%d; chmod 755 mpc-range.sh; ./mpc-range.sh %d %d") % (parties, parties, i)
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
        party_processes.append(process)

    #cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/SCALE-MAMBA/range-check.out .") % (keyPath, followerPublicAddrs[i])
    #print(cmd)
    for process in party_processes:
        process.wait()

    print("Finished range check MPC benchmarks for %d parties." % (parties))

for i in range(max(num_parties)):
    for parties in num_parties:
        cmd = ("scp -i %s -o StrictHostKeyChecking=no mpc-jl.sh ubuntu@%s:~/SCALE-MAMBA-%d") % (keyPath, followerPublicAddrs[i], parties)
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()

    # kill all current range processes
    cmd = ("pkill -f range -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

    # kill all current jl processes
    cmd = ("pkill -f jl -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()


for parties in num_parties:
    print("Producing JL MPC benchmarks for %d parties." % (parties))
    party_processes = []
    for i in range(parties):
        cmd = ("cd ~/SCALE-MAMBA-%d; chmod 755 mpc-jl.sh; ./mpc-jl.sh %d %d") % (parties, parties, i)
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
        party_processes.append(process)

    for process in party_processes:
        process.wait()

    print("Finished JL MPC benchmarks for %d parties." % (parties))

