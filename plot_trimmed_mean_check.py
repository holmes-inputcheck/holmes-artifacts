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
    columns = ["threshold","100k", "200k"]
    trimmed_qs = pd.read_csv("trimmed_quicksilver.csv", usecols=columns)

    plt.plot(trimmed_qs.threshold, trimmed_qs.iloc[:,1], linestyle=':', marker='o', markersize=6, color=red, label="N = 100k (HOLMES)")
    plt.plot(trimmed_qs.threshold, trimmed_qs.iloc[:,2], linestyle='--', marker='o', markersize=6, color=blue, label="N = 200k (HOLMES)")

    axes = plt.gca()
    axes.set_ylim([0,10])

    plt.legend(ncol=1, columnspacing=0.2, fontsize=13, loc = [0.04, 0.7])

    plt.ylabel("Time (s)",fontsize=15)
    plt.yticks(np.arange(0,10,3), fontsize=15)
    plt.xlabel("Threshold", fontsize=15)
    xts = [8, 12, 16, 20, 24]
    plt.xticks(xts, ["$2^8$", "$2^{12}$", "$2^{16}$", "$2^{20}$", "$2^{24}$"], fontsize=15)

    fig = plt.gcf()
    fig.set_size_inches(6,4, forward=True)

    pp = PdfPages('plot_trimmed_mean_quicksilver.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()
    plt.cla()

def plot_fig_mpc():
    columns = ["threshold","100k", "200k"]
    trimmed_mpc = pd.read_csv("trimmed_mpc.csv", usecols=columns)

    plt.plot(trimmed_mpc.threshold, trimmed_mpc.iloc[:,1], linestyle=':', marker='o', markersize=6, color=red, label="N = 100k (Baseline)")
    plt.plot(trimmed_mpc.threshold, trimmed_mpc.iloc[:,2], linestyle='--', marker='o', markersize=6, color=blue, label="N = 200k (Baseline)")

    axes = plt.gca()
    axes.set_ylim([0,145])

    plt.legend(ncol=1, columnspacing=0.2, fontsize=13, loc = [0.04, 0.7])

    plt.ylabel("Time (s)",fontsize=15)
    plt.yticks(np.arange(0,145,20), fontsize=15)
    plt.xlabel("Range size", fontsize=15)
    xts = [8, 12, 16, 20, 24]
    plt.xticks(xts, ["$2^8$", "$2^{12}$", "$2^{16}$", "$2^{20}$", "$2^{24}$"], fontsize=15)

    fig = plt.gcf()
    fig.set_size_inches(6,4, forward=True)

    pp = PdfPages('plot_trimmed_mean_mpc.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()


if __name__ == "__main__":
    if True:
        plot_fig_quicksilver()
        plot_fig_mpc()