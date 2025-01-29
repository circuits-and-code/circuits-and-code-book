import numpy as np
import matplotlib.pyplot as plt
import argparse
from math import sqrt

# fmt: off

TITLE = "Buck Converter in Discontinuous Conduction Mode"

def plotter() :
    VIN = 12          # Input voltage (V)
    VOUT = 3.3        # vout   
    IOUT_AVG = 0.1 # for inductor curr plot only 
    IOUT_RIPPLE_RATIO = 0.3
    iout_max = IOUT_AVG * (1+(IOUT_RIPPLE_RATIO/2))
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
    t_off = (1 - D - 0.3) * T_s                              # Switch OFF time before resonance

    t = np.linspace(0, 3 * T_s, 5000)  # High resolution for smooth waveform

    def switch_node_voltage(time):
        v_s = np.zeros_like(time)
        for i, t_i in enumerate(time):
            cycle_pos = t_i % T_s  # Time within each cycle
            if cycle_pos < t_on:
                v_s[i] = VIN  # Switch ON
            elif cycle_pos < t_on + t_off:
                v_s[i] = 0  # Diode conduction
            else:
                # Resonance after diode conduction ends
                t_res = cycle_pos - (t_on + t_off)
                v_s[i] = (VOUT) * np.cos(omega_res * t_res - (np.pi)) * np.exp(-t_res / (R_damping * C_parasitic)) + (VOUT)
        return v_s
    v_sw = switch_node_voltage(t)

    # TODO DRAW PLOT : @daniel fix the inductor current plot 
    triangle_wave = np.mod(t * f_sw, 1)
    triangle_wave = np.where(
        triangle_wave < D,
        2 * triangle_wave / D,  # Rising part
        2 * (1 - triangle_wave) / (1 - D)  # Falling part
    )
    i_l = (IOUT_RIPPLE_RATIO / 2) * triangle_wave + (IOUT_AVG - (IOUT_RIPPLE_RATIO / 2))

    fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax[0].plot(t, v_sw, label="Vsw")
    ax[0].axhline(y=VIN, color='g', linestyle='--', label=f"Vin")
    ax[0].axhline(y=VOUT, color='r', linestyle='--', label=f"Vout")
    ax[0].axhline(y=VOUT*2, color='y', linestyle='--', label=f"Vout*2")
    ax[0].set_title(f"{TITLE}")
    ax[0].set_ylim(0, VIN*1.1) 
    ax[0].set_xlabel("Time")
    ax[0].set_ylabel("Voltage")
    ax[0].legend()

    ax[1].plot(t, i_l, label="Il")
    ax[1].axhline(y=IOUT_AVG, color='r', linestyle='--', label=f"Ioutavg")
    ax[1].set_ylim(0, iout_max*1.1) 
    ax[1].set_xlabel("Time")
    ax[1].set_ylabel("Current")
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
