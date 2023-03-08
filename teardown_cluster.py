import sys, string, json
import subprocess

filename = "system.config"

f_config = open(filename)
sysConfig = json.load(f_config)

# teardown aux server
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 terminate-instances --instance-ids "%s"') % (sysConfig["AuxID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()

# teardown leader server
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 terminate-instances --instance-ids "%s"') % (sysConfig["LeaderID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()

# teardown follower servers
for i in range(len(sysConfig["Followers"])):
    cmd = ('aws ec2 terminate-instances --instance-ids "%s"') % (sysConfig["Followers"][i]["ID"])
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

# teardown coordinator server
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 terminate-instances --instance-ids "%s"') % (sysConfig["CoordinatorID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()


f_config.close()

print("Finished cluster teardown")