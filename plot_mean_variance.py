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
    columns = ["num_instances","mv"]
    mv_qs = pd.read_csv("mv_quicksilver.csv", usecols=columns)

    plt.plot(mv_qs.num_instances, mv_qs.mv, linestyle=':', marker='o', markersize=6, linewidth = 3, color=red, label="HOLMES")

    axes = plt.gca()
    axes.set_ylim([0,37])

    plt.legend(ncol=1, columnspacing=0.2, fontsize=13, loc = [0.04, 0.7])

    plt.ylabel("Time (s)",fontsize=15)
    plt.yticks(np.arange(0,41,10), fontsize=15)
    plt.xlabel("Number of instances", fontsize=15)
    xts = [1000000, 2000000, 3000000, 4000000, 5000000]
    plt.xticks(xts, ["$1\\times10^6$", "$2\\times10^6$", "$3\\times10^6$", "$4\\times10^6$", "$5\\times10^6$"], fontsize=15)

    fig = plt.gcf()
    fig.set_size_inches(6,4, forward=True)

    pp = PdfPages('plot_mean_variance_quicksilver.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()
    plt.cla()

def plot_fig_mpc():
    columns = ["num_instances","mv"]
    mv_mpc = pd.read_csv("mv_mpc.csv", usecols=columns)

    plt.plot(mv_mpc.num_instances, mv_mpc.mv, linestyle='--', marker='o', markersize=6, color=blue, label="Baseline")

    axes = plt.gca()
    axes.set_ylim([0, 205])

    plt.legend(ncol=1, columnspacing=0.2, fontsize=13, loc = [0.04, 0.7])

    plt.ylabel("Time (s)",fontsize=15)
    plt.yticks(np.arange(0, 205,40), fontsize=15)
    plt.xlabel("Number of instances", fontsize=15)
    xts = [1000000, 2000000, 3000000, 4000000, 5000000]
    plt.xticks(xts, ["$1\\times10^6$", "$2\\times10^6$", "$3\\times10^6$", "$4\\times10^6$", "$5\\times10^6$"], fontsize=15)

    fig = plt.gcf()
    fig.set_size_inches(6,4, forward=True)

    pp = PdfPages('plot_mean_variance_mpc.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()


if __name__ == "__main__":
    if True:
        plot_fig_quicksilver()
        plot_fig_mpc()