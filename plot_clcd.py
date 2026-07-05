import numpy as np
import matplotlib.pyplot as plt


def plot_force_coefficients(filepath, rho, U_inf, D):
    """
    Reads OpenFOAM force.dat and plots Drag and Lift coefficients.
    Assumes incompressible flow where forces might need density multiplication
    depending on the OpenFOAM version and setup.
    """
    times, cd_list, cl_list = [], [], []

    # Reference area
    A_ref = D * 3.14

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

            time = float(cols[0])

            # Total Drag force (x) and Lift force (y)
            Fx_total = float(cols[1])
            Fy_total = float(cols[2])

            # Calculate coefficients
            Cd = Fx_total / (q * A_ref)
            Cl = Fy_total / (q * A_ref)

            times.append(time)
            cd_list.append(Cd)
            cl_list.append(Cl)

    # Plotting
    fig, ax = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    ax[0].plot(times, cd_list, label='Drag Coefficient (Cd)', color='blue')
    ax[0].set_ylabel('Cd')
    ax[0].grid(True)
    ax[0].legend()

    ax[1].plot(times, cl_list, label='Lift Coefficient (Cl)', color='red')
    ax[1].set_ylabel('Cl')
    ax[1].set_xlabel('Simulation Time (s)')
    ax[1].grid(True)
    ax[1].legend()

    plt.suptitle('Aerodynamic Force Coefficients over Time')
    plt.tight_layout()
    plt.show()

file = '../postProcessing/forces_on_cylinder/0.000000/force.dat'
# Execution Example:
plot_force_coefficients(file, rho=1.225, U_inf=0.0779, D=1.0)