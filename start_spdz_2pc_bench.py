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

num_parties = [2, 6, 10]
num_threads = 32

print("Note: this script is synchronous")
print("Please continue to run this script for approximately 15 minutes.")
print("You will need your computer to be continuously connected to the AMI.")

for i in range(2):
    cmd = ("scp -i %s -o StrictHostKeyChecking=no spdz-script-2pc.sh ubuntu@%s:~/MP-SPDZ") % (keyPath, followerPublicAddrs[i])
    process = subprocess.Popen(cmd, shell=True, stdout=devNull)
    process.wait()

# first, find throughput of 2 party, 6 party, 10 party
#num_parties = [2, 6, 10]

leaderPublicAddr = followerPublicAddrs[0]
for parties in num_parties:
    party_processes = []
    for i in range(2):
        # kill all running scripts
        cmd = ("pkill -f spdz-script-2pc -9")
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
        process.wait()

        # kill all current SPDZ processes
        cmd = ("pkill -f pairwise-offline -9")
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
        process.wait()
    
    # run all the scripts on two parties with limited cores to estimate 2PC
    print("Started SPDZ 2PC benchmarking for %d parties." % (parties)) 
    for i in range(2):
        cmd = "cd ~/MP-SPDZ; chmod 755 spdz-script-2pc.sh;"
        if i == 0:
            cmd += ("./spdz-script-2pc.sh %d %d %d %s &> /dev/null") % (parties, 0, num_threads // (parties - 1), "localhost")
        else:
            cmd += ("./spdz-script-2pc.sh %d %d %d %s &> /dev/null") % (parties, i, num_threads // (parties - 1), leaderPublicAddr)
            
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
        party_processes.append(process)
    
    # halt until all the scripts finish for the current amount of parties
    for process in party_processes:
        process.wait()

    cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/MP-SPDZ/spdz-2pc-p%d-throughput.out .") % (keyPath, leaderPublicAddr, parties)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    print("Finished SPDZ 2PC benchmarking for %d parties." % (parties)) 