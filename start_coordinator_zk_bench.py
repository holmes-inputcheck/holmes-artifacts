import sys, string, json, time, os
import subprocess
from benchClient import generateRemoteCmdStr

username = "ubuntu"

f_config = open('system.config')
config = json.load(f_config)
f_config.close()
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
coordinatorPublicAddr = config["CoordinatorPublicAddr"]

print("Starting asynchronous ZK bench (Range+JL) test.")
print("Retrieve results after 15 minutes with `python3 retrieve_zk_bench.py`.")

# kill all zk scripts
cmd = ("pkill -f zk -9")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()

cmd = ("pkill -f bench -9")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "zk-bench.sh", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "start_zk_bench.py", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("cd ~/holmes-artifacts; screen -dmS zk_bench python3 start_zk_bench.py")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True)
process.wait()