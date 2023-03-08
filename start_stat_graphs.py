import sys, string, json, os
from benchClient import generateRemoteCmdStr
import subprocess

username = "ubuntu"

f_config = open('system.config')
config = json.load(f_config)
f_config.close()
keyPath = config["SSHKeyPath"]
serverAddr = config["AuxPublicAddr"]
devNull = open(os.devnull, 'w')

print("Note: this script is synchronous")
print("This script will take approximately 40 minutes long")
print("You will need your computer to be continuously connected to the AMI.")

print("Starting statistical graph tests.")

cmd = ("cd ~/HOLMES/holmes-stat; python3 graph-scripts/run_all_simulated.py &> /dev/null; python3 graph-scripts/run_all_dataset.py &> /dev/null")
process = subprocess.Popen(generateRemoteCmdStr(serverAddr, cmd), shell=True)
process.wait()

print("Finished up statistical graph tests.")