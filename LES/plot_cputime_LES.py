import matplotlib.pyplot as plt
import re
import sys

def plot_cputime(log_file, U_inf, D):
    """
    Parses OpenFOAM log for CPU execution time and plots it against
    non-dimensional simulation time (t*).
    """
    sim_times_tstar = []
    cumulative_exec_times = []

    time_pattern = re.compile(r'^Time = ([\d\.eE\+\-]+)')
    exec_pattern = re.compile(r'^ExecutionTime = ([\d\.eE\+\-]+) s')

    current_tstar = None

    print("Parsing log file for computational time...")

    try:
        with open(log_file, 'r') as f:
            for line in f:
                # Catch the current simulation time
                time_match = time_pattern.match(line)
                if time_match:
                    physical_time = float(time_match.group(1))
                    # Convert to non-dimensional time
                    current_tstar = physical_time * (U_inf / D)

                # Catch the execution time at the end of that step
                exec_match = exec_pattern.search(line)
                if exec_match and current_tstar is not None:
                    exec_time = float(exec_match.group(1))

                    sim_times_tstar.append(current_tstar)
                    cumulative_exec_times.append(exec_time)

                    # Reset current_time so we don't double-count
                    current_tstar = None
    except FileNotFoundError:
        print(f"Error: Could not find '{log_file}'. Make sure you are in the case directory.")
        sys.exit()

    if len(sim_times_tstar) == 0:
        print("No execution time data found yet. The solver might still be on the first step!")
        sys.exit()

    # Calculate how long each individual step took
    step_times = [cumulative_exec_times[0]]
    for i in range(1, len(cumulative_exec_times)):
        step_duration = cumulative_exec_times[i] - cumulative_exec_times[i - 1]
        step_times.append(step_duration)

    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Top Plot: Total Cumulative Time
    ax1.plot(sim_times_tstar, cumulative_exec_times, 'b-', linewidth=2, label='Total CPU Time')
    ax1.set_ylabel('Cumulative Execution Time (s)')
    ax1.set_title('LES Computational Cost Tracking')
    ax1.grid(True, linestyle='--', alpha=0.7)
    ax1.legend()

    # Bottom Plot: Time taken per step
    ax2.plot(sim_times_tstar, step_times, 'r-', linewidth=1.5, label='Time per Step')
    ax2.set_xlabel('Non-dimensional time (t*)')
    ax2.set_ylabel('Step Duration (s)')
    ax2.grid(True, linestyle='--', alpha=0.7)
    ax2.legend()

    plt.tight_layout()
    plt.show()

log_file = '../log'

# Execution Example:
plot_cputime(log_file, U_inf=0.0779, D=1.0)