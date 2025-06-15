class Supercapacitor:
    def __init__(self, capacitance, voltage_init=480, r_internal=0.001, max_voltage=500, discharge_rate_kW=10):
        self.c = capacitance  # Farads
        self.voltage = voltage_init  # Volts
        self.max_voltage = max_voltage
        self.r = r_internal  # Ohms
        self.discharge_rate = discharge_rate_kW * 1000  # Convert kW to W
        self.power = 0.5 * self.c * (self.voltage ** 2)  # Stored energy in Joules

    def deliver_power(self, power, dt):
        # power > 0: charging (currently ignored or clamped)
        # power < 0: discharging (allowed, capped)

        if power >= 0:
            # Ignore or prevent charging above max voltage
            if self.voltage >= self.max_voltage:
                return self.voltage, 0.0
            return self.voltage, 0.0

        # Discharging: enforce voltage and discharge limit
        if self.voltage <= 0.1:
            return self.voltage, 0.0

        # Cap discharge to max discharge rate
        power = max(power, -self.discharge_rate)  # power is negative when discharging
        current = power / self.voltage  # Current will be negative
        dv = (current * dt) / self.c
        self.voltage += dv  # dv is negative => voltage decreases

        # Update stored power
        self.power = 0.5 * self.c * (self.voltage ** 2)

        return self.voltage, current
