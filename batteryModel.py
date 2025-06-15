import math

class Battery:
    def __init__(self, capacity, voltage, discharge_rate, soc_init=1.0, internal_resistance=0.005):
        self.voltage = voltage
        self.r = internal_resistance
        self.capacity_As = capacity * 3600 * 1000 / voltage  # convert kWh to As
        self.current = 0.0
        
        self.capacity = capacity
        self.remaining_capacity = capacity * soc_init
        self.soc = max(0.0, min(1.0, soc_init))
        self.discharge_rate = discharge_rate*10**3
        self.discharge_efficiency = 0.90
        

    def discharge(self, power_load, dt):
        if power_load <= 0 or self.soc <= 0:
            self.current = 0.0
            return self.voltage, 0.0

        # Cap power load to discharge rate
        power_load = min(power_load, self.discharge_rate)
        if (power_load > self.discharge_rate):
            print("battey cant provide higher than discharge rate")
        
        # Estimate current and terminal voltage with internal resistance
        current = power_load / self.voltage
        #print(f"pwoer load {power_load} self.voltage {self.voltage} current {current}")
        terminal_voltage = max(0.0, self.voltage - current * self.r)
        current = power_load / terminal_voltage if terminal_voltage > 0 else 0.0
        #print(f"current adjusted {current}")

        # Limit current to what the battery can handle
        max_current = self.discharge_rate / self.voltage
        current = min(current, max_current)
        #print(f"current min {current}")

        # SOC drop due to energy drained, with a nonlinear factor
        linear_drop = (current * dt) / self.capacity_As
        scale = 1.5 - math.exp(-5 * (1 - self.soc))  # nonlinear scale
        nonlinear_drop = linear_drop * scale

        # Energy discharged = Power × Time (in hours)
        energy_used_kWh = ((power_load*10**-3) * dt) / 3600  # dt is in seconds

        # Apply discharge efficiency
        actual_energy_removed = energy_used_kWh / self.discharge_efficiency
        #print(f"actual_energy_removed {actual_energy_removed}")

        # Reduce remaining capacity
        self.remaining_capacity = max(0.0, self.remaining_capacity - actual_energy_removed)
    
        # Update SoC
        self.soc = (self.remaining_capacity / self.capacity) - nonlinear_drop
        self.current = current

        return terminal_voltage, current

    def degrade_battery(battery, energy_discharged_kWh, degradation_rate=0.0001):
        """
        Simple degradation model:
        - battery: Battery instance
        - energy_discharged_kWh: energy removed this step in kWh
        - degradation_rate: fraction capacity lost per kWh throughput (example value)

        Updates battery capacity and SoH.
        """
        # Initialize cycle_energy_throughput attribute if not present
        if not hasattr(battery, 'cycle_energy_throughput'):
            battery.cycle_energy_throughput = 0.0

        if not hasattr(battery, 'soh'):
            battery.soh = 1.0  # State of Health (1.0 = 100%)

        # Accumulate total energy throughput
        battery.cycle_energy_throughput += energy_discharged_kWh

        # Calculate degradation: linear model
        capacity_loss = battery.cycle_energy_throughput * degradation_rate

        # Update SoH and capacity
        battery.soh = max(0.0, 1.0 - capacity_loss)
        battery.capacity = battery.capacity * battery.soh

        # Make sure remaining_capacity and soc do not exceed new capacity
        battery.remaining_capacity = min(battery.remaining_capacity, battery.capacity)
        battery.soc = max(0.0, min(1.0, battery.remaining_capacity / battery.capacity))

