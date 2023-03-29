import sys, string, json
import subprocess
import os
import threading
import time
import tempfile

username = "ubuntu"

f_config = open('system.config')
config = json.load(f_config)
f_config.close()
keyPath = config["SSHKeyPath"]

def generateRemoteCmdStr(machine, remoteCmd):
    return ("ssh -i %s -o StrictHostKeyChecking=no %s@%s \"%s\"") % (keyPath, username, machine, remoteCmd) 

def generateRemoteCmdStrScreen(machine, remoteCmd):
    return ("ssh -i %s -o StrictHostKeyChecking=no %s@%s screen -d -m \"%s\"") % (keyPath, username, machine, remoteCmd) 

def getThroughput():
    if not os.path.exists("./spdz-mpc-p2-throughput.out"):
        print("You must run the SPDZ benchmarking script first with `python3 start_spdz_bench.py`")
        exit

    f = open('./spdz-mpc-p2-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput

def getMPC6Throughput():
    if not os.path.exists("./spdz-mpc-p6-throughput.out"):
        print("You must run the SPDZ benchmarking script first with `python3 start_spdz_bench.py`")
        exit

    f = open('./spdz-mpc-p6-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput

def getMPC10Throughput():
    if not os.path.exists("./spdz-mpc-p10-throughput.out"):
        print("You must run the SPDZ benchmarking script first with `python3 start_spdz_bench.py`")
        exit

    f = open('./spdz-mpc-p10-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput


def get2PC6Throughput():
    if not os.path.exists("./spdz-2pc-p6-throughput.out"):
        print("You must run the SPDZ benchmarking script first with `python3 start_spdz_2pc_bench.py`")
        exit

    f = open('./spdz-2pc-p6-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput

def get2PC10Throughput():
    if not os.path.exists("./spdz-2pc-p10-throughput.out"):
        print("You must run the SPDZ benchmarking script first with `python3 start_spdz_2pc_bench.py`")
        exit

    f = open('./spdz-2pc-p10-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput
