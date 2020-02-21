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
      
def find_distance(res_x, res_y):
   first_index = -1
   second_index = -1
   threshold = -1.555
   for i in range(len(res_y)):
      if res_y[i] > threshold and first_index == -1:
         first_index = i
      else if res_y[i] > threshold and first_index != -1:
         second_index = i
   return res_x[second_index] - res_x[first_index]
         
def basic_plot(data_x, data_y):
    plt.figure(figsize=(30,20))
    plt.plot(data_x, data_y)
    plt.xlabel('time (microsec)')
    plt.ylabel('voltage (V)')
    plt.show()

if __name__ == '__main__':
    data_x, data_y = read_waveform_data("trial1/C1nov15pr00000.txt")
    print(find_distance(data_x, data_y))
    basic_plot(data_x, data_y)
    
