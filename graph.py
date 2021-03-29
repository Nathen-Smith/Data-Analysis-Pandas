# check if stats.txt exists

# read each line from stats.txt
# for each second aggregate size and delay

# stats.txt format:
# timestamp(sec) size(bytes) delay(sec)

# create 2 graphs displaying bits(size*8)/sec, avg_delay(in ms, sec*1000)/sec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

STATS_FILE = 'stats.txt'

with open(STATS_FILE) as f:
    input_lines = np.array([[float(elem) for elem in line.strip().split()] for line in f])
    #input lines are a 2d array. input[i][j], 0 <= j <= 2, gives information for event i

# take input_lines[0][0] - input_lines[0][2] as time zero.
# go until input_lines[i][0] = t_0 + 100
t0 = input_lines[0][0] - input_lines[0][2]
rows = len(input_lines)

i = 0 # the index on entry in stats file
secondIdx = 0
secondArr = []
# data
minArr = []
maxArr = []
medianArr = []
ninetyth = []

currLine = 0
receivedFlag = 0
for s in range(int(t0), int(input_lines[-1][0] + 1)):
    secondArr.append(s - int(t0))
    if currLine < len(input_lines) and input_lines[currLine][0] >= s and input_lines[currLine][0] < s + 1:
        # get all delays within this second
        currSecond = []
        while input_lines[currLine][0] < s + 1:
            currSecond.append(input_lines[currLine][2])
            currLine = currLine + 1
            receivedFlag = 1
            if currLine == len(input_lines):
                break
    if receivedFlag == 1:
        minArr.append(min(currSecond))
        maxArr.append(max(currSecond))
        medianArr.append(np.quantile(currSecond, 0.5))
        ninetyth.append(np.quantile(currSecond, 0.9))
    else:
        minArr.append(0)
        maxArr.append(0)
        medianArr.append(0)
        ninetyth.append(0)
    receivedFlag = 0

df = pd.DataFrame(np.c_[minArr, medianArr, ninetyth, maxArr], index=secondArr)
plt.figure(figsize=(18,8))
df.plot.bar(ax = plt.gca())
plt.xticks(rotation=90)
plt.xlabel('Delay Statistics at each Second')
plt.ylabel('Length of Delay (s)')
plt.title('Delay Statistics Over 100 Seconds')
plt.legend(['Minimum', 'Median', '90th Percentile', 'Maximum'])
plt.savefig('delays.png') # needs to be before show. show creates another figure
plt.show()

# bandwidth: total amount of bytes recieved in a second. plot in Kbps or Mbps
bandwidthSumArr = []
secondArr = []
currLine = 0
for s in range(int(t0), int(input_lines[-1][0] + 1)):
    secondArr.append(s - t0)
    bandwidthSum = 0
    if currLine < len(input_lines) and input_lines[currLine][0] >= s and input_lines[currLine][0] < s + 1:
        # get all events within this second
        while input_lines[currLine][0] < s + 1:
            bandwidthSum = bandwidthSum + input_lines[currLine][1]
            currLine = currLine + 1
            if currLine == len(input_lines):
                break
    bandwidthSumArr.append(bandwidthSum * 0.008) #Mbps is 0.000008

plt.figure(figsize=(18,8))
plt.plot(secondArr, bandwidthSumArr)
plt.xlabel('Time (s)')
plt.ylabel('Bandwidth (Kbps)')
plt.title('Bandwidth per Second')
plt.savefig('bandwidths.png')
plt.show()
