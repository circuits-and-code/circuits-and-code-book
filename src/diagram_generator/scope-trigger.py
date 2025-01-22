import numpy as np
import matplotlib.pyplot as plt
import argparse

TITLE = "Scope Triggering Waveform"


def plotter():
    plt.figure(figsize=(16, 11))

    num_sin_wave_completions = 3

    trigger_time_offset_rad = 1 / 6 * np.pi

    t = np.linspace(-3 / 4 * np.pi, 2 * np.pi * num_sin_wave_completions, num=1000)

    # create 2 subplots, one for showing un-triggered waveform (bunch of sincewaves and messy), and one for triggered waveform
    plt.subplot(2, 1, 1)

    num_overlapping_waves = 6
    for i in range(num_overlapping_waves):
        phase_delay_const_rad = i * np.pi / 6
        sin_wave = np.sin(t + phase_delay_const_rad + trigger_time_offset_rad)
        plt.plot(t, sin_wave)

    plt.xlabel("Time (us)")
    plt.ylabel("Amplitude")
    plt.title("Un-triggered Waveform (Measurements Appear Overlapping)")
    plt.grid()

    plt.subplot(2, 1, 2)
    sin_wave = np.sin(t + trigger_time_offset_rad)
    plt.plot(t, sin_wave, label="Actual Waveform (Triggered)")

    # draw trigger line
    trigger_value = np.sin(trigger_time_offset_rad)
    plt.axhline(
        y=trigger_value, color="r", linestyle="--", label="Trigger Value (Rising Edge)"
    )

    # draw trigger time at 0.0s
    plt.axvline(x=0.0, color="purple", linestyle="--", label="Trigger Time")

    # draw a circle at the trigger valye and trigger time
    plt.plot(0.0, trigger_value, "ro")

    plt.xlabel("Time (us)")
    plt.ylabel("Amplitude")
    plt.title("Triggered Waveform")
    plt.grid()
    plt.legend()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(f"{TITLE} Plotter")
    parser.add_argument("--output_path", help="Path to save image to")

    args = parser.parse_args()

    plotter()

    if args.output_path is not None:
        plt.savefig(args.output_path)
    else:
        plt.show()
