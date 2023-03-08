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
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath,mathptmx}']

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

# fix dimension size 10

def plot_fig():
    columns = ["num_dim","100k", "200k","500k"]
    jl_qs = pd.read_csv("jl_num_dim_quicksilver.csv", usecols=columns)
    jl_straw = pd.read_csv("strawman_jl_num_dim_quicksilver.csv", usecols=columns)

    x = [2, 3, 4, 5]

    #ylabels = ["N = 100k (HOLMES)", "N = 200k (HOLMES)", "N = 500k (HOLMES)"]
    #zlabels = ["N = 100k (Baseline)", "N = 200k (Baseline)", "N = 500k (Baseline)"]
    combined_labels =  ["N = 100k (HOLMES)", "N = 100k (Baseline)", "N = 200k (HOLMES)","N = 200k (Baseline)",  "N = 500k (HOLMES)", "N = 500k (Baseline)"]

    y1plot, = plt.plot(x, jl_qs.iloc[1:,1], linestyle='-', marker='o', markersize=6, color=red)
    y2plot, = plt.plot(x, jl_qs.iloc[1:,2], linestyle='-', marker='o', markersize=6, color=blue)
    y3plot, = plt.plot(x, jl_qs.iloc[1:,3], linestyle='-', marker='o', markersize=6, color=green)

    z1plot, = plt.plot(x, jl_straw.iloc[1:,1], linestyle=':', marker='o', markersize=6, color=red)
    z2plot, = plt.plot(x, jl_straw.iloc[1:,2], linestyle=':', marker='o', markersize=6, color=blue)
    z3plot, = plt.plot(x, jl_straw.iloc[1:,3], linestyle=':', marker='o', markersize=6, color=green)

    axes = plt.gca()    

    combinedlegend = ylegend = plt.legend([y1plot, z1plot, y2plot, z2plot, y3plot, z3plot], combined_labels, ncol=3, columnspacing=0.2, fontsize=8, loc = [0.002, 0.85])

    #ylegend = plt.legend([y1plot, y2plot, y3plot], ylabels, ncol=1, columnspacing=0.2, fontsize=8, loc = [0.05, 0.75])
    #zlegend = plt.legend([z1plot, z2plot, z3plot], zlabels, ncol=1, columnspacing=0.2, fontsize=8, loc = [0.6, 0.04])

    #axes.add_artist(ylegend)
    #axes.add_artist(zlegend)
    axes.add_artist(combinedlegend)

    plt.ylabel("Time (s)",fontsize=10)
    #plt.yticks(np.arange(0,1001,10), fontsize=10)
    plt.xlabel("Number of dimensions", fontsize=15)
    xts = [2, 3, 4, 5]
    plt.xticks(xts, ["2", "3", "4", "5"], fontsize=15)

    # print log scale on the y-axis
    plt.semilogy()

    #start at 1 to start it at 10^0
    #start at 10 to start at 10^1
    axes.set_ylim([10, 100000001])

    fig = plt.gcf()
    
    fig.set_size_inches(6,4, forward=True)

    pp = PdfPages('plot_jl_varying_num_dim.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()

if __name__ == "__main__":
    if True:
        plot_fig()