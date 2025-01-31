import numpy as np
import matplotlib.pyplot as plt
import argparse

TITLE = "I2C SCL with Varying Pullup Resistance"

def plotter() :
    kilo = 1e3
    pico = 1e-12

    freq = 400 * kilo
    v_ll = 3.3

    tau = 2.2 * kilo * 47 * pico 
    tau_higher = 4.7 * kilo * 47 * pico
    tau_lower = 470 * 47 * pico

    period = 1.0 / float(freq)
    half_period = period / 2 

    number_of_plotted_points = 5000
    cycles_shown = 3
    t = np.linspace(0, cycles_shown * period, number_of_plotted_points) 

    scl = np.zeros_like(t)
    scl_higher = np.zeros_like(t)
    scl_lower = np.zeros_like(t)
    for i, t_i in enumerate(t):
        cycle_pos = t_i % period  # Time within each cycle
        if cycle_pos < half_period :
            scl[i] = 0
            scl_higher[i] = 0
            scl_lower[i] = 0
        else :
            scl[i] = v_ll * (1 - np.exp((-1* (cycle_pos-half_period))/tau))
            scl_higher[i] = v_ll * (1 - np.exp((-1* (cycle_pos-half_period))/tau_higher))
            scl_lower[i] = v_ll * (1 - np.exp((-1* (cycle_pos-half_period))/tau_lower))

    plt.figure(figsize=(10, 6))
    plt.title(f"{TITLE}")
    plt.plot(t, scl, label="SCL Nominal")
    plt.plot(t, scl_higher, label="SCL with Increased Pullup Value")
    plt.plot(t, scl_lower, label="SCL with Decfeased Pullup Value")
    plt.xlabel("Time (sec)")
    # plt.xlim(0, number_of_plotted_points)
    plt.ylabel("Voltage (V)")
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
