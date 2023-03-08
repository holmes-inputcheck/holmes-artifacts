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
print("You will need your computer to be continuously connected to the AMI.")
print("This script will take approximately 3 hours long")

print("Started producing Spartan bench (Range+JL) tests")
cmd = ("cd ~/HOLMES/holmes-spartan; ./run-tests.sh")
#cmd = ("cd ~/HOLMES/holmes-spartan; nohup ./run-tests.sh &")
process = subprocess.Popen(generateRemoteCmdStr(serverAddr, cmd), shell=True)
process.wait()
print("Finished Spartan benchmarking tests.")
