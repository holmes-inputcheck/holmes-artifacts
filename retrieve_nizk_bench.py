import sys, string, json, os
from benchClient import generateRemoteCmdStr, getThroughput
import subprocess

def parse_range_file(version, num_records, lines):
    words_arr = []
    for i in range(1, len(lines)):
        line = lines[i].rstrip()
        words_arr.append(line.split(','))
    
    words_to_write = ["spartan_" + version]
    for i in range(1, len(words_arr[0])):
        for j in range(len(words_arr)):
            #print("Range: " + str(num_records / 2 / throughput))
            words_to_write.append(str("%.1f" % (float(words_arr[j][i]) + num_records / throughput / 2)))
    
    return ','.join(words_to_write)

def parse_jl_file(version, num_records, lines):
    words_arr = []
    for i in range(1, len(lines)):
        line = lines[i].rstrip()
        words_arr.append(line.split(','))
    
    words_to_write = ["spartan_" + version]
    for i in range(2, len(words_arr[0])):
        for j in range(len(words_arr)):
            #print("JL: " + str(int(words_arr[j][0]) * num_records / 2 / throughput))
            words_to_write.append(str("%.1f" % (float(words_arr[j][i]) + int(words_arr[j][0]) * num_records / throughput / 2)))
    
    return ','.join(words_to_write)
    
username = "ubuntu"

f_config = open('system.config')
config = json.load(f_config)
f_config.close()

auxID = config["AuxID"]
auxPublicAddr = config["AuxPublicAddr"]
keyPath = config["SSHKeyPath"]
devNull = open(os.devnull, 'w')
throughput = getThroughput()

range_raw_filenames = ["range_check_100000_nizk.txt", "range_check_200000_nizk.txt", "range_check_500000_nizk.txt"]
range_csv_filenames = ["range_100000_spartan_nizk.csv", "range_200000_spartan_nizk.csv", "range_500000_spartan_nizk.csv"]
jl_raw_filenames = ["jl_100000_nizk.txt", "jl_200000_nizk.txt", "jl_500000_nizk.txt"]
jl_csv_filenames = ["jl_100000_spartan_nizk.csv", "jl_200000_spartan_nizk.csv", "jl_500000_spartan_nizk.csv"]

for file in range_raw_filenames:
    cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/HOLMES/holmes-spartan/%s .") % (keyPath, auxPublicAddr, file)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

for file in jl_raw_filenames:
    cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/HOLMES/holmes-spartan/%s .") % (keyPath, auxPublicAddr, file)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()


#print("retrieved all files")

range_header = "protocol,2p_8,2p_12,2p_16,2p_20,2p_24,"
range_header += "6p_8,6p_12,6p_16,6p_20,6p_24,"
range_header += "10p_8,10p_12,10p_16,10p_20,10p_24\n"

for i in range(len(range_raw_filenames)):
    if not os.path.isfile(range_raw_filenames[i]):
        print("Spartan benchmarks not complete! Please re-run `python3 start_spartan_bench.py`")
        exit
    f_config = open(range_raw_filenames[i], 'r')
    f_config_lines = f_config.readlines()
    w = parse_range_file("nizk", int(range_raw_filenames[i].split('_')[2]), f_config_lines)
    f_config.close()

    f = open(range_csv_filenames[i], 'w')
    f.write(range_header)
    f.write(w)
    f.close()

jl_header = "protocol,2p_1s10s,2p_4d10s,2p_4d50s,"
jl_header += "6p_1s10s,6p_4d10s,6p_4d50s,"
jl_header += "10p_1s10s,10p_4d10s,10p_4d50s\n"

for i in range(len(jl_raw_filenames)):
    if not os.path.isfile(jl_raw_filenames[i]):
        print("Spartan benchmarks not complete! Please re-run `python3 start_spartan_bench.py`")
        exit
    f_config = open(jl_raw_filenames[i], 'r')
    f_config_lines = f_config.readlines()
    w = parse_jl_file("nizk", int(jl_raw_filenames[i].split('_')[1]), f_config_lines)
    f_config.close()

    f = open(jl_csv_filenames[i], 'w')
    f.write(jl_header)
    f.write(w)
    f.close()