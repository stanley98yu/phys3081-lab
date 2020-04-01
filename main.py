"""Muon lifetime experiment script for automating waveform analysis.
   Stanley Yu, sy2751
"""
from scipy.optimize import curve_fit
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import sys


THRESHOLD = -1.555
N_BINS = 10

def perror(msg):
    print(msg, file=sys.stderr)
    sys.exit()

def avg(data):
    return sum(data) / float(len(data))

def read_waveform_data(filename):
    with open(filename) as f:
        # Skip headers
        line = f.readline()
        while line and line != "Time,Ampl\n":
            line = f.readline()

        if not line:
            perror("No data available.")
            return []
        
        res_x, res_y, line = [], [], f.readline()
        while line:
            time, ampl = line[:-1].split(',')
            try:
                res_x.append(float(time))
                res_y.append(float(ampl))
            except ValueError:
                perror(f"ValueError: {f} could not convert {time},{ampl} to "
                        "float.")
            line = f.readline()
        
    return res_x, res_y
      
def find_distance(res_x, res_y):
    i1, i2 = -1, -1
    n = len(res_y)
    for i in range(n):
        if res_y[i] > THRESHOLD:
            i1 = i
            break
    
    for i in range(n-1, -1, -1):
        if res_y[i] > THRESHOLD:
            i2 = i
            break
    
    return res_x[i2] - res_x[i1]

def waveform_plot(data_x, data_y):
    plt.figure(figsize=(30,20))
    plt.plot([1e6 * x for x in data_x], data_y)
    plt.xlabel('Time (microsec)')
    plt.ylabel('Voltage (V)')
    plt.show()

def plot_lifetime(data_path):
    """Graphs a histogram of all muon lifetimes in a given dir and returns
       the average lifetime
    """
    # List all filenames
    fnames = [os.path.join(data_path, f) for f in os.listdir(data_path)
              if os.path.isfile(os.path.join(data_path, f))]

    lifetimes = []
    for fn in tqdm(fnames):
        res_x, res_y = read_waveform_data(fn)
        lifetimes.append(1e6 * find_distance(res_x, res_y))

    fig, ax = plt.subplots(figsize=(15,10))
    counts, bins, _ = ax.hist(lifetimes, bins=N_BINS)
    x_bins = [(bins[i + 1] + bins[i]) / 2.0 for i in range(len(bins) - 1)]
    ax.scatter(x_bins, counts, c='k')

    # Exponential curve-fitting
    def exp_fun(x, a, b, c):
        return a * np.exp(-b * x) + c
    x_bins = np.array(x_bins)
    counts = np.array(counts)
    popt, pcov = curve_fit(exp_fun, x_bins, counts)
    ax.plot(x_bins, exp_fun(x_bins, *popt), 'r-')

    se = np.square(counts - exp_fun(x_bins, *popt))
    std = [math.sqrt(s / N_BINS) for s in se]
    ax.errorbar(x_bins, counts, yerr=std,
                linestyle="None", elinewidth=2, capsize=2, color="red")

    textstr = '\n'.join((
        "Model: a * exp(-b * x) + c",
        r'$a=%.3f$' % (popt[0], ),
        r'$b=%.3f$' % (popt[1], ),
        r'$c=%.3f$' % (popt[2], )))
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.75, 0.95, textstr, transform=ax.transAxes, fontsize=14,   
        verticalalignment='top', bbox=props)

    ax.set_title('Muon Lifetime Distribution')
    ax.set_xlabel('Lifetime (microsec)')
    ax.set_ylabel('Count')
    fig.tight_layout()
    plt.show()

    return lifetimes

if __name__ == '__main__':
    # Verify that waveform analysis works.
    # data_x, data_y = read_waveform_data("data/C1nov15pr00987.txt")
    # find_distance(data_x, data_y)
    # waveform_plot(data_x, data_y)
    
    lf = plot_lifetime("data/")
    print(f"Average Muon Lifetime (microsec): {avg(lf)} +/- " \
          f"{avg(lf) / math.sqrt(len(lf))}")

    with open('result.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(x) for x in lf])
