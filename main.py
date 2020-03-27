"""Muon lifetime experiment script for automating waveform analysis.
   Stanley Yu, sy2751
"""
from tqdm import tqdm
import csv
import matplotlib.pyplot as plt
import os
import sys


THRESHOLD = -1.555

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

    plt.figure(figsize=(30,20))
    plt.hist(lifetimes, bins=40)
    plt.xlabel('Lifetime (microsec)')
    plt.ylabel('Count')
    plt.show()

    return lifetimes

if __name__ == '__main__':
    # Verify that waveform analysis works.
    data_x, data_y = read_waveform_data("data/C1nov15pr00987.txt")
    find_distance(data_x, data_y)
    waveform_plot(data_x, data_y)
    
    lf = plot_lifetime("data/")
    print(f"Average Muon Lifetime (microsec): {avg(lf)}")

    with open('result.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([str(x) for x in lf])
