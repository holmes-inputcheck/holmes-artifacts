import sys, string, json, time, os
import subprocess
from benchClient import generateRemoteCmdStr

username = "ubuntu"

print("Starting asynchronous MPC bench (range+JL) tests.")
print("Retrieve results after 7 hours with `python3 retrieve_mpc_bench.py`.")

f_config = open('system.config')
config = json.load(f_config)
f_config.close()
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
coordinatorPublicAddr = config["CoordinatorPublicAddr"]

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "start_mpc_bench.py", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "mpc-range.sh", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "mpc-jl.sh", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

# kill all existing MPC scripts
cmd = ("pkill -f mpc -9")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()

cmd = ("pkill -f Player -9")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()

cmd = ("cd ~/holmes-artifacts; screen -dmS mpc_bench python3 start_mpc_bench.py")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True)
process.wait()