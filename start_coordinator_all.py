import sys, string, json, time, os
import subprocess
from benchClient import generateRemoteCmdStr

username = "ubuntu"

print("Starting ALL benchmarks asynchronously!")
print("Retrieve results after AT LEAST 24 hours with `./retrieve_all.sh`.")

f_config = open('system.config')
config = json.load(f_config)
f_config.close()
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
coordinatorPublicAddr = config["CoordinatorPublicAddr"]

cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % (keyPath, "start_all.sh", coordinatorPublicAddr)
process = subprocess.Popen(cmd, shell=True)
process.wait()

cmd = ("cd ~/holmes-artifacts; screen -dmS all_tests ./start_all.sh")
process = subprocess.Popen(generateRemoteCmdStr(coordinatorPublicAddr, cmd), shell=True)
process.wait()