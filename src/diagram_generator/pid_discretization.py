import numpy as np
import matplotlib.pyplot as plt
import argparse

NUM_POINTS = 10


def plot_sine_backward_derivative_and_sum(NUM_POINTS=20):
    # Time range
    T = 2 * np.pi  # One full sine wave period
    dt = T / NUM_POINTS  # Time step based on the number of points
    t = np.linspace(0, T, 1000)  # Continuous time for the sine wave

    # Continuous sine wave
    y_cont = np.sin(t)

    # Discretized points for sine wave
    t_discrete = np.linspace(0, T, NUM_POINTS + 1)
    y_discrete = np.sin(t_discrete)

    # Plotting
    plt.figure(figsize=(10, 6))

    # Continuous sine wave
    plt.plot(t, y_cont, color="black", label="Continuous Function")

    # Backward Euler Derivative Lines
    for i in range(1, NUM_POINTS + 1):
        plt.plot(
            [t_discrete[i - 1], t_discrete[i]],
            [y_discrete[i - 1], y_discrete[i]],
            color="magenta",
            linestyle="-",
            linewidth=2,
            zorder=5,
        )
        plt.scatter(
            [t_discrete[i - 1], t_discrete[i]],
            [y_discrete[i - 1], y_discrete[i]],
            color="magenta",
            zorder=5,
        )
    plt.plot(
        [], [], color="magenta", linewidth=2, label="Backward Euler (Derivative)"
    )  # Legend entry

    # Right-Hand Riemann Sum Rectangles
    for i in range(1, NUM_POINTS + 1):
        plt.plot(
            [t_discrete[i], t_discrete[i]],
            [0, y_discrete[i]],
            color="yellow",
            linewidth=2,
            zorder=4,
        )
        plt.plot(
            [t_discrete[i - 1], t_discrete[i]],
            [y_discrete[i], y_discrete[i]],
            color="yellow",
            linewidth=2,
            zorder=4,
        )
        plt.plot(
            [t_discrete[i - 1], t_discrete[i - 1]],
            [0, y_discrete[i]],
            color="yellow",
            linewidth=2,
            zorder=4,
        )
    plt.plot(
        [], [], color="yellow", linewidth=2, label="Backward Euler (Sum)"
    )  # Legend entry

    # Discrete points
    plt.scatter(t_discrete, y_discrete, color="cyan", zorder=6, label="Discrete Points")

    # Labels and styling
    plt.title(
        "Sine Wave with Raw Backward Derivative and Backward Euler Sum Calculations"
    )
    plt.xlabel("Time (t)")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("PID Discretization Plotter")
    parser.add_argument("--output_path", help="Path to save image to")

    args = parser.parse_args()

    plot_sine_backward_derivative_and_sum(NUM_POINTS)

    if args.output_path is not None:
        plt.savefig(args.output_path)
    else:
        plt.show()
