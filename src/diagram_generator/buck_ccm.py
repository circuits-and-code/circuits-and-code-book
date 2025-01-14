import numpy as np
import matplotlib.pyplot as plt
import argparse

# fmt: off

TITLE = "Buck Converter in Continuous Conduction Mode"

def plotter() :
    NUM_POINTS = 1000
    SWITCHING_FREQUENCY = 3 
    VIN = 12.0
    VOUT = 3.3

    duty_cycle = VOUT / VIN
    negative_duty_cycle = 1.0 - duty_cycle
    period = 1.0 / SWITCHING_FREQUENCY
    on_time = duty_cycle * period
    off_time = (1 - duty_cycle) * period

    t = np.linspace(0, 1, NUM_POINTS) # time vector

    square_wave =  ((t * SWITCHING_FREQUENCY % 1) < (duty_cycle)).astype(float)
    v_sw = VIN * square_wave + 0

    triangle_wave = np.mod(t * SWITCHING_FREQUENCY, 1)
    triangle_wave = np.where(
        triangle_wave < duty_cycle,
        2 * triangle_wave / duty_cycle,  # Rising part
        2 * (1 - triangle_wave) / (1 - duty_cycle)  # Falling part
    )
    i_l = 1 * triangle_wave + 4

    plt.figure(figsize=(10, 6))

    plt.plot(t, v_sw, label="V_sw")
    plt.plot(t, i_l, label="I_l")
    # plt.plot(t, ) # i_in
    plt.axhline(y=VIN, color='r', linestyle='--', label=f"V_in")
    plt.axhline(y=VOUT, color='r', linestyle='--', label=f"V_out")

    plt.title(f"{TITLE}")
    plt.gca().axes.get_xaxis().set_visible(False)
    plt.xlabel("Time")
    # plt.ylabel("")
    # plt.legend()
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True)

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
