import math

class Meter:
    def __init__(self, name="HBESS Meter", nominal_voltage=480):
        self.name = name
        self.nominal_voltage = nominal_voltage
        self.v_rms = 0.0
        self.i_rms = 0.0
        self.p = 0.0  # Active Power (W)
        self.q = 0.0  # Reactive Power (VAR)
        self.s = 0.0  # Apparent Power (VA)
        self.pf = 1.0

    def update(self, voltage_rms, current_rms, phase_angle_deg=0.0):
        """
        Update meter readings.
        
        :param voltage_rms: RMS line voltage (V)
        :param current_rms: RMS line current (A)
        :param phase_angle_deg: phase angle between V and I (degrees)
        """
        angle_rad = math.radians(phase_angle_deg)

        self.v_rms = voltage_rms
        self.i_rms = current_rms
        self.s = voltage_rms * current_rms  # Apparent Power (S)
        self.p = self.s * math.cos(angle_rad)  # Active Power (P)
        self.q = self.s * math.sin(angle_rad)  # Reactive Power (Q)
        self.pf = math.cos(angle_rad)

    def read(self):
        return {
            "V_rms (V)": self.v_rms,
            "I_rms (A)": self.i_rms,
            "P (W)": self.p,
            "Q (VAR)": self.q,
            "S (VA)": self.s,
            "Power Factor": self.pf
        }
