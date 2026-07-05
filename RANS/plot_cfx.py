import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def plot_cfx_ccw(csv_filepath, U_inf=0.0779, target_z=0.0):
    df = pd.read_csv(csv_filepath)

    # 1. Filter data
    closest_z = df.iloc[(df['Points:2'] - target_z).abs().argsort()[:1]]['Points:2'].values[0]
    slice_df = df[np.isclose(df['Points:2'], closest_z, atol=1e-4)].copy()

    # 2. Calculate CCW Angle (0 at Front)
    raw_angle = np.degrees(np.arctan2(slice_df['Points:1'], slice_df['Points:0']))
    slice_df['theta'] = (raw_angle - 180) % 360
    slice_df = slice_df.sort_values(by='theta')

    # 3. Calculate Cfx
    q = 0.5 * U_inf ** 2
    slice_df['cfx'] = slice_df['wallShearStressMean:0'] / q

    # 4. Plotting
    plt.figure(figsize=(10, 6))

    # Add a horizontal line at 0 to easily spot separation points
    plt.axhline(0, color='black', linewidth=1, linestyle='--')

    plt.plot(slice_df['theta'], slice_df['cfx'], 'b-', linewidth=2.5, label=f'Cfx at Z ≈ {closest_z:.2f}')

    plt.xlabel('Angle θ (degrees) [0°=Front, 90°=Bottom, 180°=Rear, 270°=Top]', fontsize=11)
    plt.ylabel('Skin Friction Coefficient ($C_{f,x}$)', fontsize=12)
    plt.title('Time-Averaged $C_{f,x}$ Distribution (CCW)', fontsize=14)

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xlim(0, 360)
    plt.xticks(np.arange(0, 361, 45))

    plt.legend()
    plt.tight_layout()
    plt.show()


file = '../Paraview/cfx.csv'

# Run the function
plot_cfx_ccw(file, U_inf=0.0779, target_z=0.0)
