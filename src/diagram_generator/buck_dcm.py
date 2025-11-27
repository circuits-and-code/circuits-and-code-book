import numpy as np
import matplotlib.pyplot as plt
import argparse
from math import sqrt

# fmt: off

TITLE = "Buck Converter in Discontinuous Conduction Mode"

def plotter() :
    VIN = 12          # Input voltage (V)
    VOUT = 3.3        # vout   
    i_out_max = 0.2
    D = 0.4            # Duty cycle
    T_s = 10e-6        # Switching period (s)
    f_sw = 1.0 / T_s
    L = 100e-6         # Inductance (H)
    C_parasitic = 100e-12 # Parasitic capacitance at the switch node (F)
    k = 1000
    R_damping = 20*k    # Effective damping resistance (Ohm)
    f_res = 1 / (2 * np.pi * np.sqrt(L * C_parasitic))  # Resonant frequency (Hz)
    f_res = f_res / 2
    omega_res = 2 * np.pi * f_res                      # Angular resonant frequency
    t_on = (D - 0.15) * T_s                                     # Switch ON time
    t_off = (1 - D - 0.45) * T_s                              # Switch OFF time before resonance

    NUM_PTS = 5000

    t = np.linspace(0, 3 * T_s, NUM_PTS) 

    v_sw = np.zeros_like(t)
    i_l = np.zeros_like(t)
    i_l_total = 0
    for i, t_i in enumerate(t):
        cycle_pos = t_i % T_s  # Time within each cycle
        if cycle_pos < t_on : # Switch ON
            v_sw[i] = VIN  
            i_l[i] = (cycle_pos / t_on) *  i_out_max
        elif cycle_pos < t_on + t_off: # Diode conduction
            v_sw[i] = 0  
            i_l[i] = i_out_max - ((cycle_pos - t_on) / t_off) *  i_out_max
        else: # Resonance after diode conduction ends
            t_res = cycle_pos - (t_on + t_off)
            v_sw[i] = (VOUT) * np.cos(omega_res * t_res - (np.pi)) * np.exp(-t_res / (R_damping * C_parasitic)) + (VOUT)
            i_l[i] = 0
        i_l_total += i_l[i]
    i_out_avg = i_l_total / NUM_PTS

    fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax[0].plot(t, v_sw, label="Switch Node Voltage (V_sw)")
    ax[0].axhline(y=VIN, color='g', linestyle='--', label=f"Input Voltage (V_in)")
    ax[0].axhline(y=VOUT, color='r', linestyle='--', label=f"Output Voltage (V_out)")
    ax[0].axhline(y=VOUT*2, color='y', linestyle='--', label=f"V_out*2")
    ax[0].set_title(f"{TITLE}")
    ax[0].set_ylim(0, VIN*1.1) 
    ax[0].set_xlabel("Time (seconds)")
    ax[0].set_ylabel("Voltage (volts)")
    ax[0].legend()

    ax[1].plot(t, i_l, label="Load Current (I_l)")
    ax[1].axhline(y=i_out_avg, color='r', linestyle='--', label=f"Avg Output Current (I_out_avg)")
    ax[1].axhline(y=i_out_max, color='y', linestyle='--', label=f"Max Output Current (I_out_max)")
    ax[1].set_ylim(0, i_out_max*1.1) 
    ax[1].set_xlabel("Time (seconds)")
    ax[1].set_ylabel("Current (amps)")
    ax[1].legend()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(f"{TITLE} Plotter")
    parser.add_argument("--output_path", help="Path to save image to")

    args = parser.parse_args()

    plotter()

    if args.output_path is not None:
        plt.savefig(args.output_path)
    else:
        plt.show()

# fmt: on
