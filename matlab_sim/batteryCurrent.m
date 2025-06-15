clc; clear; close all;

% Parameters
dt = 0.01;
t_end = 7;
time = 0:dt:t_end;

% Step change times
step_up = 0.1;
step_down = 1.8;

% Battery parameters
tau_batt = 0.3;         % time constant
zeta_batt = 0.45;       % low damping (no SC)
tau_batt_sc = 0.3;
zeta_batt_sc = 0.6;     % high damping (with SC)

% Load step values
I_load_high = 300;
I_load_low = 0;

% Preallocate
I_batt = zeros(size(time));
I_batt_sc = zeros(size(time));

% Natural frequencies
omega_batt = 1 / tau_batt;
omega_batt_sc = 1 / tau_batt_sc;

% Initial states
x1 = 0; x2 = 0;
x1_sc = 0; x2_sc = 0;

for i = 2:length(time)
    if time(i) < step_up
        setpoint = I_load_low;
    elseif time(i) < step_down
        setpoint = I_load_high;
    else
        setpoint = I_load_low;
    end

    % Battery only
    dx1 = x2;
    dx2 = omega_batt^2 * (setpoint - x1) - 2*zeta_batt*omega_batt*x2;
    x1 = x1 + dx1*dt;
    x2 = x2 + dx2*dt;
    I_batt(i) = x1;

    % Battery + SC
    dx1_sc = x2_sc;
    dx2_sc = omega_batt_sc^2 * (setpoint - x1_sc) - 2*zeta_batt_sc*omega_batt_sc*x2_sc;
    x1_sc = x1_sc + dx1_sc*dt;
    x2_sc = x2_sc + dx2_sc*dt;
    I_batt_sc(i) = x1_sc;
end

%% Extract time window: after step-up and before step-down
mask = (time >= step_up) & (time <= step_down);
t_window = time(mask);
y1_window = I_batt(mask);
y2_window = I_batt_sc(mask);

%% Metrics in window
target = I_load_high;
[overshoot1, rise1, settle1] = step_metrics(t_window, y1_window, target);
[overshoot2, rise2, settle2] = step_metrics(t_window, y2_window, target);

%% Plot
figure('Position',[100 100 1000 500]);
plot(time, I_batt, 'r-', 'LineWidth', 2); hold on;
plot(time, I_batt_sc, 'b-', 'LineWidth', 2);

xlabel('Time (s)');
ylabel('Battery Current (A)');
title('Battery Current with and without Supercapacitor');
legend({...
    sprintf('Battery only (OS: %.1f%%)', overshoot1), ...
    sprintf('Battery + SC (OS: %.1f%%)', overshoot2) ...
}, 'Location', 'SouthEast');
grid on;

%% Function to compute metrics
function [overshoot, rise_time, settling_time] = step_metrics(t, y, target)
    % Rise time (10% to 90%)
    idx_10 = find(y >= 0.1 * target, 1);
    idx_90 = find(y >= 0.9 * target, 1);
    if ~isempty(idx_10) && ~isempty(idx_90)
        rise_time = t(idx_90) - t(idx_10);
    else
        rise_time = NaN;
    end

    % Overshoot
    peak = max(y);
    overshoot = max(0, (peak - target) / target * 100);

    % Settling time (±2% band)
    settle_band = 0.02 * target;
    within_band = abs(y - target) <= settle_band;

    % Find the last time it enters and STAYS within band
    N = 20;  % Number of future samples to confirm it stays settled (0.2s)
    settling_time = NaN;
    for i = 1:(length(t) - N)
        if all(within_band(i:i+N))
            settling_time = t(i);
            break;
        end
    end

    % Final fallback: if it ends within band
    if isnan(settling_time) && abs(y(end) - target) <= settle_band
        settling_time = t(end);
    end
end