from loadProfile import generate_community_load_profile
from plotUtils import plot_load_profile, plot_hess_results, plot_load_fft
from batteryModel import Battery
from supercapModel import Supercapacitor
from emsController import EMSController

def main():
    # Configuration
    num_houses = 10
    daily_kWh_per_house = 21.0
    resolution_steps = 86400  # 15-min resolution
    dt = 1  # 15 minutes in seconds

    # Load profile generation
    load, time = generate_community_load_profile(
        num_houses=num_houses,
        daily_kWh_per_house=daily_kWh_per_house,
        time_steps=resolution_steps
    )

    # Plot load profile first
    plot_load_profile(time, load, title=f"{num_houses} Houses Community Load (15-min Resolution)")

    # Initialize system models
    battery = Battery(capacity=500, voltage=480, discharge_rate=250) #250kW/h  
    supercap = Supercapacitor(capacitance=1000, voltage_init=480)
    ems = EMSController(battery, supercap)

    # Run simulation loop
    results = []
    for t in range(resolution_steps):
        power_demand = load[t] * 1000  # kW to W
        snapshot = ems.dispatch(power_demand, dt)
        results.append(snapshot)

    # Convert list of dicts to dict of lists for plotting convenience
    results_dict = {key: [r[key] for r in results] for key in results[0]}

    # Plot HESS simulation results
    plot_hess_results(time, results_dict)

if __name__ == "__main__":
    main()
