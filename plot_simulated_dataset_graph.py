import json, subprocess
import pandas as pd
import matplotlib as mpl
from matplotlib import pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

username = "ubuntu"

f_config = open('system.config')
config = json.load(f_config)
f_config.close()

auxID = config["AuxID"]
auxPublicAddr = config["AuxPublicAddr"]
keyPath = config["SSHKeyPath"]

files = ["t_test_p_graph.csv", "z_test_p_graph.csv", "f_test_p_graph.csv", "chi_test_p_graph.csv"]
for file in files:
    cmd = ("scp -i %s -o StrictHostKeyChecking=no ubuntu@%s:~/HOLMES/holmes-stat/%s .") % (keyPath, auxPublicAddr, file)
    process = subprocess.Popen(cmd, shell=True)
    process.wait()

mpl.rcParams['text.usetex'] = True
plt.rcParams.update( { "text.latex.preamble": r"\usepackage{amsmath,mathptmx}", } )

mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
#mpl.rcParams['xtick.labelsize'] = 20
#mpl.rcParams.update({'figure.max_open_warning': 0})
#mpl.rcParams.update({"font.size": 34,"figure.autolayout": True})
plt.rcParams["font.family"] = "Helvetica Neue"
plt.rc('font', weight='bold')

columns = ["EntriesChanged", "Pvalue"]
jl_columns = ["EntriesChanged", "NormalPvalue", "UnnormalPvalue", "JLPvalue"]
dt = pd.read_csv("t_test_p_graph.csv", usecols=columns)
dz = pd.read_csv("z_test_p_graph.csv", usecols=columns)
df = pd.read_csv("f_test_p_graph.csv", usecols=columns)
dc = pd.read_csv("chi_test_p_graph.csv", usecols=jl_columns)

num_entries = 40000
threshold = 12000
x = np.arange(0, threshold, 0.1)
y5 = [0.05 for y in x]

half_linspace = [i for i in range(0, threshold)]
for i in range(threshold, num_entries):
    half_linspace.append(None)
half_linspace = np.array(half_linspace)

ax = plt.axes()
ztest = ax.plot(dz.EntriesChanged, dz.Pvalue, color='blue', linewidth=6, label=r"$z$-test")
ttest = ax.plot(dt.EntriesChanged, dt.Pvalue, color='orange', linestyle='--', dashes=(3, 3), linewidth=6, label=r"$t$-test")
ftest = ax.plot(df.EntriesChanged, df.Pvalue, color='c', linewidth=6, label=r"$F$-test")
normaltest = ax.plot(dc.EntriesChanged, dc.NormalPvalue, color='pink', linewidth=6, label=r"Normalized $\mathbf{\chi^2}$")

unnormaltest = ax.plot(dc.EntriesChanged, dc.UnnormalPvalue, color='lime', linewidth=6, label=r"Unnormalized $\mathbf{\chi^2}$")
jltest = ax.plot(dc.EntriesChanged, dc.JLPvalue, color='firebrick', linestyle='--', dashes=(3, 3), linewidth=6, label=r"HOLMES $\mathbf{\chi^2}$")
statvalue = ax.plot(x, y5, color='black', linestyle='--', label=r"$p$-value $=0.05$")

plt.ylabel(r"$\mathbf{p}$\textbf{-value}",fontsize=25)
plt.yticks(np.array([0.05, 0.2, 0.4, 0.6, 0.8, 1.0]), fontsize=33)
plt.xlabel(r"\textbf{\% of data inputs corrupted", fontsize=25)

plt.legend(ncol=1, labelspacing=0.2, columnspacing=0.1, fontsize=24, loc = [0.24, 0.37])

plt.xticks(np.arange(0, threshold + 1, 2000), fontsize=33)
ax.xaxis.set_major_formatter(mtick.PercentFormatter(num_entries, symbol=None, decimals=0))

fig = plt.gcf()
fig.set_size_inches(6,6, forward=True)

pp = PdfPages('simulated_dataset_stat_graph.pdf')
plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
pp.close()

#plt.show()
