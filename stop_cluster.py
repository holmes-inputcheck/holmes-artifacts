import sys, string, json, time
import subprocess

filename = "system.config"

f_config = open(filename)
sysConfig = json.load(f_config)

cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 stop-instances --instance-ids "%s"') % (sysConfig["AuxID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()

cmd = ('aws ec2 stop-instances --instance-ids "%s"') % (sysConfig["LeaderID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()

for i in range(len(sysConfig["Followers"])):
    cmd = ('aws ec2 stop-instances --instance-ids "%s"') % (sysConfig["Followers"][i]["ID"])
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

cmd = ('aws ec2 stop-instances --instance-ids "%s"') % (sysConfig["CoordinatorID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()

print("Finished cluster stop. Wait around 60 seconds before resuming.")