import numpy as np

def calculate_received_power(initial_power_mw: float, extinction_coef: float, distance_km: float) -> float:
    """
    Calculates the optical power received after atmospheric attenuation using Beer-Lambert's Law.
    
    Parameters:
        initial_power_mw (float): Transmitted optical power in milliwatts (mW).
        extinction_coef (float): Atmospheric extinction coefficient alpha (1/km).
        distance_km (float): Propagation path length / Line of Sight (km).
        
    Returns:
        float: Received optical power at the detector in milliwatts (mW).
    """
    return initial_power_mw * np.exp(-extinction_coef * distance_km)

if __name__ == "__main__":
    # Test Simulation Scenario:
    # 1550 nm optical transmission over a 5 km link under moderate fog (alpha = 0.8 / km)
    p_tx = 100.0  # Transmitted power (mW)
    alpha = 0.8   # Extinction coefficient
    d = 5.0       # Link distance (km)
    
    p_rx = calculate_received_power(p_tx, alpha, d)
    print(f"[OOM Simulation] Transmitted Power: {p_tx} mW")
    print(f"[OOM Simulation] Distance: {d} km (alpha = {alpha})")
    print(f"[OOM Simulation] Received Power at Diode: {p_rx:.4f} mW")
