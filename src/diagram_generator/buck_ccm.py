import numpy as np
import matplotlib.pyplot as plt
import argparse

# fmt: off

TITLE = "Buck Converter in Continuous Conduction Mode"

def plotter() :
    NUM_POINTS = 1000
    SWITCHING_FREQUENCY = 3 # number of switching cycles to show 
    VIN = 12.0
    VOUT = 3.3
    assert VIN > VOUT # just cuz it'll kill my formulas otherwise 
    IOUT_AVG = 2.5
    IOUT_RIPPLE_RATIO = 0.3 # 30% is a common value 

    duty_cycle = VOUT / VIN
    negative_duty_cycle = 1.0 - duty_cycle
    period = 1.0 / SWITCHING_FREQUENCY
    on_time = duty_cycle * period
    off_time = (1 - duty_cycle) * period
    iout_max = IOUT_AVG * (1+(IOUT_RIPPLE_RATIO/2))

    t = np.linspace(0, 1, NUM_POINTS)

    square_wave =  ((t * SWITCHING_FREQUENCY % 1) < (duty_cycle)).astype(float)
    v_sw = VIN * square_wave

    triangle_wave = np.mod(t * SWITCHING_FREQUENCY, 1)
    triangle_wave = np.where(
        triangle_wave < duty_cycle,
        2 * triangle_wave / duty_cycle,  # Rising part
        2 * (1 - triangle_wave) / (1 - duty_cycle)  # Falling part
    )
    i_l = (IOUT_RIPPLE_RATIO / 2) * triangle_wave + (IOUT_AVG - (IOUT_RIPPLE_RATIO / 2))

    fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax[0].plot(t, v_sw, label="Switch Node Voltage (V_sw_")
    ax[0].axhline(y=VIN, color='r', linestyle='--', label=f"Input Voltage (V_in)")
    ax[0].axhline(y=VOUT, color='r', linestyle='--', label=f"Output Voltage (V_out)")
    ax[0].set_title(f"{TITLE}")
    ax[0].set_ylim(0, VIN*1.1) 
    ax[0].set_xlabel("Time (sec)")
    ax[0].set_ylabel("Voltage")
    ax[0].legend()

    ax[1].plot(t, i_l, label="Load Current (I_l)")
    ax[1].axhline(y=IOUT_AVG, color='r', linestyle='--', label=f"Average Load Current (I_out_avg)")
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
