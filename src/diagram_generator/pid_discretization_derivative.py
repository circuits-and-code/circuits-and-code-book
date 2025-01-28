import numpy as np
import matplotlib.pyplot as plt
import argparse

NUM_POINTS = 4


def plot_sine_and_derivative_comparison(NUM_POINTS=20):
    # Time range
    T_start = 0.0 * np.pi
    T_end = 1.0 * np.pi 
    dt = T_end / NUM_POINTS  # Time step based on the number of points
    t = np.linspace(T_start, T_end, 1000)  # Continuous time for the sine wave

    # Continuous sine wave and its derivative
    y_cont = np.sin(t)
    dy_cont = np.cos(t)

    # Discretized points for sine wave
    t_discrete = np.linspace(T_start, T_end, NUM_POINTS + 1)
    y_discrete = np.sin(t_discrete)

    # Compute backward Euler derivative
    dy_discrete = np.diff(y_discrete) / dt  # Discretized derivative approximation
    t_derivative = t_discrete[:-1]  # Time points for the derivative (one less)

    # Create subplots
    fig, axes = plt.subplots(2, 1, figsize=(10, 6))

    # Plot continuous sine wave and backward Euler approximation
    axes[0].plot(t, y_cont, color="black", label="Continuous Function")
    for i in range(1, NUM_POINTS + 1):
        # Plot backward Euler approximation
        axes[0].plot(
            [t_discrete[i - 1], t_discrete[i]],
            [y_discrete[i - 1], y_discrete[i]],
            color="magenta",
            linestyle="-",
            linewidth=2,
            zorder=5,
        )
        axes[0].scatter(
            [t_discrete[i - 1], t_discrete[i]],
            [y_discrete[i - 1], y_discrete[i]],
            color="magenta",
            zorder=6,
        )

        # Calculate rise and run
        rise = y_discrete[i] - y_discrete[i - 1]
        run = t_discrete[i] - t_discrete[i - 1]

        # Offset for arrows (small margin)
        arrow_offset = 0.0

        # Plot rise marker
        axes[0].arrow(
            t_discrete[i] + arrow_offset,
            y_discrete[i - 1],  # Offset arrow slightly
            0,
            rise,  # Delta for the arrow
            color="green",
            alpha=0.7,
            head_width=0.03,
            head_length=0.05,
            width=0.005,
            length_includes_head=True,
            zorder=4,
        )

        # Plot run marker
        axes[0].arrow(
            t_discrete[i - 1],
            y_discrete[i - 1] - arrow_offset,  # Offset arrow slightly
            run,
            0,  # Delta for the arrow
            color="blue",
            alpha=0.7,
            head_width=0.03,
            head_length=0.05,
            width=0.005,
            length_includes_head=True,
            zorder=4,
        )
    axes[0].plot([], [], color="magenta", linewidth=2, label="Discretized Function")
    axes[0].plot([], [], color="green", label="Rise")
    axes[0].plot([], [], color="blue", label="Run")
    axes[0].scatter(
        t_discrete, y_discrete, color="red", zorder=7, label="Discrete Points"
    )
    axes[0].set_title("Sine Wave with Backward Derivative Approximation")
    axes[0].set_xlabel("Time (t)")
    axes[0].set_ylabel("Value")
    axes[0].legend()
    axes[0].grid(True)

    # Plot actual derivative and discretized derivative
    axes[1].plot(t, dy_cont, color="black", label="Continuous Derivative")
    axes[1].scatter(
        t_derivative,
        dy_discrete,
        color="magenta",
        label="Discretized Derivative",
        zorder=5,
    )
    axes[1].plot(t_derivative, dy_discrete, color="magenta", linestyle="--", zorder=5)
    axes[1].set_title("Derivative Comparison")
    axes[1].set_xlabel("Time (t)")
    axes[1].set_ylabel("Derivative")
    axes[1].legend()
    axes[1].grid(True)

    # Adjust layout
    plt.tight_layout()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("PID Discretization Plotter")
    parser.add_argument("--output_path", help="Path to save image to")

    args = parser.parse_args()

    plot_sine_and_derivative_comparison(NUM_POINTS)

    if args.output_path is not None:
        plt.savefig(args.output_path)
    else:
        plt.show()
