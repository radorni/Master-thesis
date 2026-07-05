import pandas as pd
import matplotlib.pyplot as plt


def plot_yplus(filepath):
    """
    Reads OpenFOAM yPlus.dat and plots the average and maximum y+ values.
    """
    # OpenFOAM yPlus data is usually tab/space separated.
    # Columns typically: Time, patchName, min, max, average
    times, yplus_avg, yplus_max = [], [], []

    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#'):
                continue

            cols = line.split()
            if len(cols) >= 5:
                times.append(float(cols[0]))
                # Assuming the structure is: Time Patch Min Max Average
                yplus_max.append(float(cols[3]))
                yplus_avg.append(float(cols[4]))

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(times, yplus_avg, label='Average y+', color='green', linewidth=2)
    plt.plot(times, yplus_max, label='Maximum y+', color='orange', linestyle='--')

    plt.xlabel('Simulation Time (s)')
    plt.ylabel('y+ Value')
    plt.title('y+ Evolution on Cylinder Surface')
    plt.axhline(y=1.0, color='red', linestyle=':', label='Viscous Sublayer Target (y+ = 1)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


file = '../postProcessing/yPlus/0.000000/yPlus.dat'

# Execution Example:
plot_yplus(file)
