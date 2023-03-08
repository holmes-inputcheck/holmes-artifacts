import sys, string, json, time, os
import subprocess
from benchClient import generateRemoteCmdStr

username = "ubuntu"

print("Starting asynchronous statistical graph tests.")
print("Retrieve results after 40 minutes with `python3 TO-DO???.py`.")

f_config = open('system.config')
config = json.load(f_config)
f_config.close()
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
coordinatorPublicAddr = config["CoordinatorPublicAddr"]

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "start_stat_graphs.py", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

# kill all existing graph scripts
cmd = ("pkill -f graph -9")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True, stdout=devNull)
process.wait()


cmd = ("cd ~/holmes-artifacts; screen -dmS stat_graphs python3 start_stat_graphs.py")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True)
process.wait()
