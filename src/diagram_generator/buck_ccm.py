
import numpy as np
import matplotlib.pyplot as plt
import argparse

TITLE = "Buck Converter in Continuous Conduction Mode"

def plotter() :
    NUM_POINTS = 1000
    SWITCHING_FREQUENCY = 3 
    VIN = 12
    VOUT = 3.3

    t = np.linspace(0, 1, NUM_POINTS) # time vector

    square_wave = np.sign(np.sin(2 * np.pi * SWITCHING_FREQUENCY * t))
    triangle_wave = 2 * np.abs(2 * (t * SWITCHING_FREQUENCY % 1) - 1) - 1

    v_sw = 5 * square_wave + 0
    i_l = 1 * triangle_wave + 2

    # i_in =
    # v_in = 
    # v_out = 

    plt.figure(figsize=(10, 6))

    plt.plot(t, v_sw, label="V_sw")
    plt.plot(t, i_l, label="I_l")
    # plt.plot(t, )
    # plt.plot(t, )
    # plt.plot(t, )
    plt.axhline(y=VIN, color='r', linestyle='--', label=f"V_in")
    plt.axhline(y=VOUT, color='r', linestyle='--', label=f"V_out")

    plt.title(f"{TITLE}")
    plt.xlabel("Time")
    # plt.ylabel("")
    plt.legend()
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
