import matplotlib.pyplot as plt
import re
import sys

# 1. Define the log file name
log_file = '../log'

# 2. Set up dictionaries to hold our data
# We track 'Time' for the X-axis, and store lists of residuals for the Y-axis
times = []
residuals = {}

# 3. Define the Regular Expressions to hunt for text patterns
# We are looking for lines like: "Time = 0.01"
time_pattern = re.compile(r'^Time = ([\d\.eE\+\-]+)')
# We are looking for lines like: "Solving for Ux, Initial residual = 0.012, Final..."
res_pattern = re.compile(r'Solving for ([a-zA-Z0-9_]+), Initial residual = ([\d\.eE\+\-]+)')

# Helper variable to only grab the *first* residual of the PIMPLE loop per timestep
seen_fields_this_step = set()

print("Parsing log file...")

# 4. Read the file line by line
try:
    with open(log_file, 'r') as f:
        for line in f:
            # Check if the line is a new time step
            time_match = time_pattern.match(line)
            if time_match:
                current_time = float(time_match.group(1))
                times.append(current_time)
                seen_fields_this_step.clear()  # Reset for the new time step

            # Check if the line contains a residual calculation
            res_match = res_pattern.search(line)
            if res_match and len(times) > 0:
                field = res_match.group(1)
                val = float(res_match.group(2))

                # pimpleFoam solves fields multiple times per step.
                # We only want to plot the FIRST initial residual of the step.
                if field not in seen_fields_this_step:
                    if field not in residuals:
                        residuals[field] = []
                    residuals[field].append(val)
                    seen_fields_this_step.add(field)
except FileNotFoundError:
    print(f"Error: Could not find '{log_file}'. Make sure you are in the case directory.")
    sys.exit()

# 5. Plot the data
plt.figure(figsize=(10, 6))

# Only plot the major fields to avoid clutter (Velocity and Pressure)
target_fields = ['Ux', 'Uy', 'p']

for field in target_fields:
    if field in residuals:
        # Ensure x and y arrays are the same length before plotting
        y_data = residuals[field]
        x_data = times[:len(y_data)]
        plt.plot(x_data, y_data, label=f'{field} (Initial)')

# Format the plot for logarithmic convergence viewing
plt.yscale('log')
plt.xlabel('Simulation Time (s)')
plt.ylabel('Initial Residual')
plt.title('Convergence History')
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.legend()

print("Opening plot...")
plt.show()