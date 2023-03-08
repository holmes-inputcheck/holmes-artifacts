import sys, string, json, os
from benchClient import generateRemoteCmdStr
import subprocess

username = "ubuntu"

f_config = open('system.config')
config = json.load(f_config)
f_config.close()

leaderID = config["LeaderID"]
leaderPublicAddr = config["LeaderPublicAddr"]
leaderPrivateAddr = config["LeaderPrivateAddr"]
followerIDs = [config["Followers"][i]["ID"] for i in range(len(config["Followers"]))]
followerPublicAddrs = [config["Followers"][i]["PublicAddr"] for i in range(len(config["Followers"]))]
followerPrivateAddrs = [config["Followers"][i]["PrivateAddr"] for i in range(len(config["Followers"]))]

keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')

num_parties = [2, 6, 10]

for i in range(max(num_parties) - 1):
    cmd = ("scp -i %s -o StrictHostKeyChecking=no 2pc-range.sh ubuntu@%s:~/SCALE-MAMBA-%d") % (keyPath, leaderPublicAddr, i)
    process = subprocess.Popen(cmd, shell=True, stdout=devNull)
    process.wait()

    cmd = ("scp -i %s -o StrictHostKeyChecking=no 2pc-range.sh ubuntu@%s:~/SCALE-MAMBA-PAIR") % (keyPath, followerPublicAddrs[i])
    process = subprocess.Popen(cmd, shell=True, stdout=devNull)
    process.wait()

    # kill all current range check processes
    cmd = ("pkill -f range -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

# kill all current range check processes
cmd = ("pkill -f range -9")
process = subprocess.Popen(generateRemoteCmdStr(leaderPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()

# 40 minutes
for parties in num_parties:
    print("Producing range check 2PC benchmarks for %d parties. Takes around 40 minutes." % (parties))
    party_processes = []

    # run SCALE-MAMBA on the followers first
    for i in range(parties - 1):
        cmd = ("cd ~/SCALE-MAMBA-PAIR; chmod 755 2pc-range.sh; ./2pc-range.sh %d %d") % (parties, 1)
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)

    # run SCALE-MAMBA on the leader next
    f = open('2pc-parallel-range.txt', 'w')
    for i in range(parties - 1):
        f.write("cd ~/SCALE-MAMBA-%d; chmod 755 2pc-range.sh; ./2pc-range.sh %d %d\n" % (i, parties, 0))
    f.close()

    cmd = ("scp -i %s -o StrictHostKeyChecking=no 2pc-parallel-range.txt ubuntu@%s:~/") % (keyPath, leaderPublicAddr)
    process = subprocess.Popen(cmd, shell=True, stdout=devNull)
    print(cmd)
    process.wait()

    cmd = ("cd ~; parallel --jobs %d < 2pc-parallel-range.txt" % (parties - 1))
    process = subprocess.Popen(generateRemoteCmdStr(leaderPublicAddr, cmd), shell=True, stdout=devNull)
    party_processes.append(process)

    for process in party_processes:
        process.wait()

    print("Finished range check 2PC benchmarks for %d parties." % (parties))

'''
for i in range(max(num_parties) - 1):
    cmd = ("scp -i %s -o StrictHostKeyChecking=no 2pc-jl.sh ubuntu@%s:~/SCALE-MAMBA-%d") % (keyPath, leaderPublicAddr, i)
    process = subprocess.Popen(cmd, shell=True, stdout=devNull)
    process.wait()

    cmd = ("scp -i %s -o StrictHostKeyChecking=no 2pc-jl.sh ubuntu@%s:~/SCALE-MAMBA-PAIR") % (keyPath, followerPublicAddrs[i])
    process = subprocess.Popen(cmd, shell=True, stdout=devNull)
    process.wait()

    # kill all current JL processes
    cmd = ("pkill -f jl -9")
    process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)
    process.wait()

# kill all current JL processes
cmd = ("pkill -f jl -9")
process = subprocess.Popen(generateRemoteCmdStr(leaderPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()

for parties in num_parties:
    print("Producing JL 2PC benchmarks for %d parties." % (parties))
    party_processes = []

    # run SCALE-MAMBA on the followers first
    for i in range(parties - 1):
        cmd = ("cd ~/SCALE-MAMBA-PAIR; chmod 755 2pc-jl.sh; ./2pc-jl.sh %d %d") % (parties, 1)
        process = subprocess.Popen(generateRemoteCmdStr(followerPublicAddrs[i], cmd), shell=True, stdout=devNull)

    # run SCALE-MAMBA on the leader next
    f = open('2pc-parallel-jl.txt', 'w')
    for i in range(parties - 1):
        f.write("cd ~/SCALE-MAMBA-%d; chmod 755 2pc-jl.sh; ./2pc-jl.sh %d %d\n" % (i, parties, 0))
    f.close()

    for i in range(parties - 1):
        cmd = ("scp -i %s -o StrictHostKeyChecking=no 2pc-parallel-jl.txt ubuntu@%s:~/") % (keyPath, leaderPublicAddr)
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()

    cmd = ("cd ~; parallel --jobs %d < 2pc-parallel-jl.txt" % (parties - 1))
    process = subprocess.Popen(generateRemoteCmdStr(leaderPublicAddr, cmd), shell=True, stdout=devNull)
    party_processes.append(process)

    for process in party_processes:
        process.wait()

    print("Finished JL 2PC benchmarks for %d parties." % (parties))
'''