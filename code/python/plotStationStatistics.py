import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

# Definitions
STATION_STATISTICS_FILENAME = './../../data/camstat/station_statistics.csv'
PLOT_START_TIME = 0.0
PLOT_END_TIME = 1200.0

# Define data dictionaries
mapAverageChannelLoad = { }
mapTotalNumberOfCollisions = { }
mapDeltaNumberOfCollisions = { }
mapPacketReceptionRatio = { }
mapUnknownRatio_50 = { }
mapAveragePositionError_50 = { }
mapMaximumPositionError_50 = { }
mapUnknownRatio_100 = { }
mapAveragePositionError_100 = { }
mapMaximumPositionError_100 = { }
mapUnknownRatio_200 = { }
mapAveragePositionError_200 = { }
mapMaximumPositionError_200 = { }
mapUnknownRatio_300 = { }
mapAveragePositionError_300 = { }
mapMaximumPositionError_300 = { }
mapUnknownRatio_400 = { }
mapAveragePositionError_400 = { }
mapMaximumPositionError_400 = { }
mapUnknownRatio_500 = { }
mapAveragePositionError_500 = { }
mapMaximumPositionError_500 = { }
mapUnknownRatio_1000 = { }
mapAveragePositionError_1000 = { }
mapMaximumPositionError_1000 = { }

# Read from station statistics file
line_number = 0
row_time = 0
prev_time = 0
data_count_per_time = 0
channel_load = 0
total_collision = 0
delta_collision = 0
delta_recevied = 0
unknown_ratio_50 = 0
avg_position_error_50 = 0
max_position_error_50 = 0
unknown_ratio_100 = 0
avg_position_error_100 = 0
max_position_error_100 = 0
unknown_ratio_200 = 0
avg_position_error_200 = 0
max_position_error_200 = 0
unknown_ratio_300 = 0
avg_position_error_300 = 0
max_position_error_300 = 0
unknown_ratio_400 = 0
avg_position_error_400 = 0
max_position_error_400 = 0
unknown_ratio_500 = 0
avg_position_error_500 = 0
max_position_error_500 = 0
unknown_ratio_1000 = 0
avg_position_error_1000 = 0
max_position_error_1000 = 0

with open(STATION_STATISTICS_FILENAME, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        line_number += 1
        if line_number == 1:
            continue
        row_time = float(row[0])
        if row_time < PLOT_START_TIME or row_time > PLOT_END_TIME:
            continue
        if row_time > prev_time:
            if prev_time > 0:
                mapAverageChannelLoad[prev_time] = channel_load / data_count_per_time
                mapTotalNumberOfCollisions[prev_time] = total_collision
                mapDeltaNumberOfCollisions[prev_time] = delta_collision
                if delta_recevied > 0:
                    mapPacketReceptionRatio[prev_time] = float(delta_recevied - delta_collision) / float(delta_recevied)
                mapUnknownRatio_50[prev_time] = unknown_ratio_50 / data_count_per_time
                mapAveragePositionError_50[prev_time] = avg_position_error_50 / data_count_per_time
                mapMaximumPositionError_50[prev_time] = max_position_error_50
                mapUnknownRatio_100[prev_time] = unknown_ratio_100 / data_count_per_time
                mapAveragePositionError_100[prev_time] = avg_position_error_100 / data_count_per_time
                mapMaximumPositionError_100[prev_time] = max_position_error_100
                mapUnknownRatio_200[prev_time] = unknown_ratio_200 / data_count_per_time
                mapAveragePositionError_200[prev_time] = avg_position_error_200 / data_count_per_time
                mapMaximumPositionError_200[prev_time] = max_position_error_200
                mapUnknownRatio_300[prev_time] = unknown_ratio_300 / data_count_per_time
                mapAveragePositionError_300[prev_time] = avg_position_error_300 / data_count_per_time
                mapMaximumPositionError_300[prev_time] = max_position_error_300
                mapUnknownRatio_400[prev_time] = unknown_ratio_400 / data_count_per_time
                mapAveragePositionError_400[prev_time] = avg_position_error_400 / data_count_per_time
                mapMaximumPositionError_400[prev_time] = max_position_error_400
                mapUnknownRatio_500[prev_time] = unknown_ratio_500 / data_count_per_time
                mapAveragePositionError_500[prev_time] = avg_position_error_500 / data_count_per_time
                mapMaximumPositionError_500[prev_time] = max_position_error_500
                mapUnknownRatio_1000[prev_time] = unknown_ratio_1000 / data_count_per_time
                mapAveragePositionError_1000[prev_time] = avg_position_error_1000 / data_count_per_time
                mapMaximumPositionError_1000[prev_time] = max_position_error_1000
            prev_time = row_time
            data_count_per_time = 0
            channel_load = 0
            delta_collision = 0
            delta_recevied = 0
            unknown_ratio_50 = 0
            avg_position_error_50 = 0
            max_position_error_50 = 0
            unknown_ratio_100 = 0
            avg_position_error_100 = 0
            max_position_error_100 = 0
            unknown_ratio_200 = 0
            avg_position_error_200 = 0
            max_position_error_200 = 0
            unknown_ratio_300 = 0
            avg_position_error_300 = 0
            max_position_error_300 = 0
            unknown_ratio_400 = 0
            avg_position_error_400 = 0
            max_position_error_400 = 0
            unknown_ratio_500 = 0
            avg_position_error_500 = 0
            max_position_error_500 = 0 
            unknown_ratio_1000 = 0
            avg_position_error_1000 = 0
            max_position_error_1000 = 0       
        data_count_per_time += 1
        channel_load += float(row[2])
        total_collision += int(row[3])
        delta_collision += int(row[5])
        delta_recevied += int(row[6])
        unknown_ratio_50 += float(row[7])
        avg_position_error_50 += float(row[8])
        if float(row[9]) > max_position_error_50:
            max_position_error_50 = float(row[9])
        unknown_ratio_100 += float(row[10])
        avg_position_error_100 += float(row[11])
        if float(row[12]) > max_position_error_100:
            max_position_error_100 = float(row[12])
        unknown_ratio_200 += float(row[13])
        avg_position_error_200 += float(row[14])
        if float(row[15]) > max_position_error_200:
            max_position_error_200 = float(row[15])
        unknown_ratio_300 += float(row[16])
        avg_position_error_300 += float(row[17])
        if float(row[18]) > max_position_error_300:
            max_position_error_300 = float(row[18])
        unknown_ratio_400 += float(row[19])
        avg_position_error_400 += float(row[20])
        if float(row[21]) > max_position_error_400:
            max_position_error_400 = float(row[21])
        unknown_ratio_500 += float(row[22])
        avg_position_error_500 += float(row[23])
        if float(row[24]) > max_position_error_500:
            max_position_error_500 = float(row[24])
        unknown_ratio_1000 += float(row[25])
        avg_position_error_1000 += float(row[26])
        if float(row[27]) > max_position_error_1000:
            max_position_error_1000 = float(row[27])

# Plot channel load
X = mapAverageChannelLoad.keys()
Y = mapAverageChannelLoad.values()
figure1, axes1 = plt.subplots(figsize=(8, 6))
figure1.tight_layout(pad=5.0)
axes1.set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes1.xaxis.set_major_locator(MultipleLocator(300))
axes1.xaxis.set_minor_locator(AutoMinorLocator(5))
axes1.grid(which='major', color='#CCCCCC', linestyle='--')
axes1.grid(which='minor', color='#CCCCCC', linestyle=':')
axes1.set_title('Channel Load vs Time')
axes1.set_xlabel('time (s)')
axes1.set_ylabel('average channel load measured by vehicles')
axes1.scatter(X, Y, s=0.5)

# Plot collision statistics
X1 = mapTotalNumberOfCollisions.keys()
Y1 = mapTotalNumberOfCollisions.values()
X2 = mapDeltaNumberOfCollisions.keys()
Y2 = mapDeltaNumberOfCollisions.values()
figure2, axes2 = plt.subplots(2, figsize=(8, 8))
figure2.tight_layout(pad=5.0)
# Create figure 1
axes2[0].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes2[0].xaxis.set_major_locator(MultipleLocator(300))
axes2[0].xaxis.set_minor_locator(AutoMinorLocator(5))
axes2[0].grid(which='major', color='#CCCCCC', linestyle='--')
axes2[0].grid(which='minor', color='#CCCCCC', linestyle=':')
axes2[0].set_title('Total Number of Collisions')
axes2[0].set_xlabel('time (s)')
axes2[0].set_ylabel('# collisions')
axes2[0].scatter(X1, Y1, s=0.5)
# Create figure 2
axes2[1].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes2[1].xaxis.set_major_locator(MultipleLocator(300))
axes2[1].xaxis.set_minor_locator(AutoMinorLocator(5))
axes2[1].grid(which='major', color='#CCCCCC', linestyle='--')
axes2[1].grid(which='minor', color='#CCCCCC', linestyle=':')
axes2[1].set_title('Delta Number of Collisions')
axes2[1].set_xlabel('time (s)')
axes2[1].set_ylabel('# collisions per 0.5 sec intervals')
axes2[1].scatter(X2, Y2, s=0.5)

# Plot packet reception ratio
X = mapPacketReceptionRatio.keys()
Y = mapPacketReceptionRatio.values()
figure3, axes3 = plt.subplots(figsize=(8, 6))
figure3.tight_layout(pad=5.0)
axes3.set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes3.xaxis.set_major_locator(MultipleLocator(300))
axes3.xaxis.set_minor_locator(AutoMinorLocator(5))
axes3.set_ylim(0.95, 1)
axes3.yaxis.set_major_locator(MultipleLocator(0.05))
axes3.yaxis.set_minor_locator(AutoMinorLocator(5))
axes3.grid(which='major', color='#CCCCCC', linestyle='--')
axes3.grid(which='minor', color='#CCCCCC', linestyle=':')
axes3.set_title('Packet Reception Ratio')
axes3.set_xlabel('time (s)')
axes3.set_ylabel('packet reception ratio per 0.5 sec intervals')
axes3.scatter(X, Y, s=0.5)

# Plot position errors for roi distance 50m
X1 = mapAveragePositionError_50.keys()
Y1 = mapAveragePositionError_50.values()
X2 = mapMaximumPositionError_50.keys()
Y2 = mapMaximumPositionError_50.values()
X3 = mapUnknownRatio_50.keys()
Y3 = mapUnknownRatio_50.values()
figure4, axes4 = plt.subplots(3, figsize=(8, 12))
figure4.tight_layout(pad=5.0)
# Create figure 1
axes4[0].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes4[0].xaxis.set_major_locator(MultipleLocator(300))
axes4[0].xaxis.set_minor_locator(AutoMinorLocator(5))
axes4[0].set_ylim(0, 25)
axes4[0].yaxis.set_major_locator(MultipleLocator(5))
axes4[0].yaxis.set_minor_locator(AutoMinorLocator(5))
axes4[0].grid(which='major', color='#CCCCCC', linestyle='--')
axes4[0].grid(which='minor', color='#CCCCCC', linestyle=':')
axes4[0].set_title('Mean Position Error (ROI = 50 meters)')
axes4[0].set_xlabel('time (s)')
axes4[0].set_ylabel('mean of position errors (m)\ncollected per 0.5 sec intervals')
axes4[0].scatter(X1, Y1, s=0.5)
# Create figure 2
axes4[1].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes4[1].xaxis.set_major_locator(MultipleLocator(300))
axes4[1].xaxis.set_minor_locator(AutoMinorLocator(5))
axes4[1].set_ylim(0, 125)
axes4[1].yaxis.set_major_locator(MultipleLocator(25))
axes4[1].yaxis.set_minor_locator(AutoMinorLocator(5))
axes4[1].grid(which='major', color='#CCCCCC', linestyle='--')
axes4[1].grid(which='minor', color='#CCCCCC', linestyle=':')
axes4[1].set_title('Maximum Position Error (ROI = 50 meters)')
axes4[1].set_xlabel('time (s)')
axes4[1].set_ylabel('maximum of position errors (m)\ncollected per 0.5 sec intervals')
axes4[1].scatter(X2, Y2, s=0.5)
# Create figure 3
axes4[2].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes4[2].xaxis.set_major_locator(MultipleLocator(300))
axes4[2].xaxis.set_minor_locator(AutoMinorLocator(5))
axes4[2].set_ylim(0, 0.5)
axes4[2].yaxis.set_major_locator(MultipleLocator(0.1))
axes4[2].yaxis.set_minor_locator(AutoMinorLocator(5))
axes4[2].grid(which='major', color='#CCCCCC', linestyle='--')
axes4[2].grid(which='minor', color='#CCCCCC', linestyle=':')
axes4[2].set_title('Unknown Vehicle Ratio (ROI = 50 meters)')
axes4[2].set_xlabel('time (s)')
axes4[2].set_ylabel('ratio of unknown vehicles\ncollected per 0.5 sec intervals')
axes4[2].scatter(X3, Y3, s=0.5)

# Plot position errors for roi distance 100m
X1 = mapAveragePositionError_100.keys()
Y1 = mapAveragePositionError_100.values()
X2 = mapMaximumPositionError_100.keys()
Y2 = mapMaximumPositionError_100.values()
X3 = mapUnknownRatio_100.keys()
Y3 = mapUnknownRatio_100.values()
figure5, axes5 = plt.subplots(3, figsize=(8, 12))
figure5.tight_layout(pad=5.0)
# Create figure 1
axes5[0].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes5[0].xaxis.set_major_locator(MultipleLocator(300))
axes5[0].xaxis.set_minor_locator(AutoMinorLocator(5))
axes5[0].set_ylim(0, 25)
axes5[0].yaxis.set_major_locator(MultipleLocator(5))
axes5[0].yaxis.set_minor_locator(AutoMinorLocator(5))
axes5[0].grid(which='major', color='#CCCCCC', linestyle='--')
axes5[0].grid(which='minor', color='#CCCCCC', linestyle=':')
axes5[0].set_title('Mean Position Error (ROI = 100 meters)')
axes5[0].set_xlabel('time (s)')
axes5[0].set_ylabel('mean of position errors (m)\ncollected per 0.5 sec intervals')
axes5[0].scatter(X1, Y1, s=0.5)
# Create figure 2
axes5[1].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes5[1].xaxis.set_major_locator(MultipleLocator(300))
axes5[1].xaxis.set_minor_locator(AutoMinorLocator(5))
axes5[1].set_ylim(0, 125)
axes5[1].yaxis.set_major_locator(MultipleLocator(25))
axes5[1].yaxis.set_minor_locator(AutoMinorLocator(5))
axes5[1].grid(which='major', color='#CCCCCC', linestyle='--')
axes5[1].grid(which='minor', color='#CCCCCC', linestyle=':')
axes5[1].set_title('Maximum Position Error (ROI = 100 meters)')
axes5[1].set_xlabel('time (s)')
axes5[1].set_ylabel('maximum of position errors (m)\ncollected per 0.5 sec intervals')
axes5[1].scatter(X2, Y2, s=0.5)
# Create figure 3
axes5[2].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes5[2].xaxis.set_major_locator(MultipleLocator(300))
axes5[2].xaxis.set_minor_locator(AutoMinorLocator(5))
axes5[2].set_ylim(0, 0.5)
axes5[2].yaxis.set_major_locator(MultipleLocator(0.1))
axes5[2].yaxis.set_minor_locator(AutoMinorLocator(5))
axes5[2].grid(which='major', color='#CCCCCC', linestyle='--')
axes5[2].grid(which='minor', color='#CCCCCC', linestyle=':')
axes5[2].set_title('Unknown Vehicle Ratio (ROI = 100 meters)')
axes5[2].set_xlabel('time (s)')
axes5[2].set_ylabel('ratio of unknown vehicles\ncollected per 0.5 sec intervals')
axes5[2].scatter(X3, Y3, s=0.5)

# Plot position errors for roi distance 200m
X1 = mapAveragePositionError_200.keys()
Y1 = mapAveragePositionError_200.values()
X2 = mapMaximumPositionError_200.keys()
Y2 = mapMaximumPositionError_200.values()
X3 = mapUnknownRatio_200.keys()
Y3 = mapUnknownRatio_200.values()
figure6, axes6 = plt.subplots(3, figsize=(8, 12))
figure6.tight_layout(pad=5.0)
# Create figure 1
axes6[0].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes6[0].xaxis.set_major_locator(MultipleLocator(300))
axes6[0].xaxis.set_minor_locator(AutoMinorLocator(5))
axes6[0].set_ylim(0, 25)
axes6[0].yaxis.set_major_locator(MultipleLocator(5))
axes6[0].yaxis.set_minor_locator(AutoMinorLocator(5))
axes6[0].grid(which='major', color='#CCCCCC', linestyle='--')
axes6[0].grid(which='minor', color='#CCCCCC', linestyle=':')
axes6[0].set_title('Mean Position Error (ROI = 200 meters)')
axes6[0].set_xlabel('time (s)')
axes6[0].set_ylabel('mean of position errors (m)\ncollected per 0.5 sec intervals')
axes6[0].scatter(X1, Y1, s=0.5)
# Create figure 2
axes6[1].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes6[1].xaxis.set_major_locator(MultipleLocator(300))
axes6[1].xaxis.set_minor_locator(AutoMinorLocator(5))
axes6[1].set_ylim(0, 125)
axes6[1].yaxis.set_major_locator(MultipleLocator(25))
axes6[1].yaxis.set_minor_locator(AutoMinorLocator(5))
axes6[1].grid(which='major', color='#CCCCCC', linestyle='--')
axes6[1].grid(which='minor', color='#CCCCCC', linestyle=':')
axes6[1].set_title('Maximum Position Error (ROI = 200 meters)')
axes6[1].set_xlabel('time (s)')
axes6[1].set_ylabel('maximum of position errors (m)\ncollected per 0.5 sec intervals')
axes6[1].scatter(X2, Y2, s=0.5)
# Create figure 3
axes6[2].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes6[2].xaxis.set_major_locator(MultipleLocator(300))
axes6[2].xaxis.set_minor_locator(AutoMinorLocator(5))
axes6[2].set_ylim(0, 0.5)
axes6[2].yaxis.set_major_locator(MultipleLocator(0.1))
axes6[2].yaxis.set_minor_locator(AutoMinorLocator(5))
axes6[2].grid(which='major', color='#CCCCCC', linestyle='--')
axes6[2].grid(which='minor', color='#CCCCCC', linestyle=':')
axes6[2].set_title('Unknown Vehicle Ratio (ROI = 200 meters)')
axes6[2].set_xlabel('time (s)')
axes6[2].set_ylabel('ratio of unknown vehicles\ncollected per 0.5 sec intervals')
axes6[2].scatter(X3, Y3, s=0.5)

# Plot position errors for roi distance 300m
X1 = mapAveragePositionError_300.keys()
Y1 = mapAveragePositionError_300.values()
X2 = mapMaximumPositionError_300.keys()
Y2 = mapMaximumPositionError_300.values()
X3 = mapUnknownRatio_300.keys()
Y3 = mapUnknownRatio_300.values()
figure7, axes7 = plt.subplots(3, figsize=(8, 12))
figure7.tight_layout(pad=5.0)
# Create figure 1
axes7[0].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes7[0].xaxis.set_major_locator(MultipleLocator(300))
axes7[0].xaxis.set_minor_locator(AutoMinorLocator(5))
axes7[0].set_ylim(0, 25)
axes7[0].yaxis.set_major_locator(MultipleLocator(5))
axes7[0].yaxis.set_minor_locator(AutoMinorLocator(5))
axes7[0].grid(which='major', color='#CCCCCC', linestyle='--')
axes7[0].grid(which='minor', color='#CCCCCC', linestyle=':')
axes7[0].set_title('Mean Position Error (ROI = 300 meters)')
axes7[0].set_xlabel('time (s)')
axes7[0].set_ylabel('mean of position errors (m)\ncollected per 0.5 sec intervals')
axes7[0].scatter(X1, Y1, s=0.5)
# Create figure 2
axes7[1].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes7[1].xaxis.set_major_locator(MultipleLocator(300))
axes7[1].xaxis.set_minor_locator(AutoMinorLocator(5))
axes7[1].set_ylim(0, 125)
axes7[1].yaxis.set_major_locator(MultipleLocator(25))
axes7[1].yaxis.set_minor_locator(AutoMinorLocator(5))
axes7[1].grid(which='major', color='#CCCCCC', linestyle='--')
axes7[1].grid(which='minor', color='#CCCCCC', linestyle=':')
axes7[1].set_title('Maximum Position Error (ROI = 300 meters)')
axes7[1].set_xlabel('time (s)')
axes7[1].set_ylabel('maximum of position errors (m)\ncollected per 0.5 sec intervals')
axes7[1].scatter(X2, Y2, s=0.5)
# Create figure 3
axes7[2].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes7[2].xaxis.set_major_locator(MultipleLocator(300))
axes7[2].xaxis.set_minor_locator(AutoMinorLocator(5))
axes7[2].set_ylim(0, 0.5)
axes7[2].yaxis.set_major_locator(MultipleLocator(0.1))
axes7[2].yaxis.set_minor_locator(AutoMinorLocator(5))
axes7[2].grid(which='major', color='#CCCCCC', linestyle='--')
axes7[2].grid(which='minor', color='#CCCCCC', linestyle=':')
axes7[2].set_title('Unknown Vehicle Ratio (ROI = 300 meters)')
axes7[2].set_xlabel('time (s)')
axes7[2].set_ylabel('ratio of unknown vehicles\ncollected per 0.5 sec intervals')
axes7[2].scatter(X3, Y3, s=0.5)

# Plot position errors for roi distance 400m
X1 = mapAveragePositionError_400.keys()
Y1 = mapAveragePositionError_400.values()
X2 = mapMaximumPositionError_400.keys()
Y2 = mapMaximumPositionError_400.values()
X3 = mapUnknownRatio_400.keys()
Y3 = mapUnknownRatio_400.values()
figure8, axes8 = plt.subplots(3, figsize=(8, 12))
figure8.tight_layout(pad=5.0)
# Create figure 1
axes8[0].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes8[0].xaxis.set_major_locator(MultipleLocator(400))
axes8[0].xaxis.set_minor_locator(AutoMinorLocator(5))
axes8[0].set_ylim(0, 25)
axes8[0].yaxis.set_major_locator(MultipleLocator(5))
axes8[0].yaxis.set_minor_locator(AutoMinorLocator(5))
axes8[0].grid(which='major', color='#CCCCCC', linestyle='--')
axes8[0].grid(which='minor', color='#CCCCCC', linestyle=':')
axes8[0].set_title('Mean Position Error (ROI = 400 meters)')
axes8[0].set_xlabel('time (s)')
axes8[0].set_ylabel('mean of position errors (m)\ncollected per 0.5 sec intervals')
axes8[0].scatter(X1, Y1, s=0.5)
# Create figure 2
axes8[1].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes8[1].xaxis.set_major_locator(MultipleLocator(400))
axes8[1].xaxis.set_minor_locator(AutoMinorLocator(5))
axes8[1].set_ylim(0, 125)
axes8[1].yaxis.set_major_locator(MultipleLocator(25))
axes8[1].yaxis.set_minor_locator(AutoMinorLocator(5))
axes8[1].grid(which='major', color='#CCCCCC', linestyle='--')
axes8[1].grid(which='minor', color='#CCCCCC', linestyle=':')
axes8[1].set_title('Maximum Position Error (ROI = 400 meters)')
axes8[1].set_xlabel('time (s)')
axes8[1].set_ylabel('maximum of position errors (m)\ncollected per 0.5 sec intervals')
axes8[1].scatter(X2, Y2, s=0.5)
# Create figure 3
axes8[2].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes8[2].xaxis.set_major_locator(MultipleLocator(300))
axes8[2].xaxis.set_minor_locator(AutoMinorLocator(5))
axes8[2].set_ylim(0, 0.5)
axes8[2].yaxis.set_major_locator(MultipleLocator(0.1))
axes8[2].yaxis.set_minor_locator(AutoMinorLocator(5))
axes8[2].grid(which='major', color='#CCCCCC', linestyle='--')
axes8[2].grid(which='minor', color='#CCCCCC', linestyle=':')
axes8[2].set_title('Unknown Vehicle Ratio (ROI = 400 meters)')
axes8[2].set_xlabel('time (s)')
axes8[2].set_ylabel('ratio of unknown vehicles\ncollected per 0.5 sec intervals')
axes8[2].scatter(X3, Y3, s=0.5)

# Plot position errors for roi distance 500m
X1 = mapAveragePositionError_500.keys()
Y1 = mapAveragePositionError_500.values()
X2 = mapMaximumPositionError_500.keys()
Y2 = mapMaximumPositionError_500.values()
X3 = mapUnknownRatio_500.keys()
Y3 = mapUnknownRatio_500.values()
figure9, axes9 = plt.subplots(3, figsize=(8, 12))
figure9.tight_layout(pad=5.0)
# Create figure 1
axes9[0].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes9[0].xaxis.set_major_locator(MultipleLocator(500))
axes9[0].xaxis.set_minor_locator(AutoMinorLocator(5))
axes9[0].set_ylim(0, 25)
axes9[0].yaxis.set_major_locator(MultipleLocator(5))
axes9[0].yaxis.set_minor_locator(AutoMinorLocator(5))
axes9[0].grid(which='major', color='#CCCCCC', linestyle='--')
axes9[0].grid(which='minor', color='#CCCCCC', linestyle=':')
axes9[0].set_title('Mean Position Error (ROI = 500 meters)')
axes9[0].set_xlabel('time (s)')
axes9[0].set_ylabel('mean of position errors (m)\ncollected per 0.5 sec intervals')
axes9[0].scatter(X1, Y1, s=0.5)
# Create figure 2
axes9[1].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes9[1].xaxis.set_major_locator(MultipleLocator(500))
axes9[1].xaxis.set_minor_locator(AutoMinorLocator(5))
axes9[1].set_ylim(0, 125)
axes9[1].yaxis.set_major_locator(MultipleLocator(25))
axes9[1].yaxis.set_minor_locator(AutoMinorLocator(5))
axes9[1].grid(which='major', color='#CCCCCC', linestyle='--')
axes9[1].grid(which='minor', color='#CCCCCC', linestyle=':')
axes9[1].set_title('Maximum Position Error (ROI = 500 meters)')
axes9[1].set_xlabel('time (s)')
axes9[1].set_ylabel('maximum of position errors (m)\ncollected per 0.5 sec intervals')
axes9[1].scatter(X2, Y2, s=0.5)
# Create figure 3
axes9[2].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes9[2].xaxis.set_major_locator(MultipleLocator(300))
axes9[2].xaxis.set_minor_locator(AutoMinorLocator(5))
axes9[2].set_ylim(0, 0.5)
axes9[2].yaxis.set_major_locator(MultipleLocator(0.1))
axes9[2].yaxis.set_minor_locator(AutoMinorLocator(5))
axes9[2].grid(which='major', color='#CCCCCC', linestyle='--')
axes9[2].grid(which='minor', color='#CCCCCC', linestyle=':')
axes9[2].set_title('Unknown Vehicle Ratio (ROI = 500 meters)')
axes9[2].set_xlabel('time (s)')
axes9[2].set_ylabel('ratio of unknown vehicles\ncollected per 0.5 sec intervals')
axes9[2].scatter(X3, Y3, s=0.5)

# Plot position errors for roi distance 1000m
X1 = mapAveragePositionError_1000.keys()
Y1 = mapAveragePositionError_1000.values()
X2 = mapMaximumPositionError_1000.keys()
Y2 = mapMaximumPositionError_1000.values()
X3 = mapUnknownRatio_1000.keys()
Y3 = mapUnknownRatio_1000.values()
figure10, axes10 = plt.subplots(3, figsize=(8, 12))
figure10.tight_layout(pad=5.0)
# Create figure 1
axes10[0].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes10[0].xaxis.set_major_locator(MultipleLocator(1000))
axes10[0].xaxis.set_minor_locator(AutoMinorLocator(5))
axes10[0].set_ylim(0, 25)
axes10[0].yaxis.set_major_locator(MultipleLocator(5))
axes10[0].yaxis.set_minor_locator(AutoMinorLocator(5))
axes10[0].grid(which='major', color='#CCCCCC', linestyle='--')
axes10[0].grid(which='minor', color='#CCCCCC', linestyle=':')
axes10[0].set_title('Mean Position Error (ROI = 1000 meters)')
axes10[0].set_xlabel('time (s)')
axes10[0].set_ylabel('mean of position errors (m)\ncollected per 0.5 sec intervals')
axes10[0].scatter(X1, Y1, s=0.5)
# Create figure 2
axes10[1].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes10[1].xaxis.set_major_locator(MultipleLocator(1000))
axes10[1].xaxis.set_minor_locator(AutoMinorLocator(5))
axes10[1].set_ylim(0, 125)
axes10[1].yaxis.set_major_locator(MultipleLocator(25))
axes10[1].yaxis.set_minor_locator(AutoMinorLocator(5))
axes10[1].grid(which='major', color='#CCCCCC', linestyle='--')
axes10[1].grid(which='minor', color='#CCCCCC', linestyle=':')
axes10[1].set_title('Maximum Position Error (ROI = 1000 meters)')
axes10[1].set_xlabel('time (s)')
axes10[1].set_ylabel('maximum of position errors (m)\ncollected per 0.5 sec intervals')
axes10[1].scatter(X2, Y2, s=0.5)
# Create figure 3
axes10[2].set_xlim(PLOT_START_TIME, PLOT_END_TIME)
axes10[2].xaxis.set_major_locator(MultipleLocator(300))
axes10[2].xaxis.set_minor_locator(AutoMinorLocator(5))
axes10[2].set_ylim(0, 0.5)
axes10[2].yaxis.set_major_locator(MultipleLocator(0.1))
axes10[2].yaxis.set_minor_locator(AutoMinorLocator(5))
axes10[2].grid(which='major', color='#CCCCCC', linestyle='--')
axes10[2].grid(which='minor', color='#CCCCCC', linestyle=':')
axes10[2].set_title('Unknown Vehicle Ratio (ROI = 1000 meters)')
axes10[2].set_xlabel('time (s)')
axes10[2].set_ylabel('ratio of unknown vehicles\ncollected per 0.5 sec intervals')
axes10[2].scatter(X3, Y3, s=0.5)

# Show plotted figures
plt.show()