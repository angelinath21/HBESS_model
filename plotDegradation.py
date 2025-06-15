import matplotlib.pyplot as plt
import numpy as np

class Battery:
    def __init__(self, name, capacity_kWh, degradation_factor, hbess=False):
        self.name = name
        self.initial_capacity = capacity_kWh
        self.capacity = capacity_kWh
        self.degradation_factor = degradation_factor
        self.soh = 1.0
        self.total_throughput = 0.0
        self.hbess = hbess

    def degrade(self, cycle_energy_kWh, avg_soc):
        if self.hbess:
            if avg_soc <= 0.5:
                soc_factor = 1.0 + 1.0 * avg_soc
            elif avg_soc <= 0.75:
                soc_factor = 1.5
            else:
                soc_factor = 1.7

            wear_factor = 1 + 2 * (1 - self.soh)
            soc_diff_factor = 1 + 0.7 * np.exp(4.4 * (avg_soc - 0.5))  # mild exponential
        else:
            if avg_soc <= 0.25:
                soc_factor = 1.0
            elif avg_soc <= 0.5:
                soc_factor = 1.2
            elif avg_soc <= 0.75:
                soc_factor = 1.5
            else:
                soc_factor = 1.7

            wear_factor = 1 + 10 * (1 - self.soh)**3
            soc_diff_factor = 0.8 + 0.5 * np.exp(5 * (avg_soc - 0.7))  # steep exponential
            soc_diff_factor = min(soc_diff_factor, 10)  # clamp max value

        delta_capacity = cycle_energy_kWh * self.degradation_factor * soc_factor * wear_factor * soc_diff_factor

        self.total_throughput += cycle_energy_kWh
        self.capacity = max(0, self.capacity - delta_capacity)
        self.soh = self.capacity / self.initial_capacity
        return self.soh

def simulate_degradation(battery, avg_soc, cycle_energy_kWh, max_cycles=3000):
    sohs = []
    cycles = []

    for cycle in range(max_cycles):
        soh = battery.degrade(cycle_energy_kWh, avg_soc)
        sohs.append(soh)
        cycles.append(cycle)
        if soh <= 0.2:  # end-of-life threshold
            break
    return cycles, sohs

def plot_degradation():
    soc_levels = [0.25, 0.50, 0.75, 0.90]
    colors = ['green', 'blue', 'orange', 'red']

    bess_factor = 0.008     # BESS degrades faster
    hbess_factor = 0.003   # HBESS degrades slower

    cycle_energy_kWh = 1.0  # use stronger throughput to see curvature

    plt.figure(figsize=(14, 6))

    # Plot BESS
    plt.subplot(1, 2, 1)
    for soc, color in zip(soc_levels, colors):
        bess = Battery("BESS", 100, bess_factor, hbess=False)
        cycles, sohs = simulate_degradation(bess, soc, cycle_energy_kWh)
        plt.plot(cycles, sohs, label=f"SoC {int(soc*100)}%", color=color)

    plt.title("BESS - Battery Health vs. Cycles")
    plt.xlabel("Cycle Count")
    plt.ylabel("State of Health (SoH)")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True)

    # Plot HBESS
    plt.subplot(1, 2, 2)
    for soc, color in zip(soc_levels, colors):
        hbess = Battery("HBESS", 100, hbess_factor, hbess=True)
        cycles, sohs = simulate_degradation(hbess, soc, cycle_energy_kWh)
        plt.plot(cycles, sohs, label=f"SoC {int(soc*100)}%", color=color)

    plt.title("HBESS - Battery Health vs. Cycles")
    plt.xlabel("Cycle Count")
    plt.ylabel("State of Health (SoH)")
    plt.ylim(0, 1.05)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_degradation()
