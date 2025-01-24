import numpy as np
import matplotlib.pyplot as plt
import argparse
from math import sqrt

# fmt: off

TITLE = "Buck Converter in Discontinuous Conduction Mode"

def plotter() :
    NUM_POINTS = 1000
    SWITCHING_FREQUENCY = 3 # number of switching cycles to show 
    VIN = 12.0 # aligns with buck_ccm.py so plots will look nice when placed side by side 
    VOUT = 3.3
    assert VIN > VOUT # just cuz it'll kill my formulas otherwise 
    IOUT_AVG = 10 * 10 **-3 # 10mA is low enough to be reasonable for DCM for most bucks, especially this high step down ratio

    t = np.linspace(0, 1, NUM_POINTS)

    # D = (Vout / Vin) * sqrt(2 * L * f / (R * (Vin - Vout))) 
    duty_cycle = 0.2
    square_wave =  ((t * SWITCHING_FREQUENCY % 1) < (duty_cycle)).astype(float)
    v_sw = VIN * square_wave

    # Draw !

    plt.figure(figsize=(10, 6))

    # Draw !

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

# fmt: on
