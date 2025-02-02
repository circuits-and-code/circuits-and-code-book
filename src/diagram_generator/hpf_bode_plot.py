import numpy as np
import matplotlib.pyplot as plt
import argparse
import control

TITLE = "Frequency vs Gain of High Pass Filter"


def plotter():
    w0 = 1
    sys = control.TransferFunction([1 / w0, 0], [1 / w0, 1])
    mag, phase, omega = control.frequency_response(sys, Hz=True)

    plt.figure(figsize=(10, 6))

    # only plot the magnitude plot
    plt.semilogx(omega, mag, label="Vout/Vin Gain of HPF")

    plt.title(f"{TITLE}")
    plt.xlabel("")
    plt.ylabel("")
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
