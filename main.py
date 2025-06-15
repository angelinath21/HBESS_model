from loadProfile import generate_community_load_profile
from plotUtils import plot_load_profile, plot_hess_results, plot_load_fft, plot_performance_degradation, plot_cycle_life
from batteryModel import Battery
from supercapModel import Supercapacitor
from emsController import EMSController
import matplotlib.pyplot as plt

def degrade_battery(battery, energy_discharged_kWh, degradation_rate=0.0001):
    """
    Simple degradation model:
    - battery: Battery instance
    - energy_discharged_kWh: energy removed this step in kWh (positive value)
    - degradation_rate: fraction capacity lost per kWh throughput (example)
    """
    if not hasattr(battery, 'cycle_energy_throughput'):
        battery.cycle_energy_throughput = 0.0
    if not hasattr(battery, 'soh'):
        battery.soh = 1.0  # State of Health (1 = 100%)

    battery.cycle_energy_throughput += energy_discharged_kWh
    capacity_loss = battery.cycle_energy_throughput * degradation_rate
    battery.soh = max(0.0, 1.0 - capacity_loss)
    battery.capacity = battery.capacity * battery.soh

    # Ensure remaining capacity and soc are consistent with new capacity
    battery.remaining_capacity = min(battery.remaining_capacity, battery.capacity)
    battery.soc = max(0.0, min(1.0, battery.remaining_capacity / battery.capacity))


def run_simulation(num_houses, daily_kWh_per_house, resolution_steps, dt, use_supercap=True):
    # Generate load profile
    load, time = generate_community_load_profile(
        num_houses=num_houses,
        daily_kWh_per_house=daily_kWh_per_house,
        time_steps=resolution_steps
    )

    # Initialize battery and supercap
    battery = Battery(capacity=500, voltage=480, discharge_rate=250)  # 500 kWh capacity
    if use_supercap:
        supercap = Supercapacitor(capacitance=1000, voltage_init=480)
    else:
        supercap = None

    # Initialize EMS controller
    if use_supercap:
        ems = EMSController(battery, supercap)
    else:
        # EMSController without supercap, just give it a dummy supercap with zero discharge
        class DummySupercap:
            discharge_rate = 0
            def deliver_power(self, power, dt):
                return 0, 0
        ems = EMSController(battery, DummySupercap())

    results = []
    soh_history = []
    for t in range(resolution_steps):
        power_demand = load[t] * 1000  # kW to W
        snapshot = ems.dispatch(power_demand, dt)

        # Calculate energy discharged by battery this step in kWh (convert W * sec to kWh)
        energy_discharged_kWh = abs(snapshot['batt_power']) * dt / 3600 / 1000

        # Apply degradation model
        degrade_battery(battery, energy_discharged_kWh)

        results.append(snapshot)
        soh_history.append(battery.soh)

    results_dict = {key: [r[key] for r in results] for key in results[0]}

    return time, load, results_dict, soh_history


def main():
    num_houses = 10
    daily_kWh_per_house = 21.0
    resolution_steps = 96  # 15-minute intervals for 24 hours
    dt = 900  # 15 minutes in seconds

    # Plot community load profile first
    load, time = generate_community_load_profile(
        num_houses=num_houses,
        daily_kWh_per_house=daily_kWh_per_house,
        time_steps=resolution_steps
    )
    plot_load_profile(time, load, title=f"{num_houses} Houses Community Load (15-min Resolution)")

    # Run BESS + Supercap simulation
    time, load, results_hess, soh_hess = run_simulation(num_houses, daily_kWh_per_house, resolution_steps, dt, use_supercap=True)

    # Run BESS only simulation
    _, _, results_bess_only, soh_bess_only = run_simulation(num_houses, daily_kWh_per_house, resolution_steps, dt, use_supercap=False)

    # Plot HESS results (BESS + Supercap)
    plot_hess_results(time, results_hess)

    # Plot SoH comparison
    plt.figure(figsize=(10, 6))
    plt.plot(time, soh_hess, label='BESS + Supercap SoH')
    plt.plot(time, soh_bess_only, label='BESS Only SoH')
    plt.xlabel('Time (s)')
    plt.ylabel('State of Health (SoH)')
    plt.title('Battery State of Health Over Time')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    main()
