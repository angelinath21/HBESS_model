import numpy as np
import matplotlib.pyplot as plt

def generate_community_load_profile(num_houses, daily_kWh_per_house, time_steps=96):
    """
    Generates a synthetic 24-hour load profile for a community of houses at 15-minute resolution,
    including transient events.
    """

    def add_transients(profile, num_transients=3, magnitude_range=(0.5, 2.0), duration_range=(1, 4)):
        """
        Add random transients (spikes or dips) to the profile.

        Args:
            profile: 1D array of load (kW)
            num_transients: Number of transient events to add
            magnitude_range: tuple(min, max) transient size in kW
            duration_range: tuple(min, max) transient duration in time steps

        Returns:
            profile with transients added
        """
        profile = profile.copy()
        n = len(profile)

        for _ in range(num_transients):
            start = np.random.randint(0, n - 1)
            duration = np.random.randint(duration_range[0], duration_range[1] + 1)
            end = min(start + duration, n)

            magnitude = np.random.uniform(*magnitude_range)

            # Randomly decide if transient is a spike (+) or dip (-)
            sign = 1 if np.random.rand() > 0.5 else -1

            # Apply transient
            profile[start:end] += sign * magnitude

            # Prevent negative load
            profile = np.clip(profile, 0, None)

        return profile

    def single_house_profile():
        t = np.linspace(0, 24, time_steps)

        # Morning and evening peaks
        morning_peak = np.exp(-0.5 * ((t - 7.5) / 1.0) ** 2)
        evening_peak = np.exp(-0.5 * ((t - 18.5) / 1.5) ** 2)

        # Base load
        base_load = 0.2 + 0.1 * np.sin(2 * np.pi * t / 24)

        # Total profile (before scaling)
        profile = base_load + 2.0 * morning_peak + 3.0 * evening_peak
        profile += 0.05 * np.random.randn(time_steps)  # small noise
        profile = np.clip(profile, 0, None)

        # Add transient events
        profile = add_transients(profile, num_transients=5, magnitude_range=(0.5, 3.0), duration_range=(1, 3))

        # Scale to match daily energy consumption (kWh)
        energy_kWh = np.sum(profile) * (24 / time_steps)
        profile *= daily_kWh_per_house / energy_kWh

        return profile  # kW per 15-minute interval

    # Generate and sum all house profiles
    load_matrix = np.array([single_house_profile() for _ in range(num_houses)])
    community_load_kw = np.sum(load_matrix, axis=0)
    time_vector = np.linspace(0, 24, time_steps)

    return community_load_kw, time_vector
