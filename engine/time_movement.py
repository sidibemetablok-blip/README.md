"""
LocalTrace-Nav: Time-Movement Engine
Calculates human-scale duration based on terrain friction and local movement vectors.
"""

def calculate_lived_duration(base_distance_km, terrain_friction_coefficient, physical_effort_factor):
    """
    Transforms flat geometric distance into physical, lived time-movement.
    
    Parameters:
    - base_distance_km (float): Standard geographic distance.
    - terrain_friction_coefficient (float): Resistance or density of the local environment (e.g., urban path vs rough trail).
    - physical_effort_factor (float): Human pacing coefficient.
    
    Returns:
    - float: Lived duration in minutes.
    """
    # Standard walking/movement base rate (approx 5 km/h -> 12 mins per km)
    base_time_per_km = 12.0 
    
    lived_duration = base_distance_km * base_time_per_km * terrain_friction_coefficient * physical_effort_factor
    return round(lived_duration, 2)

if __name__ == "__main__":
    # Example calculation for a local route
    distance = 2.5 # km
    friction = 1.3 # dense urban or uneven worksite terrain
    effort = 1.0   # steady pacing
    
    duration = calculate_lived_duration(distance, friction, effort)
    print(f"Route Distance: {distance} km")
    print(f"Calculated Lived Duration: {duration} minutes (Ground-adjusted)")
