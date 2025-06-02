f_nom = 50.0        # Nominal frequency in Hz
P_nom = 2000.0      # Max supercap power (W)
k_f = 500.0         # Droop constant (W/Hz)

def droop_control(f_measured, f_nom=50.0, P_nom=2000.0, k_f=500.0):
    """
    Simple droop control function for power-sharing.
    
    Args:
        f_measured (float): Measured frequency (Hz)
        f_nom (float): Nominal frequency (default 50 Hz)
        P_nom (float): Nominal power output (W)
        k_f (float): Droop coefficient (W/Hz)

    Returns:
        float: Power output in Watts
    """
    delta_f = f_measured - f_nom
    P_output = P_nom - k_f * delta_f
    return max(0, min(P_output, P_nom))
