import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_cp_ccw(csv_filepath, target_z=0.0):
    df = pd.read_csv(csv_filepath)

    # 1. Filter data for the specific Z-height
    closest_z = df.iloc[(df['Points:2'] - target_z).abs().argsort()[:1]]['Points:2'].values[0]
    slice_df = df[np.isclose(df['Points:2'], closest_z, atol=1e-4)].copy()

    # 2. Calculate CCW Angle (0 at Front)
    # arctan2(Y, X) gives standard angles from the origin.
    # Subtracting 180 shifts 0 to the front, and % 360 forces a positive 0-360 CCW sweep.
    raw_angle = np.degrees(np.arctan2(slice_df['Points:1'], slice_df['Points:0']))
    slice_df['theta'] = (raw_angle - 180) % 360

    # Sort by the new angle so the line plots smoothly
    slice_df = slice_df.sort_values(by='theta')

    # 3. Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(slice_df['theta'], slice_df['cp'], 'r-', linewidth=2.5, label=f'Cp at Z ≈ {closest_z:.2f}')

    plt.xlabel('Angle θ (degrees) [0°=Front, 90°=Bottom, 180°=Rear, 270°=Top]', fontsize=11)
    plt.ylabel('Pressure Coefficient ($C_p$)', fontsize=12)
    plt.title('Time-Averaged $C_p$ Distribution (CCW)', fontsize=14)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, 360)
    plt.xticks(np.arange(0, 361, 45))

    # Invert Y-axis for standard aerodynamic pressure plotting
    # plt.gca().invert_yaxis()

    plt.legend()
    plt.tight_layout()
    plt.show()

file = '../Paraview/cp.csv'

# Run the function
plot_cp_ccw(file, target_z=0.0)