
protocols_100 = ["quicksilver", "2pc", "mpc", "spartan_nizk", "spartan_snark"]
protocols_rest = ["quicksilver", "2pc", "mpc", "spartan_nizk"]

# range case
num_records = "100k"
header = "num_entries,protocol,2p_8,2p_12,2p_16,2p_20,2p_24,6p_8,6p_12,6p_16,6p_20,6p_24,10p_8,10p_12,10p_16,10p_20,10p_24\n"
fp = open("range_all.csv", 'w')
fp.write(header)
for protocol in protocols_100:
    filename = "range_100000_%s.csv" % (protocol)
    f = open(filename, 'r')
    fp.write(num_records + "," + f.readlines()[1].rstrip() + "\n")
    f.close()

num_records = "200k"
for protocol in protocols_rest:
    filename = "range_200000_%s.csv" % (protocol)
    f = open(filename, 'r')
    fp.write(num_records + "," + f.readlines()[1].rstrip() + "\n")
    f.close()

num_records = "500k"
for protocol in protocols_rest:
    filename = "range_500000_%s.csv" % (protocol)
    f = open(filename, 'r')
    fp.write(num_records + "," + f.readlines()[1].rstrip() + "\n")
    f.close()

fp.close()

# jl case
num_records = "100k"
header = "num_entries,protocol,2p_1s10s,2p_4d10s,2p_4d50s,6p_1s10s,6p_4d10s,6p_4d50s,10p_1s10s,10p_4d10s,10p_4d50s\n"
fp = open("jl_all.csv", 'w')
fp.write(header)
for protocol in protocols_100:
    filename = "jl_100000_%s.csv" % (protocol)
    f = open(filename, 'r')
    fp.write(num_records + "," + f.readlines()[1].rstrip() + "\n")
    f.close()

num_records = "200k"
for protocol in protocols_rest:
    filename = "jl_200000_%s.csv" % (protocol)
    f = open(filename, 'r')
    fp.write(num_records + "," + f.readlines()[1].rstrip() + "\n")
    f.close()

num_records = "500k"
for protocol in protocols_rest:
    filename = "jl_500000_%s.csv" % (protocol)
    f = open(filename, 'r')
    fp.write(num_records + "," + f.readlines()[1].rstrip() + "\n")
    f.close()

fp.close()