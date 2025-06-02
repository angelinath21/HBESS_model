import numpy as np
from batteryModel import Battery
from loadProfile import generate_community_load_profile

def check_battery_capacity(battery, load_kw, dt=900):
    """
    battery: Battery instance
    load_kw: numpy array of power demand in kW (positive means power draw)
    dt: timestep duration in seconds (default 15 minutes = 900s)
    
    Returns:
        can_supply: bool, True if battery SOC never drops to zero during load
        soc_history: list of SOC values over time
    """
    soc_history = []
    for power in load_kw:
        # Battery discharge: power < 0 means discharging, so invert load sign
        # Here load_kw is positive (load demand), so battery power is negative of that
        voltage, current = battery.charge(-power, dt)
        soc_history.append(battery.soc)
        if battery.soc <= 0:
            return False, soc_history
    return True, soc_history

if __name__ == "__main__":
    # Generate load profile for community
    load_kw, time_vec = generate_community_load_profile()

    # Initialize battery with 100 kWh capacity, 48 V nominal, starting fully charged
    batt = Battery(capacity_kWh=100, voltage=48, soc_init=1.0)

    can_supply, soc_history = check_battery_capacity(batt, load_kw)

    print(f"Battery can supply entire load: {can_supply}")
    print(f"Final SOC: {batt.soc:.3f}")
