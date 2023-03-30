#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib
# import seaborn as sns
import sys
import datetime
import glob
from itertools import cycle
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FixedLocator
from matplotlib.ticker import FixedFormatter
# %matplotlib inline

import warnings
import matplotlib.cbook
import matplotlib as mpl

mpl.rcParams['text.usetex'] = True
plt.rcParams.update( { "text.latex.preamble": r"\usepackage{amsmath,mathptmx}", } )

warnings.filterwarnings('ignore')
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams.update({'figure.max_open_warning': 0})
mpl.rcParams.update({"font.size": 34,"figure.autolayout": True})
mpl.rc("axes", edgecolor="0.8")
plt.rcParams["font.family"] = "Helvetica Neue"

legendsize = 40

red = "#a93226"
blue = "#2874a6"
green = "#1e8449"

# fix number of dimensions 4
#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib
# import seaborn as sns
import sys
import datetime
import glob
from itertools import cycle
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import FixedLocator
from matplotlib.ticker import FixedFormatter
# %matplotlib inline

import warnings
import matplotlib.cbook
import matplotlib as mpl

mpl.rcParams['text.usetex'] = True
plt.rcParams.update( { "text.latex.preamble": r"\usepackage{amsmath,mathptmx}", } )

warnings.filterwarnings('ignore')
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['ytick.labelsize'] = 10
mpl.rcParams.update({'figure.max_open_warning': 0})
mpl.rcParams.update({"font.size": 34,"figure.autolayout": True})
mpl.rc("axes", edgecolor="0.8")
plt.rcParams["font.family"] = "Helvetica Neue"

legendsize = 40

red = "#a93226"
blue = "#2874a6"
green = "#1e8449"

# fix num of dimensions 4

def plot_fig():
    columns = ["size_dim","100k", "200k","500k"]
    jl_qs = pd.read_csv("jl_size_dim_quicksilver.csv", usecols=columns)
    jl_straw = pd.read_csv("strawman_jl_size_dim_quicksilver.csv", usecols=columns)

    combined_labels =  ["N = 100k (HOLMES)", "N = 100k (Baseline)", "N = 200k (HOLMES)","N = 200k (Baseline)",  "N = 500k (HOLMES)", "N = 500k (Baseline)"]

    y1plot, = plt.plot(jl_qs.size_dim, jl_qs.iloc[:,1], linestyle='-', marker='o', markersize=6, color=red)
    y2plot, = plt.plot(jl_qs.size_dim, jl_qs.iloc[:,2], linestyle='-', marker='o', markersize=6, color=blue)
    y3plot, = plt.plot(jl_qs.size_dim, jl_qs.iloc[:,3], linestyle='-', marker='o', markersize=6, color=green)

    z1plot, = plt.plot(jl_straw.size_dim, jl_straw.iloc[:,1], linestyle=':', marker='o', markersize=6, color=red)
    z2plot, = plt.plot(jl_straw.size_dim, jl_straw.iloc[:,2], linestyle=':', marker='o', markersize=6, color=blue)
    z3plot, = plt.plot(jl_straw.size_dim, jl_straw.iloc[:,3], linestyle=':', marker='o', markersize=6, color=green)

    axes = plt.gca()    

    combinedlegend = ylegend = plt.legend([y1plot, z1plot, y2plot, z2plot, y3plot, z3plot], combined_labels, ncol=3, columnspacing=0.2, fontsize=8, loc = [0.002, 0.85])

    axes.add_artist(combinedlegend)

    plt.ylabel("Time (s)",fontsize=10)
    plt.xlabel("Number of individual labels in each dimension", fontsize=15)
    xts = [5, 10, 15, 20, 25]
    plt.xticks(xts, ["5", "10", "15", "20", "25"], fontsize=15)

    # print log scale on the y-axis
    plt.semilogy()

    #start at 1 to start it at 10^0
    #start at 10 to start at 10^1
    axes.set_ylim([10, 100000001])

    fig = plt.gcf()
    fig.set_size_inches(6,4, forward=True)

    pp = PdfPages('plot_jl_varying_size_dim.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()

if __name__ == "__main__":
    if True:
        plot_fig()

