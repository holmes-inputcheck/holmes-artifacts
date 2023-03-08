#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib
# import seaborn as sns
import sys
import datetime
import glob
import pandas as pd
from itertools import cycle
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
mpl.rcParams.update({'figure.max_open_warning': 0})
mpl.rcParams.update({"font.size": 34,"figure.autolayout": True})
mpl.rc("axes", edgecolor="0.8")
plt.rcParams["font.family"] = "Helvetica Neue"

legendsize = 40

red = "#a93226"
blue = "#2874a6"
green = "#1e8449"

def plot_fig_quicksilver():
    columns = ["groupsize","100k_10b","200k_10b","200k_20b"]
    hist = pd.read_csv("hist_quicksilver.csv", usecols=columns)

    plt.plot(hist.groupsize, hist.iloc[:,1], linestyle=':', marker='o', markersize=6, color=red, label="N = 100k, 10 groups (HOLMES)")
    plt.plot(hist.groupsize, hist.iloc[:,2], linestyle='--', marker='o', markersize=6, color=blue, label="N = 100k, 10 groups (HOLMES)")
    plt.plot(hist.groupsize, hist.iloc[:,3], linestyle='-.', marker='o', markersize=6, color=green, label="N = 200k, 20 groups (HOLMES)")

    axes = plt.gca()
    axes.set_ylim([0,18])

    plt.legend(ncol=1, columnspacing=0.2, fontsize=13, loc = [0.04, 0.6])

    plt.ylabel("Time (s)",fontsize=15)
    plt.yticks(np.arange(0,18,5), fontsize=15)
    plt.xlabel("Range size of each group", fontsize=15)
    xts = [4, 6, 8, 10, 12]
    plt.xticks(xts, ["$2^{4}$", "$2^{6}$", "$2^{8}$", "$2^{10}$", "$2^{12}$"], fontsize=15)

    fig = plt.gcf()
    fig.set_size_inches(6,4, forward=True)

    pp = PdfPages('plot_group_check_quicksilver.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()
    plt.cla()

def plot_fig_mpc():
    columns = ["groupsize","100k_10b","200k_10b","200k_20b"]
    hist = pd.read_csv("hist_mpc.csv", usecols=columns)

    plt.plot(hist.groupsize, hist.iloc[:,1], linestyle=':', marker='o', markersize=6, color=red, label="N = 100k, 10 groups (Baseline)")
    plt.plot(hist.groupsize, hist.iloc[:,2], linestyle='--', marker='o', markersize=6, color=blue, label="N = 100k, 10 groups (Baseline)")
    plt.plot(hist.groupsize, hist.iloc[:,3], linestyle='-.', marker='o', markersize=6, color=green, label="N = 200k, 20 groups (Baseline)")

    axes = plt.gca()
    axes.set_ylim([0,365])

    plt.legend(ncol=1, columnspacing=0.2, fontsize=13, loc = [0.04, 0.6])

    plt.ylabel("Time (s)",fontsize=15)
    plt.yticks(np.arange(0,365,60), fontsize=15)
    plt.xlabel("Range size of each group", fontsize=15)
    xts = [4, 6, 8, 10, 12]
    plt.xticks(xts, ["$2^{4}$", "$2^{6}$", "$2^{8}$", "$2^{10}$", "$2^{12}$"], fontsize=15)

    fig = plt.gcf()
    fig.set_size_inches(6,4, forward=True)

    pp = PdfPages('plot_group_check_mpc.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()


if __name__ == "__main__":
    if True:
        plot_fig_quicksilver()
        plot_fig_mpc()