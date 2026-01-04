import numpy as np
import matplotlib.pyplot as plt
import argparse

# fmt: off

TITLE = "AC vs. DC Coupling"

def plotter() :

    NUM_PTS = 5000
    t = np.linspace(0, 1, NUM_PTS)
    YLIM_SCALE = 1.2

    FREQ = 5
    OFFSET = 2
    AMPLITUDE = 1

    ac = AMPLITUDE * np.sin(2 * np.pi * FREQ * t)
    full = ac + OFFSET

    fig, ax = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax[0].plot(t, full, label="DC Coupled")
    ax[0].axhline(y=OFFSET, color='r', linestyle='--', label=f"DC Component")
    ax[0].set_title(f"{TITLE}")
    ax[0].set_ylim(0, (AMPLITUDE+OFFSET)*YLIM_SCALE) 
    ax[0].set_xlabel("Time (seconds)")
    ax[0].set_ylabel("Voltage (volts)")
    ax[0].legend()

    ax[1].plot(t, ac, label="AC Coupled")
    ax[1].set_ylim(-AMPLITUDE*YLIM_SCALE, AMPLITUDE*YLIM_SCALE) 
    ax[1].set_xlabel("Time (seconds)")
    ax[1].set_ylabel("Voltage (volts)")
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
