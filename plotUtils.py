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