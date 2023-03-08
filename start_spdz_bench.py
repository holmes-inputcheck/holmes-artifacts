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
print("Please continue to run this script for approximately 25 minutes.")
print("You will need your computer to be continuously connected to the AMI.")

num_parties = [2, 6, 10]

for i in range(max(num_parties)):
    cmd = ("scp -i %s -o StrictHostKeyChecking=no spdz-script-mpc.sh ubuntu@%s:~/MP-SPDZ") % (keyPath, followerPublicAddrs[i])
    process = subprocess.Popen(cmd, shell=True, stdout=devNull)
    process.wait()

leaderPublicAddr = followerPublicAddrs[0]
for parties in num_parties:
    party_processes = []
    for i in range(parties):
        # kill all running scripts
        cmd = ("pkill -f spdz-script-mpc -9")
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
        process.wait()

        # kill all current SPDZ processes
        cmd = ("pkill -f pairwise-offline -9")
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
        process.wait()
    
    # run all the scripts on all of the parties
    print("Started SPDZ MPC benchmarking for %d parties." % (parties)) 
    for i in range(parties):
        cmd = "cd ~/MP-SPDZ; chmod 755 spdz-script-mpc.sh;"
        if i == 0:
            # cmd += ("nohup ./spdz-script-mpc.sh %d %d %s &> /dev/null &") % (parties, i, "localhost")
            cmd += ("./spdz-script-mpc.sh %d %d %s &> /dev/null") % (parties, 0, "localhost")
        else:
            # cmd += ("nohup ./spdz-script-mpc.sh %d %d %s &> /dev/null &") % (parties, i, leaderPublicAddr)
            cmd += ("./spdz-script-mpc.sh %d %d %s &> /dev/null") % (parties, i, leaderPublicAddr)
            
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
        party_processes.append(process)
    
    # halt until all the scripts finish for the current amount of parties
    for process in party_processes:
        process.wait()

    cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/MP-SPDZ/spdz-mpc-p%d-throughput.out .") % (keyPath, leaderPublicAddr, parties)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

    print("Finished SPDZ MPC benchmarking for %d parties." % (parties))