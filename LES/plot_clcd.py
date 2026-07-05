import numpy as np
import matplotlib.pyplot as plt


def plot_force_coefficients(filepath, rho, U_inf, D, span):
    """
    Reads OpenFOAM force.dat, calculates non-dimensional time (t*),
    and plots Drag and Lift coefficients.
    """
    t_star_list, cd_list, cl_list = [], [], []

    # Reference area for a 3D cylinder (Diameter * Span)
    A_ref = D * span

    # Dynamic pressure
    q = 0.5 * rho * (U_inf ** 2)

    with open(filepath, 'r') as f:
        for line in f:
            # Skip header lines
            if line.startswith('#'):
                continue

            # Remove parentheses and split into columns
            clean_line = line.replace('(', '').replace(')', '')
            cols = clean_line.split()

            if not cols:
                continue

            # 1. Extract physical time
            physical_time = float(cols[0])

            # 2. Convert to Non-Dimensional Time (t*)
            t_star = physical_time * (U_inf / D)

            # Total Drag force (x) and Lift force (y)
            Fx_total = float(cols[1])
            Fy_total = float(cols[2])

            # Calculate coefficients
            Cd = Fx_total / (q * A_ref)
            Cl = Fy_total / (q * A_ref)

            # Append to lists
            t_star_list.append(t_star)
            cd_list.append(Cd)
            cl_list.append(Cl)

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax[0].plot(t_star_list, cd_list, label='Drag Coefficient (Cd)', color='blue', linewidth=1.2)
    ax[0].set_ylabel('Cd')
    ax[0].grid(True, linestyle='--', alpha=0.6)
    ax[0].legend()

    ax[1].plot(t_star_list, cl_list, label='Lift Coefficient (Cl)', color='red', linewidth=1.2)
    ax[1].set_ylabel('Cl')
    ax[1].set_xlabel('Non-dimensional time (t*)')  # Updated X-axis
    ax[1].grid(True, linestyle='--', alpha=0.6)
    ax[1].legend()

    plt.tight_layout()
    plt.show()


file = '../postProcessing/forces_on_cylinder/0.000000/force.dat'

# Execution Example
plot_force_coefficients(file, rho=1.225, U_inf=0.0779, D=1.0, span=3.14)