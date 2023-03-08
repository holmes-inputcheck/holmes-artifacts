#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib
import pandas as pd
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
mpl.rcParams['text.latex.preamble'] = [r'\usepackage{amsmath,mathptmx}']

warnings.filterwarnings('ignore')
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams.update({'figure.max_open_warning': 0})
mpl.rcParams.update({"font.size": 34,"figure.autolayout": True})
mpl.rc("axes", edgecolor="0.8")
plt.rcParams["font.family"] = "Helvetica Neue"

red = "#a93226"
blue = "#2874a6"
green = "#1e8449"

def plot_fig_quicksilver():
    columns = ["num_parties","zk"]
    marketing = pd.read_csv("marketing.csv", usecols=columns)


    plt.plot(marketing.num_parties, marketing.zk, linestyle=':', marker='o', markersize=6, color=red, label="HOLMES")
    #plt.plot(x, y2, linestyle='--', marker='o', markersize=6, color=blue, label=" Baseline")

    axes = plt.gca()
    axes.set_ylim([0, 125])

    plt.legend(ncol=1, columnspacing=0.2, fontsize=20, loc = [0.04, 0.6])

    plt.ylabel("Time (s)",fontsize=25)
    plt.yticks(np.arange(0,301,50), fontsize=25)
    plt.xlabel("Number of parties", fontsize=25)
    plt.xticks([2, 4, 6, 8, 10], fontsize=25)

    fig = plt.gcf()
    fig.set_size_inches(6,4, forward=True)
    

    pp = PdfPages('plot_marketing_dataset_quicksilver.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()
    plt.cla()

def plot_fig_mpc():
    columns = ["num_parties","mpc"]
    marketing = pd.read_csv("marketing.csv", usecols=columns)

    plt.plot(marketing.num_parties, marketing.mpc, linestyle='--', marker='o', markersize=6, color=blue, label="Baseline (k=40)")

    axes = plt.gca()
    axes.set_ylim([0,30001])

    plt.legend(ncol=1, columnspacing=0.2, fontsize=20, loc = [0.04, 0.6])

    plt.ylabel("Time (s)",fontsize=25)
    plt.yticks(np.arange(0,30001,10000), fontsize=25)
    plt.xlabel("Number of parties", fontsize=25)
    plt.xticks([2, 4, 6, 8, 10], fontsize=25)

    fig = plt.gcf()
    fig.set_size_inches(6,4, forward=True)

    pp = PdfPages('plot_marketing_dataset_mpc.pdf')
    plt.savefig(pp, format='pdf', bbox_inches='tight', dpi=fig.dpi)
    pp.close()

if __name__ == "__main__":
    if True:
        plot_fig_quicksilver()
        plot_fig_mpc()