import sys, string, json, time, os
import subprocess
from benchClient import generateRemoteCmdStr

username = "ubuntu"

print("Starting asynchronous Spartan bench (Range+JL) test.")
print("Retrieve results after 3 hours with `python3 retrieve_nizk_bench.py` and `python3 retrieve_snark_bench.py`.")

f_config = open('system.config')
config = json.load(f_config)
f_config.close()
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
coordinatorPublicAddr = config["CoordinatorPublicAddr"]

# kill all existing spartan scripts to prevent duplicates
cmd = ("pkill -f bench -9")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "start_spartan_bench.py", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("cd ~/holmes-artifacts; screen -dmS spartan_bench python3 start_spartan_bench.py")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True)
process.wait()


