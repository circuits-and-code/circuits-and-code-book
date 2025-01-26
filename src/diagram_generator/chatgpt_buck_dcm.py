import numpy as np
import matplotlib.pyplot as plt

# Define parameters
V_in = 12          # Input voltage (V)
V_out = 3.3        # vout   
D = 0.4            # Duty cycle
T_s = 10e-6        # Switching period (s)
L = 100e-6         # Inductance (H)
C_parasitic = 100e-12 # Parasitic capacitance at the switch node (F)
k = 1000
R_damping = 20*k    # Effective damping resistance (Ohm)

# Derived parameters
f_res = 1 / (2 * np.pi * np.sqrt(L * C_parasitic))  # Resonant frequency (Hz)
f_res = f_res / 2
omega_res = 2 * np.pi * f_res                      # Angular resonant frequency
t_on = (D - 0.15) * T_s                                     # Switch ON time
t_off = (1 - D - 0.3) * T_s                              # Switch OFF time before resonance

# Time vector
t = np.linspace(0, 3 * T_s, 5000)  # High resolution for smooth waveform

# Define switch node voltage function
def switch_node_voltage(time):
    v_s = np.zeros_like(time)
    for i, t_i in enumerate(time):
        cycle_pos = t_i % T_s  # Time within each cycle
        if cycle_pos < t_on:
            v_s[i] = V_in  # Switch ON
        elif cycle_pos < t_on + t_off:
            v_s[i] = 0  # Diode conduction
        else:
            # Resonance after diode conduction ends
            t_res = cycle_pos - (t_on + t_off)
            v_s[i] = (V_out) * np.cos(omega_res * t_res - (np.pi)) * np.exp(-t_res / (R_damping * C_parasitic)) + (V_out)
    return v_s

# Generate waveform
v_s_waveform = switch_node_voltage(t)

# Plotting
plt.figure(figsize=(10, 6))
# plt.plot(t * 1e6, v_s_waveform, label="Switch Node Voltage", color="b")
plt.plot(t * 1e6, v_s_waveform, color="b")
# plt.axvline(x=T_s * 1e6, color="r", linestyle="--", label="Switching Period (T_s)")
# plt.axvline(x=2 * T_s * 1e6, color="g", linestyle="--", label="2T_s")
# plt.axhline(0, color="k", linewidth=0.8, linestyle="--")
plt.title("Switch Node Voltage of a Buck Converter in DCM with Resonance")
plt.xlabel("Time (µs)")
plt.ylabel("Voltage (V)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

# chat gpt got this started, then I fixed it a lot, remove the extra stuff 