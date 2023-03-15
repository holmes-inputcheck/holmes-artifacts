import sys, string, json, time, os
import subprocess
from benchClient import generateRemoteCmdStr

regionAMIs = { 
        "aux": "ami-01e1a4855d549761f",
        "follower": "ami-0489da360b66825e8",
        "leader": "ami-09e833043aecffd75",
        "coordinator": "ami-0fbf6e826da84365a"
        }  

filename = "system.config"
devNull = open(os.devnull, 'w')

print("Starting cluster...")

f_config = open(filename, "r")
sysConfig = json.load(f_config)
f_config.close()

# Create 10 Follower Servers (MPC + 2PC + QuickSilver)
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 run-instances --image-id %s --count 10 --instance-type c5.9xlarge --key-name HOLMES --placement "{\\\"AvailabilityZone\\\": \\\"us-west-2a\\\"}" --security-groups HOLMES') % (regionAMIs["follower"])
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
followerConfig = json.loads(out)
followerIDs = [instance["InstanceId"] for instance in followerConfig["Instances"]]
sysConfig["Followers"] = [{} for sub in range(len(followerIDs))]
for i in range(len(followerIDs)):
    sysConfig["Followers"][i]["ID"] = followerIDs[i]
sysConfigBlob = json.dumps(sysConfig)
f_config = open(filename, "w")
f_config.write(sysConfigBlob)
f_config.close()
print("Finished starting follower servers")
time.sleep(10)

# Create Aux Server (Spartan + Graphs)
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 run-instances --image-id %s --count 1 --instance-type c5.9xlarge --key-name HOLMES --placement "{\\\"AvailabilityZone\\\": \\\"us-west-2a\\\"}" --security-groups HOLMES --tag-specifications \"ResourceType=instance,Tags=[{Key=Name,Value=%s}]\"') % (regionAMIs["aux"], "aux")
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
auxConfig = json.loads(out)
auxID = auxConfig["Instances"][0]["InstanceId"]
sysConfig["AuxID"] = auxID
sysConfigBlob = json.dumps(sysConfig)
f_config = open(filename, "w")
f_config.write(sysConfigBlob)
f_config.close()
print("Finished starting aux server")
time.sleep(10)

# Create Leader Server (MPC + 2PC + QuickSilver)
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 run-instances --image-id %s --count 1 --instance-type c5.9xlarge --key-name HOLMES --placement "{\\\"AvailabilityZone\\\": \\\"us-west-2a\\\"}" --security-groups HOLMES --tag-specifications \"ResourceType=instance,Tags=[{Key=Name,Value=%s}]\"') % (regionAMIs["leader"], "leader")
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
leaderConfig = json.loads(out)
leaderID = leaderConfig["Instances"][0]["InstanceId"]
sysConfig["LeaderID"] = leaderID
sysConfigBlob = json.dumps(sysConfig)
f_config = open(filename, "w")
f_config.write(sysConfigBlob)
f_config.close()
print("Finished starting leader server")
time.sleep(10)

# Create Coordinator Server
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 run-instances --image-id %s --count 1 --instance-type c5.2xlarge --key-name HOLMES --placement "{\\\"AvailabilityZone\\\": \\\"us-west-2a\\\"}" --security-groups HOLMES --tag-specifications \"ResourceType=instance,Tags=[{Key=Name,Value=%s}]\"') % (regionAMIs["coordinator"], "coordinator")
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
coordinatorConfig = json.loads(out)
coordinatorID = coordinatorConfig["Instances"][0]["InstanceId"]
sysConfig["CoordinatorID"] = coordinatorID
sysConfigBlob = json.dumps(sysConfig)
f_config = open(filename, "w")
f_config.write(sysConfigBlob)
f_config.close()
print("Finished starting coordinator server")
#print(followerIDs, followerConfig)

# Wait for all instances to be fully started
time.sleep(60)
'''
# COMMENT THIS WHEN WE UNCOMMENT THE ABOVE
auxID = sysConfig["AuxID"]
auxPublicAddr = sysConfig["AuxPublicAddr"]
leaderID = sysConfig["LeaderID"]
leaderPublicAddr = sysConfig["LeaderPublicAddr"]
followerIDs = [sysConfig["Followers"][i]["ID"] for i in range(len(sysConfig["Followers"]))]
followerPublicAddrs = [sysConfig["Followers"][i]["PublicAddr"] for i in range(len(sysConfig["Followers"]))]
coordinatorID = sysConfig["CoordinatorID"]
coordinatorPublicAddr = sysConfig["CoordinatorPublicAddr"]
'''
# Retrieve Aux Server metadata
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 describe-instances --instance-ids "%s"') % (auxID)
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
c = json.loads(out)
auxPublicAddr = (c["Reservations"][0]["Instances"][0]["PublicIpAddress"])
auxPrivateAddr = (c["Reservations"][0]["Instances"][0]["PrivateIpAddress"])
print("launched aux server")

# Retrieve Leader Server metadata
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 describe-instances --instance-ids "%s"') % (leaderID)
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
c = json.loads(out)
leaderPublicAddr = (c["Reservations"][0]["Instances"][0]["PublicIpAddress"])
leaderPrivateAddr = (c["Reservations"][0]["Instances"][0]["PrivateIpAddress"])
print("launched leader server")

# Retrieve Follower Server metadata
followerPublicAddrs = []
followerPrivateAddrs = []
for i in range(len(followerIDs)):
    cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 describe-instances --instance-ids "%s"; aws ec2 create-tags --resources %s --tags Key=Name,Value=%s') % (followerIDs[i], followerIDs[i], "follower" + str(i))
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out = process.stdout.read()
    c = json.loads(out)
    followerPublicAddrs.append(c["Reservations"][0]["Instances"][0]["PublicIpAddress"])
    followerPrivateAddrs.append(c["Reservations"][0]["Instances"][0]["PrivateIpAddress"])
print("launched follower servers")

# Retrieve Coordinator Server metadata
cmd = ('export AWS_DEFAULT_REGION=us-west-2; aws ec2 describe-instances --instance-ids "%s"') % (coordinatorID)
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
out = process.stdout.read()
c = json.loads(out)
coordinatorPublicAddr = (c["Reservations"][0]["Instances"][0]["PublicIpAddress"])
coordinatorPrivateAddr = (c["Reservations"][0]["Instances"][0]["PrivateIpAddress"])
print("launched coordinator server")

# Create SysConfig JSON
sysConfig["AuxPublicAddr"] = auxPublicAddr
sysConfig["AuxPrivateAddr"] = auxPrivateAddr
sysConfig["LeaderPublicAddr"] = leaderPublicAddr
sysConfig["LeaderPrivateAddr"] = leaderPrivateAddr
sysConfig["CoordinatorPublicAddr"] = coordinatorPublicAddr
sysConfig["CoordinatorPrivateAddr"] = coordinatorPrivateAddr
for i in range(len(followerIDs)):
    sysConfig["Followers"][i]["PublicAddr"] = followerPublicAddrs[i]
    sysConfig["Followers"][i]["PrivateAddr"] = followerPrivateAddrs[i]
sysConfig["SSHKeyPath"] = "~/.ssh/HOLMES.pem"
sysConfigBlob = json.dumps(sysConfig)
f_config = open(filename, "w")
f_config.write(sysConfigBlob)
f_config.close()
sshKeyPath = sysConfig["SSHKeyPath"]
print("Copying config files to instances")

# Create Pairwise 2PC config
pair_names = []
for i in range(9):
    pair_name = "NetworkData_pair_%d.txt" % (i)
    pair_names.append(pair_name)

    pair_config = open(pair_name, "w")
    pair_config.write("RootCA.crt\n")
    pair_config.write("2\n")
    pair_config.write("0 %s Player1.crt P1\n" % (leaderPrivateAddr))
    pair_config.write("1 %s Player2.crt P2\n" % (followerPrivateAddrs[i]))
    pair_config.write("0\n")
    pair_config.write("0")
    pair_config.close()

# Create 2, 6, and 10 party Configs for MPC

# 2 party
p2_name = "NetworkData_p2.txt"
p2_config = open(p2_name, "w")
p2_config.write("RootCA.crt\n")
p2_config.write("2\n")
p2_config.write("0 %s Player1.crt P1\n" % (followerPrivateAddrs[0]))
p2_config.write("1 %s Player2.crt P2\n" % (followerPrivateAddrs[1]))
p2_config.write("0\n")
p2_config.write("0")
p2_config.close()

# 6 party
p6_name = "NetworkData_p6.txt"
p6_config = open(p6_name, "w")
p6_config.write("RootCA.crt\n")
p6_config.write("6\n")
for i in range(6):
    p6_config.write("%d %s Player%d.crt P%d\n" % (i, followerPrivateAddrs[i], i + 1, i + 1))
p6_config.write("0\n")
p6_config.write("0")
p6_config.close()

# 10 party
p10_name = "NetworkData_p10.txt"
p10_config = open(p10_name, "w")
p10_config.write("RootCA.crt\n")
p10_config.write("10\n")
for i in range(10):
    p10_config.write("%d %s Player%d.crt P%d\n" % (i, followerPrivateAddrs[i], i + 1, i + 1))
p10_config.write("9\n")
p10_config.write("0\n")
p10_config.write("0")
p10_config.close()

# Create host_ip.hpp for QuickSilver tests
zk_config = open("host_ip.hpp", "w")
zk_config.write('#ifndef EMP_ZK_HOST_IP_H\n')
zk_config.write('#define EMP_ZK_HOST_IP_H\n')
zk_config.write(('\n#define BENCH_HOST_IP "%s"\n') % followerPublicAddrs[0])
zk_config.write('\n#endif //EMP_ZK_HOST_IP_H')
zk_config.close()

# Copy Config Files and Setup to Servers

# Aux Server
if sysConfig["AuxPublicAddr"] != "127.0.0.1":
    cmd = ("scp -i %s -o StrictHostKeyChecking=no system.config ubuntu@%s:~/HOLMES/system.config") % (sshKeyPath, sysConfig["AuxPublicAddr"])
    process = subprocess.Popen(cmd, shell=True)
    process.wait()
print("copied config to aux server")

# Leader Server
if sysConfig["LeaderPublicAddr"] != "127.0.0.1":
    for i in range(len(followerIDs) - 1):
        cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/SCALE-MAMBA-%d/Data") % (sshKeyPath, pair_names[i], sysConfig["LeaderPublicAddr"], i)
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()
        cmd = generateRemoteCmdStr(sysConfig["LeaderPublicAddr"], "cd ~/SCALE-MAMBA-%d/Data/; mv %s NetworkData.txt" % (i, pair_names[i]))
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()
print("copied config to leader server")

if sysConfig["CoordinatorPublicAddr"] != "127.0.0.1":
    #cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/.ssh/") % (sshKeyPath, sshKeyPath, sysConfig["CoordinatorPublicAddr"])
    #process = subprocess.Popen(cmd, shell=True, stdout=devNull)
    #process.wait()

    cmd = ("chmod 400 %s") % (sshKeyPath)
    process = subprocess.Popen(generateRemoteCmdStr(sysConfig["CoordinatorPublicAddr"], cmd), shell=True)
    process.wait()

    # TO-DO: coordinator server should git clone from the holmes-artifact repo or at least cp from here
    #cmd = ("cd ~; git clone https://github.com/holmes-inputcheck/holmes-artifacts.git")
    #process = subprocess.Popen(generateRemoteCmdStr(sysConfig["CoordinatorPublicAddr"], cmd), shell=True)
    #process.wait()
print("copied config to coordinator server")

# Follower Servers
for i in range(len(followerIDs)):
    follower_pubaddr = sysConfig["Followers"][i]["PublicAddr"]
    if follower_pubaddr != "127.0.0.1":
        # update bashrc file with party id
        cmd = ("echo 'export MY_PARTY_ID=%d' >> ~/.bashrc && source ~/.bashrc") % (i)
        process = subprocess.Popen(generateRemoteCmdStr(follower_pubaddr, cmd), shell = True)
        process.wait()

        # copy host_ip to QuickSilver
        if i == 1:
            cmd = ("scp -i %s -o StrictHostKeyChecking=no host_ip.hpp ubuntu@%s:~/HOLMES/holmes-library/bench/") % (sshKeyPath, follower_pubaddr)
            process = subprocess.Popen(cmd, shell=True, stdout=devNull)
            process.wait()

        # copy network configs to SCALE-MAMBA
        cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/SCALE-MAMBA/Data/") % (sshKeyPath, p2_name, follower_pubaddr)
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()
        cmd = generateRemoteCmdStr(follower_pubaddr, "cd ~/SCALE-MAMBA/Data/; mv %s NetworkData.txt" % (p2_name))
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()

        cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/SCALE-MAMBA-2/Data/") % (sshKeyPath, p2_name, follower_pubaddr)
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()
        cmd = generateRemoteCmdStr(follower_pubaddr, "cd ~/SCALE-MAMBA-2/Data/; mv %s NetworkData.txt" % (p2_name))
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()

        cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/SCALE-MAMBA-6/Data/") % (sshKeyPath, p6_name, follower_pubaddr)
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()
        cmd = generateRemoteCmdStr(follower_pubaddr, "cd ~/SCALE-MAMBA-6/Data/; mv %s NetworkData.txt" % (p6_name))
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()

        cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/SCALE-MAMBA-10/Data/") % (sshKeyPath, p10_name, follower_pubaddr)
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()
        cmd = generateRemoteCmdStr(follower_pubaddr, "cd ~/SCALE-MAMBA-10/Data/; mv %s NetworkData.txt" % (p10_name))
        process = subprocess.Popen(cmd, shell=True, stdout=devNull)
        process.wait()

        if i < len(followerIDs) - 1:
            cmd = ("scp -i %s -o StrictHostKeyChecking=no %s ubuntu@%s:~/SCALE-MAMBA-PAIR/Data/") % (sshKeyPath, pair_names[i], follower_pubaddr)
            process = subprocess.Popen(cmd, shell=True, stdout=devNull)
            process.wait()
            cmd = generateRemoteCmdStr(follower_pubaddr, "cd ~/SCALE-MAMBA-PAIR/Data/; mv %s NetworkData.txt" % (pair_names[i]))
            process = subprocess.Popen(cmd, shell=True, stdout=devNull)
            process.wait()

print("copied to follower servers")

print("Cluster setup done.")
print("--- Check that none of the scp commands above failed (SSH connection on port 22 was refused) ---")
print("--- If one or more scp commands failed, teardown the cluster and start a new one ---")
