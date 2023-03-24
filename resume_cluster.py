import sys, string, json, time
import subprocess

filename = "system.config"

f_config = open(filename)
sysConfig = json.load(f_config)
f_config.close()

# start instances

# start aux server
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 start-instances --instance-ids "%s"') % (sysConfig["AuxID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()

# start leader server
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 start-instances --instance-ids "%s"') % (sysConfig["LeaderID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()

# start follower servers
for i in range(len(sysConfig["Followers"])):
    cmd = ('aws ec2 start-instances --instance-ids "%s"') % (sysConfig["Followers"][i]["ID"])
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()

# start coordinator server
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 start-instances --instance-ids "%s"') % (sysConfig["CoordinatorID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()

# Wait for all instances to be fully started
print("Waiting for cluster to resume before updating public ip")
time.sleep(60)

# update the public ip addresses

# update aux server
cmd = ('aws ec2 describe-instances --instance-ids "%s"') % (sysConfig["AuxID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
c = json.loads(out)
newAuxPublicAddr = (c["Reservations"][0]["Instances"][0]["PublicIpAddress"])

# update follower servers
newFollowerPublicAddrs = []
for i in range(len(sysConfig["Followers"])):
    cmd = ('aws ec2 describe-instances --instance-ids "%s"') % (sysConfig["Followers"][i]["ID"])
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = process.stdout.read()
    c = json.loads(out)
    newFollowerPublicAddrs.append(c["Reservations"][0]["Instances"][0]["PublicIpAddress"])

# update leader server
cmd = ('aws ec2 describe-instances --instance-ids "%s"') % (sysConfig["LeaderID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
c = json.loads(out)
newLeaderPublicAddr = (c["Reservations"][0]["Instances"][0]["PublicIpAddress"])


# update coordinator server
cmd = ('aws ec2 describe-instances --instance-ids "%s"') % (sysConfig["CoordinatorID"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
c = json.loads(out)
newCoordinatorPublicAddr = (c["Reservations"][0]["Instances"][0]["PublicIpAddress"])

f_config = open(filename, "w")

sysConfig["AuxPublicAddr"] = newAuxPublicAddr
for i in range(len(sysConfig["Followers"])):
    sysConfig["Followers"][i]["PublicAddr"] = newFollowerPublicAddrs[i]
sysConfig["LeaderPublicAddr"] = newLeaderPublicAddr
sysConfig["CoordinatorPublicAddr"] = newCoordinatorPublicAddr

sysConfigBlob = json.dumps(sysConfig)
f_config.write(sysConfigBlob)
f_config.close()

# send the updated config to coordinator
cmd = ("scp -i ~/.ssh/HOLMES.pem -o StrictHostKeyChecking=no %s ubuntu@%s:~/holmes-artifacts/") % ("system.config", sysConfig["CoordinatorPublicAddr"])
process = subprocess.Popen(cmd, shell=True)
process.wait()

print("Finished cluster resume")