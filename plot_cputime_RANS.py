import matplotlib.pyplot as plt
import re
import sys

# 1. Define the log file name
log_file = '../log'

# 2. Set up lists to hold our data
sim_times = []
cumulative_exec_times = []

# 3. Define the Regular Expressions
# We look for the simulation time
time_pattern = re.compile(r'^Time = ([\d\.eE\+\-]+)')
# We look for the line where OpenFOAM reports the CPU time
exec_pattern = re.compile(r'^ExecutionTime = ([\d\.eE\+\-]+) s')

current_time = None

print("Parsing log file for computational time...")

# 4. Read the file
try:
    with open(log_file, 'r') as f:
        for line in f:
            # Catch the current simulation time
            time_match = time_pattern.match(line)
            if time_match:
                current_time = float(time_match.group(1))

            # Catch the execution time at the end of that step
            exec_match = exec_pattern.search(line)
            if exec_match and current_time is not None:
                exec_time = float(exec_match.group(1))

                sim_times.append(current_time)
                cumulative_exec_times.append(exec_time)

                # Reset current_time so we don't double-count
                current_time = None
except FileNotFoundError:
    print(f"Error: Could not find '{log_file}'. Make sure you are in the case directory.")
    sys.exit()

if len(sim_times) == 0:
    print("No execution time data found yet. The solver might still be on the first step!")
    sys.exit()

# 5. Calculate how long each individual step took
step_times = [cumulative_exec_times[0]]
for i in range(1, len(cumulative_exec_times)):
    step_duration = cumulative_exec_times[i] - cumulative_exec_times[i - 1]
    step_times.append(step_duration)

# 6. Plot the data
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# Top Plot: Total Cumulative Time
ax1.plot(sim_times, cumulative_exec_times, 'b-', linewidth=2, label='Total CPU Time')
ax1.set_ylabel('Cumulative Execution Time (s)')
ax1.set_title('Computational Cost')
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.legend()

# Bottom Plot: Time taken per step
ax2.plot(sim_times, step_times, 'r-', linewidth=1.5, label='CPU Time per Step')
ax2.set_xlabel('Simulation Time (s)')
ax2.set_ylabel('Step Calculation Time (s)')
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.legend()

plt.tight_layout()
print("Opening plot...")
plt.show()