import numpy as np
import matplotlib.pyplot as plt
import argparse
import control
import json


def plotter(t, y, title, y_labels: list, input_signal_label, output_signal_label):

    plt.figure(figsize=(10, 6))

    t_input = np.linspace(-1, t[-1], 1000)
    v_input = [1 if i >= 0 else 0 for i in t_input]

    # Plot input signal on primary y-axis
    ax1 = plt.gca()  # Primary axis
    (input_line,) = ax1.plot(t_input, v_input, label=input_signal_label, color="blue")
    ax1.set_xlabel("Time (s)")

    ax1_color = "black"

    # Check if a second y-axis is needed
    if len(y_labels) == 2:
        # Plot output signal on secondary y-axis
        ax2 = ax1.twinx()  # Secondary axis
        (output_line,) = ax2.plot(t, y, label=output_signal_label, color="orange")
        ax2.set_ylabel(y_labels[1], color="orange")
        ax2.tick_params(axis="y", labelcolor="orange")

        ax1_color = "blue"
    else:
        # Plot output signal on primary y-axis if only one label
        (output_line,) = ax1.plot(t, y, label=output_signal_label, color="orange")

    ax1.set_ylabel(y_labels[0], color=ax1_color)
    ax1.tick_params(axis="y", labelcolor=ax1_color)

    # Combine legends from both axes
    lines = [input_line, output_line]
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels)

    plt.title(title)
    plt.grid(True)


def get_step_response(numerator, denominator):
    sys = control.TransferFunction(numerator, denominator)
    t, y = control.step_response(sys)
    return t, y


if __name__ == "__main__":
    parser = argparse.ArgumentParser(f"Step Response Plotter")
    parser.add_argument(
        "--input_file",
        help="Path to input file to use for image generation",
        required=True,
    )
    parser.add_argument(
        "--display_plot", help="Displays the selected plot key"
    )  # ex: --display_plot=low_pass_filter
    parser.add_argument("--output_path", help="Directory to save images to")

    args = parser.parse_args()

    # Load the input file
    with open(args.input_file) as f:
        data = json.load(f)

    for key in data:
        plt.close("all")
        plt.rcdefaults()

        # coefficients are in descending order, ex: [2, 3, 4] -> 2s^2 + 3s + 4
        numerator = data[key]["numerator"]
        denominator = data[key]["denominator"]
        title = data[key]["title"]
        y_labels = data[key]["y_label"]
        input_signal_label = data[key]["input_signal_label"]
        output_signal_label = data[key]["output_signal_label"]

        t, y = get_step_response(numerator, denominator)

        plotter(t, y, title, y_labels, input_signal_label, output_signal_label)

        if args.output_path is not None:
            image_path = f"{args.output_path}/{key}.png"
            plt.savefig(image_path)
        elif (key == args.display_plot) or (args.display_plot is None):
            plt.show()
        elif args.display_plot is not None:
            print(f"Skipping display for {key}")
