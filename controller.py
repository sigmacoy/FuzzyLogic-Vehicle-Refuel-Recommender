from membership import triangular_membership, trapezoidal_membership

def run_fuzzy_controller(fuel, distance, verbose):
    if verbose:
        print(f"\nCrisp Inputs -> Fuel: {fuel}L, Distance: {distance}km")

    # 1. FUZZIFICATION
    # Fuel: 0 to 50 Liters. Edges use Trapezoidal to stay at 1.0 beyond peaks.
    fuel_low = trapezoidal_membership(fuel, 0.0, 0.0, 5.0, 15.0)    # 0-5L is critically low
    fuel_med = triangular_membership(fuel, 10.0, 25.0, 40.0)
    fuel_high = trapezoidal_membership(fuel, 30.0, 45.0, 50.0, 50.0) # >45L is perfectly full

    # Distance: Scaled to 250km (since 10L = 200km range)
    dist_near = trapezoidal_membership(distance, 0.0, 0.0, 20.0, 60.0)
    dist_med = triangular_membership(distance, 40.0, 100.0, 160.0)
    dist_far = trapezoidal_membership(distance, 120.0, 200.0, 250.0, 250.0)

    if verbose:
        print("\n--- Fuzzification Results ---")
        print(f"Fuel       [Low: {fuel_low:.2f}, Med: {fuel_med:.2f}, High: {fuel_high:.2f}]")
        print(f"Distance   [Near: {dist_near:.2f}, Med: {dist_med:.2f}, Far: {dist_far:.2f}]")

    # 2. RULE EVALUATION (Complete 9-Rule Matrix)
    # MANDATORY REFUEL CONDITIONS
    # Low fuel, or Medium fuel trying to cover a Far distance
    r1 = min(fuel_low, dist_near)
    r2 = min(fuel_low, dist_med)
    r3 = min(fuel_low, dist_far)
    r4 = min(fuel_med, dist_far) 
    strength_mandatory = max(r1, r2, r3, r4)

    # CONSIDER REFUEL CONDITIONS
    # Medium fuel/Medium distance, or High fuel/Far distance (just in case)
    r5 = min(fuel_med, dist_near)
    r6 = min(fuel_med, dist_med)
    r7 = min(fuel_high, dist_far)
    strength_consider = max(r5, r6, r7)

    # SKIP REFUEL CONDITIONS
    # High fuel (near/med dist)
    r8 = min(fuel_high, dist_near)
    r9 = min(fuel_high, dist_med)
    strength_skip = max(r8, r9)

    if verbose:
        print("\n--- Rule Firing Strengths ---")
        print(f"Mandatory Refuel: {strength_mandatory:.2f}")
        print(f"Consider Refuel:  {strength_consider:.2f}")
        print(f"Skip Refuel:      {strength_skip:.2f}")

    # 3. IMPLICATION, AGGREGATION & DEFUZZIFICATION (Centroid)
    sum_numerator = 0.0
    sum_denominator = 0.0
    step = 0.5  
    
    y = 0.0
    while y <= 100.0:
        # Output Urgency MFs (Edges are trapezoidal so 0% and 100% don't drop off)
        out_skip = trapezoidal_membership(y, 0.0, 0.0, 20.0, 50.0)
        out_consider = triangular_membership(y, 25.0, 50.0, 75.0)
        out_mandatory = trapezoidal_membership(y, 50.0, 80.0, 100.0, 100.0)

        # Implication (Clip)
        clipped_skip = min(strength_skip, out_skip)
        clipped_consider = min(strength_consider, out_consider)
        clipped_mandatory = min(strength_mandatory, out_mandatory)

        # Aggregation (Union)
        aggregated_y = max(clipped_skip, clipped_consider, clipped_mandatory)

        # Centroid accumulation
        sum_numerator += y * aggregated_y * step
        sum_denominator += aggregated_y * step
        
        y += step 

    crisp_output = 0.0
    if sum_denominator > 0.0:
        crisp_output = sum_numerator / sum_denominator

    if verbose:
        print("\n--- Mamdani Defuzzification Result ---")
        print(f"Calculated Crisp Urgency Output: {crisp_output:.2f}%")
    
    return crisp_output