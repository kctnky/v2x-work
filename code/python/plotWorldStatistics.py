import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

# Definitions
WORLD_STATISTICS_FILENAME = './../../data/camstat/world_statistics.csv'
PLOT_START_TIME = 0.0
PLOT_END_TIME = 1200.0
ROAD_LENGTH = 4250

# Define data arrays
simTime = []
simLambda = []
simVehicleCount = []
simVehicleMeanSpeed = []

# Read from world statistics file
line_number = 0
with open(WORLD_STATISTICS_FILENAME, 'r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        line_number += 1
        if line_number == 1:
            continue
        current_time = float(row[0])
        if current_time < PLOT_START_TIME or current_time > PLOT_END_TIME:
            continue
        simTime.append(current_time)
        simLambda.append(((current_time // 60) + 1) * 0.1 * 2)
        simVehicleCount.append(float(row[1]) / 4250 * 100)
        simVehicleMeanSpeed.append(float(row[2]) * 3600 / 1000)

# Create figure 1
figure1, axes1 = plt.subplots(figsize=(8, 6))
figure1.tight_layout(pad=5.0)
# Set axis ranges
axes1.set_xlim(0, PLOT_END_TIME)
axes1.set_ylim(0, 5.0)
# Change ticks
axes1.xaxis.set_major_locator(MultipleLocator(300))
axes1.yaxis.set_major_locator(MultipleLocator(1.0))
axes1.xaxis.set_minor_locator(AutoMinorLocator(5))
axes1.yaxis.set_minor_locator(AutoMinorLocator(5))
# Turn grid on
axes1.grid(which='major', color='#CCCCCC', linestyle='--')
axes1.grid(which='minor', color='#CCCCCC', linestyle=':')
# Plot line graph
axes1.set_title('Vehicle Summon Rate')
axes1.set_xlabel('time (s)')
axes1.set_ylabel('# vehicles per second')
axes1.plot(simTime, simLambda)

# Create figure 2
figure2, axes2 = plt.subplots(figsize=(8, 6))
figure2.tight_layout(pad=5.0)
# Set axis ranges
axes2.set_xlim(0, PLOT_END_TIME)
axes2.set_ylim(0, 10.0)
# Change ticks
axes2.xaxis.set_major_locator(MultipleLocator(300))
axes2.yaxis.set_major_locator(MultipleLocator(2.0))
axes2.xaxis.set_minor_locator(AutoMinorLocator(5))
axes2.yaxis.set_minor_locator(AutoMinorLocator(5))
# Turn grid on
axes2.grid(which='major', color='#CCCCCC', linestyle='--')
axes2.grid(which='minor', color='#CCCCCC', linestyle=':')
# Plot scatter graph
axes2.set_title('Vehicle Density')
axes2.set_xlabel('time (s)')
axes2.set_ylabel('# vehicles per 100 meters')
axes2.scatter(simTime, simVehicleCount, s=0.5)

# Create figure 3
figure3, axes3 = plt.subplots(figsize=(8, 6))
figure3.tight_layout(pad=5.0)
# Set axis ranges
axes3.set_xlim(0, PLOT_END_TIME)
axes3.set_ylim(0, 180)
# Change ticks
axes3.xaxis.set_major_locator(MultipleLocator(300))
axes3.yaxis.set_major_locator(MultipleLocator(30))
axes3.xaxis.set_minor_locator(AutoMinorLocator(5))
axes3.yaxis.set_minor_locator(AutoMinorLocator(5))
# Turn grid on
axes3.grid(which='major', color='#CCCCCC', linestyle='--')
axes3.grid(which='minor', color='#CCCCCC', linestyle=':')
# Plot scatter graph
axes3.set_title('Mean Speed')
axes3.set_xlabel('time (s)')
axes3.set_ylabel('kilometers per hour (kmph)')
axes3.scatter(simTime, simVehicleMeanSpeed, s=0.5)

# Create all in one figure
figure4, axes4 = plt.subplots(3, figsize=(8, 12))
figure4.tight_layout(pad=5.0)
# Create Figure 1
axes4[0].set_xlim(0, PLOT_END_TIME)
axes4[0].set_ylim(0, 5.0)
axes4[0].xaxis.set_major_locator(MultipleLocator(300))
axes4[0].yaxis.set_major_locator(MultipleLocator(1.0))
axes4[0].xaxis.set_minor_locator(AutoMinorLocator(5))
axes4[0].yaxis.set_minor_locator(AutoMinorLocator(5))
axes4[0].grid(which='major', color='#CCCCCC', linestyle='--')
axes4[0].grid(which='minor', color='#CCCCCC', linestyle=':')
axes4[0].set_title('Vehicle Summon Rate')
axes4[0].set_xlabel('time (s)')
axes4[0].set_ylabel('# vehicles per second')
axes4[0].plot(simTime, simLambda)
# Create Figure 2
axes4[1].set_xlim(0, PLOT_END_TIME)
axes4[1].set_ylim(0, 10.0)
axes4[1].xaxis.set_major_locator(MultipleLocator(300))
axes4[1].yaxis.set_major_locator(MultipleLocator(2.0))
axes4[1].xaxis.set_minor_locator(AutoMinorLocator(5))
axes4[1].yaxis.set_minor_locator(AutoMinorLocator(5))
axes4[1].grid(which='major', color='#CCCCCC', linestyle='--')
axes4[1].grid(which='minor', color='#CCCCCC', linestyle=':')
axes4[1].set_title('Vehicle Density')
axes4[1].set_xlabel('time (s)')
axes4[1].set_ylabel('# vehicles per 100 meters')
axes4[1].scatter(simTime, simVehicleCount, s=0.5)
# Create Figure 3
axes4[2].set_xlim(0, PLOT_END_TIME)
axes4[2].set_ylim(0, 180)
axes4[2].xaxis.set_major_locator(MultipleLocator(300))
axes4[2].yaxis.set_major_locator(MultipleLocator(30))
axes4[2].xaxis.set_minor_locator(AutoMinorLocator(5))
axes4[2].yaxis.set_minor_locator(AutoMinorLocator(5))
axes4[2].grid(which='major', color='#CCCCCC', linestyle='--')
axes4[2].grid(which='minor', color='#CCCCCC', linestyle=':')
axes4[2].set_title('Mean Speed')
axes4[2].set_xlabel('time (s)')
axes4[2].set_ylabel('kilometers per hour (kmph)')
axes4[2].scatter(simTime, simVehicleMeanSpeed, s=0.5)

# Show plotted figures
plt.show()
