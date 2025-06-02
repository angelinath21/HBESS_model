class PIController:
    def __init__(self, kp, ki, setpoint, output_limits=(0, 2500)):
        """
        Proportional-Integral (PI) Controller.

        Args:
            kp (float): Proportional gain
            ki (float): Integral gain
            setpoint (float): Desired setpoint
            output_limits (tuple): Min and max output limits
        """
        self.kp = kp
        self.ki = ki
        self.setpoint = setpoint
        self.integral = 0
        self.output_limits = output_limits

    def update(self, measurement, dt):
        """
        Compute PI output.

        Args:
            measurement (float): Current measured value
            dt (float): Time step in seconds

        Returns:
            float: Output signal
        """
        error = self.setpoint - measurement
        self.integral += error * dt
        output = self.kp * error + self.ki * self.integral
        return max(self.output_limits[0], min(output, self.output_limits[1]))
