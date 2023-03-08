import sys, string, json, time, os
import subprocess
from benchClient import generateRemoteCmdStr

username = "ubuntu"

print("Starting asynchronous Pairwise 2PC bench (range+JL) tests.")
print("Retrieve results after 2 hours with `python3 retrieve_2pc_bench.py`.")

f_config = open('system.config')
config = json.load(f_config)
f_config.close()
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
coordinatorPublicAddr = config["CoordinatorPublicAddr"]

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "start_all.sh", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("cd ~/holmes-artifact/scripts; screen -dmS all_tests ./start_all.sh")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True)
process.wait()