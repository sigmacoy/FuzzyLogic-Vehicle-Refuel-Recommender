from controller import run_fuzzy_controller

def main():
    print("=== Refuel Urgency Mamdani Fuzzy Logic Controller ===")

    # Define crisp inputs
    fuel = 10.0      # Fuel tank (by liters)
    # this vehicle uses 20 km/L
    distance = 65.0  # Distance to next gas station (km)
    
    # Pass variables to the controller
    crisp_output = run_fuzzy_controller(fuel, distance)
    
    # Map final crisp percentage back to human-readable decision
    if crisp_output >= 65:
        decision = "Mandatory Refuel!"
    elif crisp_output >= 35:
        decision = "Consider Refueling Soon."
    else:
        decision = "Skip, you have plenty."
        
    print(f"Final Decision: {decision}\n")

if __name__ == "__main__":
    main()