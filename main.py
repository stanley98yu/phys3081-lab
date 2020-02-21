"""Muon lifetime experiment script for automating waveform analysis.
   Stanley Yu, sy2751
"""
import matplotlib.pyplot as plt
import sys

def perror(msg):
    print(msg, file=sys.stderr)

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
            res_x.append(float(time))
            res_y.append(float(ampl))
            line = f.readline()
        
        return res_x, res_y

def basic_plot(data_x, data_y):
    plt.figure(figsize=(30,20))
    plt.plot(data_x, data_y)
    plt.xlabel('time (microsec)')
    plt.ylabel('voltage (V)')
    plt.show()

if __name__ == '__main__':
    data_x, data_y = read_waveform_data("trial1/C1nov15pr00000.txt")
    basic_plot(data_x, data_y)
    
