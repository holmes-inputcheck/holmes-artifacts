import sys, string, json, os
from benchClient import generateRemoteCmdStr
import subprocess

print("Starting asynchronous SPDZ Pairwise 2PC Offline throughput bench.")
print("Benchmarking will be finished after around 15 minutes.")

f_config = open('system.config')
config = json.load(f_config)
f_config.close()
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
coordinatorPublicAddr = config["CoordinatorPublicAddr"]

# kill all existing SPDZ scripts to prevent duplicates
cmd = ("pkill -f pairwise-offline -9")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()

cmd = ("pkill -f spdz -9")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "start_spdz_2pc_bench.py", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "spdz-script-2pc.sh", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("cd ~/holmes-artifacts; screen -dmS spdz_bench python3 start_spdz_2pc_bench.py")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True)
process.wait()


