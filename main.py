import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from membership import triangular_membership, trapezoidal_membership
from controller import run_fuzzy_controller

def plot_membership_functions():
    """Requirement 1: 2D Plots of Input/Output MFs"""
    fuel_x = np.linspace(0, 50, 100)
    dist_x = np.linspace(0, 250, 100)
    out_x = np.linspace(0, 100, 100)

    plt.figure(figsize=(15, 4))

    # Input 1: Fuel
    plt.subplot(1, 3, 1)
    plt.plot(fuel_x, [trapezoidal_membership(x, 0, 0, 5, 15) for x in fuel_x], label='Low')
    plt.plot(fuel_x, [triangular_membership(x, 10, 25, 40) for x in fuel_x], label='Med')
    plt.plot(fuel_x, [trapezoidal_membership(x, 30, 45, 50, 50) for x in fuel_x], label='High')
    plt.title('Input 1: Fuel Level (Liters)')
    plt.legend()

    # Input 2: Distance
    plt.subplot(1, 3, 2)
    plt.plot(dist_x, [trapezoidal_membership(x, 0, 0, 20, 60) for x in dist_x], label='Near')
    plt.plot(dist_x, [triangular_membership(x, 40, 100, 160) for x in dist_x], label='Med')
    plt.plot(dist_x, [trapezoidal_membership(x, 120, 200, 250, 250) for x in dist_x], label='Far')
    plt.title('Input 2: Distance (km)')
    plt.legend()

    # Output: Urgency
    plt.subplot(1, 3, 3)
    plt.plot(out_x, [trapezoidal_membership(x, 0, 0, 20, 50) for x in out_x], label='Skip')
    plt.plot(out_x, [triangular_membership(x, 25, 50, 75) for x in out_x], label='Consider')
    plt.plot(out_x, [trapezoidal_membership(x, 50, 80, 100, 100) for x in out_x], label='Mandatory')
    plt.title('Output: Refuel Urgency (%)')
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_control_surface():
    """Requirement 2: 3D Control Surface"""
    # Create a 50x50 grid for calculation
    fuel_vals = np.linspace(0, 50, 50)
    dist_vals = np.linspace(0, 250, 50)
    F, D = np.meshgrid(fuel_vals, dist_vals)
    Z = np.zeros_like(F)

    # Calculate Z for each point in the grid
    # (Ensure your run_fuzzy_controller suppresses prints here)
    for i in range(F.shape[0]):
        for j in range(F.shape[1]):
            Z[i, j] = run_fuzzy_controller(F[i, j], D[i, j], verbose=False)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(F, D, Z, cmap=cm.viridis, edgecolor='none')
    
    ax.set_xlabel('Fuel Level (Liters)')
    ax.set_ylabel('Distance (km)')
    ax.set_zlabel('Refuel Urgency (%)')
    ax.set_title('Mamdani Control Surface: Refuel Recommender')
    fig.colorbar(surf, shrink=0.5, aspect=5)
    
    plt.show()

def main():
    print("=== Refuel Urgency Mamdani Fuzzy Logic Controller ===")

    # Define crisp inputs
    fuel = 10.0      # Fuel tank (by liters)
    # Vehicle consumes 1 L per 20 km
    distance = 65.0  # Distance to next gas station (km)
    
    # Pass variables to the controller
    # crisp_output = run_fuzzy_controller(fuel, distance)
    
    # Passing verbose=True for the live terminal demo
    crisp_output = run_fuzzy_controller(fuel, distance, verbose=True)
    
    # Map final crisp percentage back to human-readable decision
    if crisp_output >= 65:
        decision = "Mandatory Refuel!"
    elif crisp_output >= 35:
        decision = "Consider Refueling Soon."
    else:
        decision = "Skip, you have plenty."
        
    print(f"Final Decision: {decision}\n")
        
    print("Generating 2D Membership Function Plots...")
    plot_membership_functions()
    
    print("Generating 3D Control Surface... (This takes a few seconds)")
    plot_control_surface()

if __name__ == "__main__":
    main()