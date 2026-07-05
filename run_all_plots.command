#!/bin/bash
# Move to the directory where this clickable script sits
cd "$(dirname "$0")"

# Define your Anaconda Python interpreter variable to keep the code clean
PYTHON_BIN="/Users/rocco/anaconda3/envs/pythonProject/bin/python"

echo "=== Plot 1 of 4: Force Coefficients (Cl & Cd) ==="
$PYTHON_BIN plot_clcd.py
echo "Plot closed. Press Enter to launch CPU Time..."
read

echo "=== Plot 2 of 4: Computational Cost ==="
$PYTHON_BIN plot_cputime_RANS.py
echo "Plot closed. Press Enter to launch Residuals..."
read

echo "=== Plot 3 of 4: Convergence Residuals ==="
$PYTHON_BIN plot_residuals_RANS.py
echo "Plot closed. Press Enter to launch Y-Plus..."
read

echo "=== Plot 4 of 4: Y-Plus Evolution ==="
$PYTHON_BIN plot_yplus.py
echo "All plotting complete! Press Enter to close this window."
read