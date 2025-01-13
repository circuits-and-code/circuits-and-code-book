
import numpy as np
import matplotlib.pyplot as plt
import argparse

TITLE = "Unknown Plot Title"

def plotter():

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
