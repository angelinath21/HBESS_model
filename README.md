# EEE30006 Hydrogen and Energy Storage  
## Hybrid Battery and Supercapacitor Model – Dynamic Simulation and Transient Management

### Overview

This repository contains the dynamic simulation and control strategy implementation for a Hybrid Battery and Supercapacitor Energy Storage System (HBESS), developed as part of the EEE30006 *Hydrogen and Energy Storage* unit. The focus is on transient response, power allocation, and system stability under fast-changing load conditions.

### Objectives

- Simulate the real-time dynamic response of a hybrid energy storage system.
- Evaluate the supercapacitor's role in mitigating transient load surges.
- Implement a control logic to detect and respond to high-power disturbances within a 1-second window.
- Quantify system performance improvements over conventional battery-only storage.

### Key Features

- **Sliding Window Transient Detection**  
  Detects transients exceeding 1 kW change within a 1-second window.

- **Fast Supercapacitor Response**  
  Supercapacitor dispatches power for 1 second during detected transients, while the battery supplies remaining demand.

- **Battery SOC Monitoring**  
  Smooths battery current and SOC profile by dynamically allocating rapid fluctuations to the supercapacitor.

- **Extreme Condition Testing**  
  Simulated 300 A load step-up/step-down events to compare HBESS vs conventional BESS voltage overshoot.

### Simulation Methodology

- **Load Profile Resolution**:  
  Simulated a 24-hour period at 1-minute intervals with additional 1-second resolution scenarios for transient testing.

- **Control Loop**:
  1. Load demand is read each timestep.
  2. Transient detection is performed using a moving average comparison.
  3. If transient >1 kW in 1s: supercapacitor is dispatched for 1s.
  4. Battery supplies remaining load and recharges the supercapacitor as needed.
  5. SOC and voltage are updated and logged at each step.

- **Extreme Load Event Simulation**:  
  Included a sudden 300 A load spike and drop to measure overshoot and system stability in both BESS and HBESS configurations.

### Results Summary

- **Transient Detection & Response**  
  Supercapacitor consistently responded within 1 s, scaling power output based on transient magnitude (see `Figure 5`).

- **Improved Voltage Stability**  
  - BESS overshoot: 21.8%  
  - HBESS overshoot: 10.1%  
  - (see `Figure X`)

- **Battery Health Impact**  
  SOC declined gradually with fewer aggressive cycles, improving battery longevity.

- **Power Sharing Effectiveness**  
  Supercapacitor managed short bursts of power, allowing the battery to follow the broader demand curve more steadily.

