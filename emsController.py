from collections import deque
from droopControl import droop_control
from PIController import PIController

class EMSController:
    def __init__(self, battery, supercap, transient_threshold=1000, window_seconds=10):
        self.battery = battery
        self.supercap = supercap
        self.transient_threshold = transient_threshold
        self.window_seconds = window_seconds
        self._power_history = deque(maxlen=window_seconds)

        self.batt_pi = PIController(kp=0.1, ki=0.05, setpoint=0, output_limits=(-1000, 0))

    def detect_transient(self, instanenous_power_demand):
        self._power_history.append(instanenous_power_demand)

        if len(self._power_history) < self.window_seconds:
            return False

        power_change = abs(instanenous_power_demand - self._power_history[0])
        print(f'[TRANSIENT CHECK] Power over {self.window_seconds}s: {power_change:.2f}W')

        return power_change > self.transient_threshold

    def dispatch(self, instanenous_power_demand, dt, f_measured=49.8):
        is_transient = self.detect_transient(instanenous_power_demand)

        sc_power = 0.0
        if is_transient:
            print("[INFO] Transient detected")
            # SC will discharge up to its max discharge rate (negative because discharging)
            sc_power = -min(abs(instanenous_power_demand), self.supercap.discharge_rate)

        # Remaining power to be handled by battery
        batt_power_requested = instanenous_power_demand - sc_power

        # Dispatch to devices
        v_sc, i_sc = self.supercap.deliver_power(sc_power, dt)
        v_batt, i_batt = self.battery.discharge(batt_power_requested, dt)

        print(f"[DISPATCH] Load: {instanenous_power_demand:.2f}W | SC: {sc_power:.2f}W | Batt: {batt_power_requested:.2f}W")

        return {
            'load_power': instanenous_power_demand,
            'sc_power': sc_power,
            'batt_power': batt_power_requested,
            'v_sc': v_sc,
            'v_batt': v_batt,
            'i_sc': i_sc,
            'i_batt': i_batt,
            'soc_batt': self.battery.soc
        }
