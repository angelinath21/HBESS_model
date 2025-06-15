import numpy as np
import matplotlib.pyplot as plt

class Battery:
    def __init__(self, capacity_kWh, voltage_nominal, discharge_rate_W, soc_init=1.0, r0=0.01, r1=0.05, c1=5000):
        self.voltage_nominal = voltage_nominal
        self.r0 = r0              # Ohmic internal resistance (Ohms)
        self.r1 = r1              # Polarization resistance (Ohms)
        self.c1 = c1              # Polarization capacitance (Farads)
        self.v_rc = 0             # Voltage across RC network (Volts)
        
        self.capacity_kWh = capacity_kWh
        self.remaining_capacity_kWh = capacity_kWh * soc_init
        self.soc = soc_init
        self.discharge_rate_W = discharge_rate_W
        self.current = 0
        
    def discharge(self, power_load_W, dt_s):
        if power_load_W <= 0 or self.soc <= 0:
            self.current = 0
            return self.voltage_nominal, 0.0
        
        # Limit power load by max discharge rate
        power_load_W = min(power_load_W, self.discharge_rate_W)
        
        # Estimate initial current
        current_A = power_load_W / self.voltage_nominal
        
        # Update v_rc using Euler integration: dv_rc/dt = (-1/(R1*C1)) * v_rc + (1/C1) * I
        dv_rc = (-1/(self.r1 * self.c1) * self.v_rc + current_A / self.c1) * dt_s
        self.v_rc += dv_rc
        
        # Terminal voltage with transient effect
        terminal_voltage = max(0, self.voltage_nominal - current_A * self.r0 - self.v_rc)
        
        # Recalculate current using terminal voltage to be more accurate
        if terminal_voltage > 0:
            current_A = power_load_W / terminal_voltage
        else:
            current_A = 0
        
        # Update SOC (simplified energy-based)
        energy_used_kWh = (power_load_W * dt_s) / (3600 * 1000)  # convert W*s to kWh
        self.remaining_capacity_kWh = max(0, self.remaining_capacity_kWh - energy_used_kWh)
        self.soc = self.remaining_capacity_kWh / self.capacity_kWh
        
        self.current = current_A
        return terminal_voltage, current_A

# Simulation parameters
dt = 0.1  # time step in seconds
total_time = 300  # total simulation time in seconds (5 minutes)
time_steps = int(total_time / dt)

# Create battery instance
battery = Battery(capacity_kWh=1.0, voltage_nominal=48, discharge_rate_W=2000, r0=0.01, r1=0.05, c1=5000)

# Prepare arrays for storing results
time_array = np.linspace(0, total_time, time_steps)
voltage_array = np.zeros(time_steps)
current_array = np.zeros(time_steps)
power_load_array = np.zeros(time_steps)

# Define power load profile: step load starting at 10 seconds
for i in range(time_steps):
    t = i * dt
    if t < 10:
        power_load_array[i] = 100  # 100 W idle load
    else:
        power_load_array[i] = 1500  # Step up to 1500 W load

# Run simulation
for i in range(time_steps):
    voltage, current = battery.discharge(power_load_array[i], dt)
    voltage_array[i] = voltage
    current_array[i] = current

# Plot results
plt.figure(figsize=(12, 6))
plt.subplot(2,1,1)
plt.plot(time_array, power_load_array, label='Power Load (W)', color='orange')
plt.ylabel('Power Load (W)')
plt.legend()
plt.grid(True)

plt.subplot(2,1,2)
plt.plot(time_array, voltage_array, label='Terminal Voltage (V)')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.legend()
plt.grid(True)

plt.suptitle("Battery Terminal Voltage Response with Transient RC Model")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
