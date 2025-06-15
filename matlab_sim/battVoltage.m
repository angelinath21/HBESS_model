% Simulation parameters
t = 0:0.001:5; % 5 seconds, 1 ms resolution
I_load = zeros(size(t));

% Create step up and down: 300 A step at 1s, back down at 3s
I_load(t >= 1 & t < 3) = 300;

% Battery model parameters
R_batt = 0.01;    % Internal resistance [ohm]
C_batt = 500;     % Capacitance-like behavior [F], simplifies voltage drop
V0 = 480;         % Initial battery voltage [V]

% Supercapacitor parameters
R_sc = 0.001;     % Very low internal resistance
C_sc = 50;        % Large capacitance [F]

% Initialize voltage arrays
V_batt_only = zeros(size(t));
V_batt_SC = zeros(size(t));
V_sc = zeros(size(t));

% Initial voltages
V_batt_only(1) = V0;
V_batt_SC(1) = V0;
V_sc(1) = V0;

% Simulation loop
for i = 2:length(t)
    dt = t(i) - t(i-1);

    % Case 1: Battery only supplies load
    I_batt = I_load(i);
    dV_batt = -(I_batt / C_batt) * dt - R_batt * I_batt;
    V_batt_only(i) = V_batt_only(i-1) + dV_batt;

    % Case 2: SC helps handle transients
    if abs(I_load(i) - I_load(i-1)) > 50 % Transient detected
        I_sc = 100; % SC delivers fixed current for transient
    else
        I_sc = 0;
    end
    I_batt = I_load(i) - I_sc;

    % Update voltages
    dV_batt = -(I_batt / C_batt) * dt - R_batt * I_batt;
    dV_sc = -(I_sc / C_sc) * dt - R_sc * I_sc;

    V_batt_SC(i) = V_batt_SC(i-1) + dV_batt;
    V_sc(i) = V_sc(i-1) + dV_sc;
end

% Plot results
figure;
plot(t, V_batt_only, 'b', 'LineWidth', 1.5); hold on;
plot(t, V_batt_SC, 'r', 'LineWidth', 1.5);
yline(V0, '--k', 'Nominal Voltage');

xlabel('Time (s)');
ylabel('Battery Voltage (V)');
title('Battery Voltage Dynamics with and without Supercapacitor');
legend('Battery Only', 'Battery + SC', 'Nominal Voltage');
grid on;
