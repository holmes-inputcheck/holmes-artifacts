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
        print("SPDZ MPC offline throughput file not found!")
        print("You either haven't completed the SPDZ benchmarks yet (run `python3 start_spdz_bench.py`)")
        print("Or you haven't retrieved the SPDZ benchmarks yet (run `python3 retrieve_spdz.py`)")
        print("Try the latter command first.")
        exit

    f = open('./spdz-mpc-p2-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput

def getMPC6Throughput():
    if not os.path.exists("./spdz-mpc-p6-throughput.out"):
        print("SPDZ MPC offline throughput file not found!")
        print("You either haven't completed the SPDZ benchmarks yet (run `python3 start_spdz_bench.py`)")
        print("Or you haven't retrieved the SPDZ benchmarks yet (run `python3 retrieve_spdz.py`)")
        print("Try the latter command first.")
        exit

    f = open('./spdz-mpc-p6-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput

def getMPC10Throughput():
    if not os.path.exists("./spdz-mpc-p10-throughput.out"):
        print("SPDZ MPC offline throughput file not found!")
        print("You either haven't completed the SPDZ benchmarks yet (run `python3 start_spdz_bench.py`)")
        print("Or you haven't retrieved the SPDZ benchmarks yet (run `python3 retrieve_spdz.py`)")
        print("Try the latter command first.")
        exit

    f = open('./spdz-mpc-p10-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput


def get2PC6Throughput():
    if not os.path.exists("./spdz-2pc-p6-throughput.out"):
        print("SPDZ 2PC offline throughput file not found!")
        print("You either haven't completed the 2PC SPDZ benchmarks yet (run `python3 start_spdz_2pc_bench.py`)")
        print("Or you haven't retrieved the SPDZ benchmarks yet (run `python3 retrieve_spdz.py`)")
        print("Try the latter command first.")
        exit

    f = open('./spdz-2pc-p6-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput

def get2PC10Throughput():
    if not os.path.exists("./spdz-2pc-p10-throughput.out"):
        print("SPDZ 2PC offline throughput file not found!")
        print("You either haven't completed the 2PC SPDZ benchmarks yet (run `python3 start_spdz_2pc_bench.py`)")
        print("Or you haven't retrieved the SPDZ benchmarks yet (run `python3 retrieve_spdz.py`)")
        print("Try the latter command first.")
        exit

    f = open('./spdz-2pc-p10-throughput.out', 'r')
    throughput = float(f.readline().rsplit()[0])
    f.close()

    return throughput
