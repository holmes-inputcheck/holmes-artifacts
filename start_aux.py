import sys, string, json, time
import subprocess
# import benchClient

regionAMIs = { 
        "aux": "ami-02c4a21a55dd8a242"
        }  


filename = "system.config"

print("Starting cluster...")

f_config = open(filename, "r")
sysConfig = json.load(f_config)
f_config.close()


# Create Aux Server (Spartan + Graphs)
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 run-instances --image-id %s --count 1 --instance-type c5.9xlarge --key-name HOLMES --placement "{\\\"AvailabilityZone\\\": \\\"us-west-2a\\\"}" --security-groups HOLMES --tag-specifications \"ResourceType=instance,Tags=[{Key=Name,Value=%s}]\"') % (regionAMIs["aux"], "aux")
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
auxConfig = json.loads(out)
auxID = auxConfig["Instances"][0]["InstanceId"]

time.sleep(30)

cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 describe-instances --instance-ids "%s"') % (auxID)
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
c = json.loads(out)
auxPublicAddr = (c["Reservations"][0]["Instances"][0]["PublicIpAddress"])
auxPrivateAddr = (c["Reservations"][0]["Instances"][0]["PrivateIpAddress"])
print("launched aux server")

time.sleep(30)

# Create configurations

sysConfig["AuxPublicAddr"] = auxPublicAddr
sysConfig["AuxPrivateAddr"] = auxPrivateAddr
sysConfig["AuxID"] = auxID
sysConfig["SSHKeyPath"] = "~/.ssh/HOLMES.pem"
sysConfigBlob = json.dumps(sysConfig)

f_config = open(filename, "w")
f_config.write(sysConfigBlob)
f_config.close()

sshKeyPath = sysConfig["SSHKeyPath"]

print("Copying config files to instances")

# Wait for all instances to be fully started
time.sleep(60)

if sysConfig["AuxPublicAddr"] != "127.0.0.1":
    cmd = ("scp -i %s -o StrictHostKeyChecking=no system.config ubuntu@%s:~/HOLMES/system.config") % (sshKeyPath, sysConfig["AuxPublicAddr"])
    process = subprocess.Popen(cmd, shell=True)
    process.wait()


print("Cluster setup done.")
print("--- Check that none of the scp commands above failed (SSH connection on port 22 was refused) ---")
print("--- If one or more scp commands failed, teardown the cluster and start a new one ---")
