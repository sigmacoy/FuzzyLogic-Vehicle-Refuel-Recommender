from membership import triangular_membership

def run_fuzzy_controller(fuel_level, distance):
    """Runs the Mamdani logic steps and prints intermediate results."""
    print(f"\nCrisp Inputs -> Fuel Level: {fuel_level}%, Distance: {distance}km")

    # 1. FUZZIFICATION (Input Memberships)
    fuel_low = triangular_membership(fuel_level, 0, 0, 50)
    fuel_med = triangular_membership(fuel_level, 20, 50, 80)
    fuel_high = triangular_membership(fuel_level, 50, 100, 100)

    dist_near = triangular_membership(distance, 0, 0, 50)
    dist_med = triangular_membership(distance, 20, 50, 80)
    dist_far = triangular_membership(distance, 50, 100, 100)

    print("\n--- Fuzzification Results ---")
    print(f"Fuel Level [Low: {fuel_low:.2f}, Med: {fuel_med:.2f}, High: {fuel_high:.2f}]")
    print(f"Distance   [Near: {dist_near:.2f}, Med: {dist_med:.2f}, Far: {dist_far:.2f}]")

    # 2. RULE EVALUATION (Firing Strengths)
    # Rule 1: IF Fuel is Low OR Distance is Far, THEN Urgency is Mandatory Refuel
    # Rule 2: IF Fuel is Medium AND Distance is Medium, THEN Urgency is Consider
    # Rule 3: IF Fuel is High, THEN Urgency is Skip
    
    rule1_strength = max(fuel_low, dist_far)  # OR means Max
    rule2_strength = min(fuel_med, dist_med)  # AND means Min
    rule3_strength = fuel_high                # Direct assignment

    print("\n--- Rule Firing Strengths ---")
    print(f"Rule 1 (Mandatory Refuel): {rule1_strength:.2f}")
    print(f"Rule 2 (Consider Refuel):  {rule2_strength:.2f}")
    print(f"Rule 3 (Skip Refuel):      {rule3_strength:.2f}")

    # 3. IMPLICATION, AGGREGATION & DEFUZZIFICATION (Center of Gravity)
    sum_numerator = 0.0
    sum_denominator = 0.0
    step = 0.5  
    
    y = 0.0
    while y <= 100.0:
        # Define output membership functions for Urgency
        out_skip = triangular_membership(y, 0.0, 0.0, 50.0)
        out_consider = triangular_membership(y, 20.0, 50.0, 80.0)
        out_mandatory = triangular_membership(y, 50.0, 100.0, 100.0)

        # Implication: Clip using Min
        clipped_skip = min(rule3_strength, out_skip)
        clipped_consider = min(rule2_strength, out_consider)
        clipped_mandatory = min(rule1_strength, out_mandatory)

        # Aggregation: Combine using Max
        aggregated_y = max(clipped_skip, clipped_consider, clipped_mandatory)

        # Accumulate for Centroid calculation
        sum_numerator += y * aggregated_y * step
        sum_denominator += aggregated_y * step
        
        y += step 

    crisp_output = 0.0
    if sum_denominator > 0.0:
        crisp_output = sum_numerator / sum_denominator

    print("\n--- Mamdani Defuzzification Result (Centroid) ---")
    print(f"Calculated Crisp Urgency Output: {crisp_output:.2f}%")
    
    return crisp_output