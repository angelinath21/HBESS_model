import numpy as np
import matplotlib.pyplot as plt

def plot_load_profile(time_vector, load_vector, title="Community Load Profile"):
    plt.figure(figsize=(10, 5))
    plt.plot(time_vector, load_vector, label='Load (kW)', color='tab:blue')
    plt.title(title)
    plt.xlabel("Time of Day (Hours)")
    plt.ylabel("Power (kW)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_hess_results(time_vector, results):
    plt.figure(figsize=(12, 12))  # extra height for 4 subplots

    # --- Subplot 1: Power Distribution ---
    plt.subplot(3, 1, 1)
    plt.plot(time_vector, [p/1000 for p in results['load_power']], label='Load (kW)', color='tab:blue')
    # plt.plot(time_vector, [-p/1000 for p in results['sc_power']], label='Supercap Power (kW)', color='tab:orange')
    # plt.plot(time_vector, [-p/1000 for p in results['batt_power']], label='Battery Power (kW)', color='tab:green')
    plt.title("Power Distribution")
    plt.ylabel("Power (kW)")
    plt.legend()
    plt.grid(True)

    # --- Subplot 2: Battery SoC, P, and Q ---
    plt.subplot(3, 1, 2)
    plt.plot(time_vector, results['soc_batt'], marker='o', linestyle='-')
    plt.xlabel("Time of Day (Hours)")
    plt.ylabel("State of Charge (%)")
    plt.title("Battery Voltage vs Time")
    plt.grid(True)

    # --- Subplot 3: Supercapacitor Voltage ---
    plt.subplot(3, 1, 3)
    plt.plot(time_vector, results['v_sc'], label='Supercap Voltage (V)', color='tab:orange')
    plt.xlabel("Time of Day (Hours)")
    plt.ylabel("Voltage (V)")
    plt.title("Supercapacitor Voltage")
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

def plot_load_fft(load_vector, dt, title="FFT of Load Profile"):
    # Number of samples
    n = len(load_vector)

    # Compute FFT
    fft_vals = np.fft.fft(load_vector)
    fft_freq = np.fft.fftfreq(n, dt)

    # Take only positive frequencies (real signals)
    pos_mask = fft_freq >= 0
    freqs = fft_freq[pos_mask]
    magnitudes = np.abs(fft_vals[pos_mask]) * 2 / n  # Normalize amplitude

    plt.figure(figsize=(10, 5))
    plt.stem(freqs, magnitudes)  # Removed use_line_collection
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def plot_performance_degradation(time, soh_hess, soh_bess_only):
    """
    Plots State of Health (SoH) over time for HBESS and BESS only.
    :param time: List or array of time points (seconds)
    :param soh_hess: List or array of SoH values for HBESS (0 to 1)
    :param soh_bess_only: List or array of SoH values for BESS only (0 to 1)
    """
    plt.figure(figsize=(10, 6))
    plt.plot(time, soh_hess, label="HBESS (Battery + Supercap)")
    plt.plot(time, soh_bess_only, label="BESS Only (Battery)")
    plt.xlabel("Time (seconds)")
    plt.ylabel("State of Health (SoH)")
    plt.title("Battery Performance Degradation Over Time")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_cycle_life(time, soh_hess, soh_bess_only, degradation_threshold=0.8):
    """
    Estimates cycle life based on when SoH crosses degradation threshold (e.g., 80% capacity).
    Plots the degradation curves and marks cycle life points.
    :param time: List or array of time points (seconds)
    :param soh_hess: SoH values for HBESS (0 to 1)
    :param soh_bess_only: SoH values for BESS only (0 to 1)
    :param degradation_threshold: SoH threshold to define end of cycle life (default 0.8)
    """
    # Find first index where SoH <= threshold (or last index if never reached)
    def find_cycle_life_index(soh):
        for i, v in enumerate(soh):
            if v <= degradation_threshold:
                return i
        return len(soh) - 1

    idx_hess = find_cycle_life_index(soh_hess)
    idx_bess = find_cycle_life_index(soh_bess_only)

    cycle_life_time_hess = time[idx_hess]
    cycle_life_time_bess = time[idx_bess]

    plt.figure(figsize=(10, 6))
    plt.plot(time, soh_hess, label="HBESS (Battery + Supercap)")
    plt.plot(time, soh_bess_only, label="BESS Only (Battery)")

    plt.axhline(y=degradation_threshold, color='r', linestyle='--', label=f'Degradation Threshold ({degradation_threshold*100}%)')

    plt.scatter(cycle_life_time_hess, soh_hess[idx_hess], color='blue', marker='o',
                label=f'HBESS Cycle Life @ {cycle_life_time_hess}s')
    plt.scatter(cycle_life_time_bess, soh_bess_only[idx_bess], color='orange', marker='o',
                label=f'BESS Cycle Life @ {cycle_life_time_bess}s')

    plt.xlabel("Time (seconds)")
    plt.ylabel("State of Health (SoH)")
    plt.title("Cycle Life Estimation Based on SoH Degradation")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()