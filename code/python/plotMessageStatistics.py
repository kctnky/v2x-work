import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

# Definitions
MESSAGE_STATISTICS_FILENAME = './../../data/camstat/message_statistics.csv'
PLOT_START_TIME = 300.0
PLOT_END_TIME = 1200.0

# Define data dictionaries
arrInterarrivalTime = [ ]
arrCamSize = [ ]
mapMaxLatency = { }
mapMaxDistance = { }
mapReliableDistance100 = { }
mapReliableDistance95 = { }
mapReliableDistance80 = { }

# Read from station statistics file
line_number = 0
row_time = 0
prev_time = 0
interarrival_time = 0
cam_size = 0
max_latency = 0
max_distance = 0
reliable_distance_100_sum = 0
reliable_distance_95_sum = 0
reliable_distance_80_sum = 0
reliable_distance_data_counter = 0
with open(MESSAGE_STATISTICS_FILENAME, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        line_number += 1
        if line_number == 1:
            continue
        row_time = int(float(row[0]) / 10) * 10
        if row_time < PLOT_START_TIME or row_time > PLOT_END_TIME:
            continue
        if row_time > prev_time:
            if prev_time > 0:
                mapMaxLatency[prev_time] = max_latency
                mapMaxDistance[prev_time] = max_distance
                if reliable_distance_data_counter > 0:
                    mapReliableDistance100[prev_time] = reliable_distance_100_sum / float(reliable_distance_data_counter)
                    mapReliableDistance95[prev_time] = reliable_distance_95_sum / float(reliable_distance_data_counter)
                    mapReliableDistance80[prev_time] = reliable_distance_80_sum / float(reliable_distance_data_counter)
            prev_time = row_time
            max_latency = 0
            max_distance = 0
            reliable_distance_100_sum = 0
            reliable_distance_95_sum = 0
            reliable_distance_80_sum = 0
            reliable_distance_data_counter = 0
        arrInterarrivalTime.append(float(row[2]))
        arrCamSize.append(int(row[4]))
        if float(row[7]) > max_latency:
            max_latency = float(row[7])
        if float(row[8]) > max_distance:
            max_distance = float(row[8])
        if int(row[5]) > 0 and int(row[6]) > 0:
            reliable_distance_100_sum += float(row[9])
            reliable_distance_95_sum += float(row[10])
            reliable_distance_80_sum += float(row[11])
            reliable_distance_data_counter += 1

# Plot interarrival time
figure1, axes1 = plt.subplots(figsize=(8, 6))
figure1.tight_layout(pad=5.0)
axes1.hist(arrInterarrivalTime, bins = np.arange(0.1, 0.51, 0.01) - 0.005, rwidth=0.5)
axes1.xaxis.set_major_locator(MultipleLocator(0.05))
axes1.xaxis.set_minor_locator(AutoMinorLocator(5))
axes1.grid(which='major', color='#CCCCCC', linestyle='--')
axes1.grid(which='minor', color='#CCCCCC', linestyle=':')
axes1.set_title('Interarrival Times')
axes1.set_xlabel('time (s)')

# Plot cam size
figure2, axes2 = plt.subplots(figsize=(8, 6))
figure2.tight_layout(pad=5.0)
axes2.hist(arrCamSize)
axes2.set_title('Cam Lengths')
axes2.set_xlabel('size (bytes)')

# Plot maximum latency
X = mapMaxLatency.keys()
Y = mapMaxLatency.values()
figure3, axes3 = plt.subplots(figsize=(8, 6))
figure3.tight_layout(pad=5.0)
axes3.set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes3.xaxis.set_major_locator(MultipleLocator(300))
axes3.xaxis.set_minor_locator(AutoMinorLocator(5))
axes3.set_ylim(0, 0.005)
axes3.yaxis.set_major_locator(MultipleLocator(0.001))
axes3.yaxis.set_minor_locator(AutoMinorLocator(5))
axes3.grid(which='major', color='#CCCCCC', linestyle='--')
axes3.grid(which='minor', color='#CCCCCC', linestyle=':')
axes3.set_title('Maximum Latency')
axes3.set_xlabel('time (s)')
axes3.set_ylabel('maximum transmission latency\nmeasured per 10 seconds intervals')
axes3.plot(X, Y)

# Plot maximum distance
X = mapMaxDistance.keys()
Y = mapMaxDistance.values()
figure4, axes4 = plt.subplots(figsize=(8, 6))
figure4.tight_layout(pad=5.0)
axes4.set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes4.xaxis.set_major_locator(MultipleLocator(300))
axes4.xaxis.set_minor_locator(AutoMinorLocator(5))
axes4.set_ylim(0, 2500)
axes4.yaxis.set_major_locator(MultipleLocator(500))
axes4.yaxis.set_minor_locator(AutoMinorLocator(5))
axes4.grid(which='major', color='#CCCCCC', linestyle='--')
axes4.grid(which='minor', color='#CCCCCC', linestyle=':')
axes4.set_title('Maximum Distance')
axes4.set_xlabel('time (s)')
axes4.set_ylabel('maximum transmission distance (meters)\nmeasured per 10 seconds intervals')
axes4.plot(X, Y)

# Plot reliable distance 80
X = mapReliableDistance80.keys()
Y = mapReliableDistance80.values()
figure5, axes5 = plt.subplots(figsize=(8, 6))
figure5.tight_layout(pad=5.0)
axes5.set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes5.xaxis.set_major_locator(MultipleLocator(300))
axes5.xaxis.set_minor_locator(AutoMinorLocator(5))
axes5.set_ylim(0, 250)
axes5.yaxis.set_major_locator(MultipleLocator(50))
axes5.yaxis.set_minor_locator(AutoMinorLocator(5))
axes5.grid(which='major', color='#CCCCCC', linestyle='--')
axes5.grid(which='minor', color='#CCCCCC', linestyle=':')
axes5.set_title('80% Distance for Transmitted CAMs')
axes5.set_xlabel('time (s)')
axes5.set_ylabel('mean of 80% distances (meters)\nmeasured per 10 seconds intervals')
axes5.plot(X, Y)

# Plot reliable distance 95
X = mapReliableDistance95.keys()
Y = mapReliableDistance95.values()
figure6, axes6 = plt.subplots(figsize=(8, 6))
figure6.tight_layout(pad=5.0)
axes6.set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes6.xaxis.set_major_locator(MultipleLocator(300))
axes6.xaxis.set_minor_locator(AutoMinorLocator(5))
axes6.set_ylim(0, 250)
axes6.yaxis.set_major_locator(MultipleLocator(50))
axes6.yaxis.set_minor_locator(AutoMinorLocator(5))
axes6.grid(which='major', color='#CCCCCC', linestyle='--')
axes6.grid(which='minor', color='#CCCCCC', linestyle=':')
axes6.set_title('95% Distance for Transmitted CAMs')
axes6.set_xlabel('time (s)')
axes6.set_ylabel('mean of 95% distances (meters)\nmeasured per 10 seconds intervals')
axes6.plot(X, Y)

# Plot reliable distance 100
X = mapReliableDistance100.keys()
Y = mapReliableDistance100.values()
figure7, axes7 = plt.subplots(figsize=(8, 6))
figure7.tight_layout(pad=5.0)
axes7.set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes7.xaxis.set_major_locator(MultipleLocator(300))
axes7.xaxis.set_minor_locator(AutoMinorLocator(5))
axes7.set_ylim(0, 250)
axes7.yaxis.set_major_locator(MultipleLocator(50))
axes7.yaxis.set_minor_locator(AutoMinorLocator(5))
axes7.grid(which='major', color='#CCCCCC', linestyle='--')
axes7.grid(which='minor', color='#CCCCCC', linestyle=':')
axes7.set_title('100% Distance for Transmitted CAMs')
axes7.set_xlabel('time (s)')
axes7.set_ylabel('mean of 100% distances (meters)\nmeasured per 10 seconds intervals')
axes7.plot(X, Y)

# Plot reliable distances all in one
X100 = mapReliableDistance100.keys()
Y100 = mapReliableDistance100.values()
X95 = mapReliableDistance95.keys()
Y95 = mapReliableDistance95.values()
X80 = mapReliableDistance80.keys()
Y80 = mapReliableDistance80.values()
figure8, axes8 = plt.subplots(figsize=(8, 6))
figure8.tight_layout(pad=5.0)
axes8.set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes8.xaxis.set_major_locator(MultipleLocator(300))
axes8.xaxis.set_minor_locator(AutoMinorLocator(5))
axes8.set_ylim(0, 250)
axes8.yaxis.set_major_locator(MultipleLocator(50))
axes8.yaxis.set_minor_locator(AutoMinorLocator(5))
axes8.grid(which='major', color='#CCCCCC', linestyle='--')
axes8.grid(which='minor', color='#CCCCCC', linestyle=':')
axes8.set_title('Comparison of XY% Distances for Transmitted CAMs')
axes8.set_xlabel('time (s)')
axes8.set_ylabel('mean of XY% distances (meters)\nmeasured per 10 seconds intervals')
axes8.plot(X100, Y100)
axes8.plot(X95, Y95)
axes8.plot(X80, Y80)
axes8.legend(['100% Distance', '95% Distance', '80% Distance'], loc ="lower right")


# Show plotted figures
plt.show()