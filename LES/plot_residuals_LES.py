import matplotlib.pyplot as plt
import re
import sys


def plot_residuals(log_file, U_inf, D):
    """
    Parses OpenFOAM log for initial residuals and plots them against
    non-dimensional simulation time (t*). Safely handles pimpleFoam outer loops.
    """
    # Dictionary mapping fields to their specific t* and residual values
    field_data = {}

    time_pattern = re.compile(r'^Time = ([\d\.eE\+\-]+)')
    res_pattern = re.compile(r'Solving for ([a-zA-Z0-9_]+), Initial residual = ([\d\.eE\+\-]+)')

    seen_fields_this_step = set()
    current_tstar = None

    print("Parsing log file for residuals...")

    try:
        with open(log_file, 'r') as f:
            for line in f:
                # Check if the line is a new time step
                time_match = time_pattern.match(line)
                if time_match:
                    physical_time = float(time_match.group(1))
                    # Convert to non-dimensional time
                    current_tstar = physical_time * (U_inf / D)
                    seen_fields_this_step.clear()  # Reset for the new time step

                # Check if the line contains a residual calculation
                res_match = res_pattern.search(line)
                if res_match and current_tstar is not None:
                    field = res_match.group(1)
                    val = float(res_match.group(2))

                    # pimpleFoam solves fields multiple times per step.
                    # We only want to plot the FIRST initial residual of the step.
                    if field not in seen_fields_this_step:
                        if field not in field_data:
                            field_data[field] = {'t': [], 'res': []}

                        # [FIXED]: Appending the time is now properly active
                        field_data[field]['t'].append(current_tstar)
                        field_data[field]['res'].append(val)

                        seen_fields_this_step.add(field)

    except FileNotFoundError:
        print(f"Error: Could not find '{log_file}'. Make sure you are in the case directory.")
        sys.exit()

    # Plotting
    plt.figure(figsize=(10, 6))

    # Target fields updated to include Uz for 3D LES
    target_fields = ['Ux', 'Uy', 'Uz', 'p']

    for field in target_fields:
        if field in field_data and len(field_data[field]['t']) > 0:
            plt.plot(field_data[field]['t'], field_data[field]['res'],
                     label=f'{field} (Initial)', linewidth=1.0, alpha=0.8)

    # Format the plot for logarithmic convergence viewing
    plt.yscale('log')
    plt.xlabel('Non-dimensional time (t*)')
    plt.ylabel('Initial Residual')
    plt.title('LES Transient Convergence History')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()

    plt.tight_layout()
    plt.show()

log_file = '../log'

# Execution Example:
# Replace U_inf and D with your actual values from the constants file
plot_residuals(log_file, U_inf=0.0779, D=1.0)