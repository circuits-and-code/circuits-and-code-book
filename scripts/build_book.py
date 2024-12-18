import subprocess
import argparse
import os
import shutil

# Constant for the output directory
OUTPUT_DIR = "output"
MAIN_TEX_PATH = "src/main.tex"


def main():
    # Remove the output directory if it exists, then recreate it
    if os.path.exists(OUTPUT_DIR):
        print(f"Removing existing {OUTPUT_DIR} directory...")
        shutil.rmtree(OUTPUT_DIR)
    print(f"Creating {OUTPUT_DIR} directory...")
    os.makedirs(OUTPUT_DIR)

    # Construct the pdflatex command
    pdflatex_command = f"pdflatex -output-directory={OUTPUT_DIR} {MAIN_TEX_PATH}"

    # Run the pdflatex command and show the output in the console
    print(f"Running command: {pdflatex_command}")
    process = subprocess.Popen(
        pdflatex_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    # Print the output in real-time
    for line in iter(process.stdout.readline, b""):
        print(line.decode().strip())
    process.stdout.close()

    # Wait for the process to finish and check the exit status
    return_code = process.wait()
    if return_code == 0:
        print("PDF successfully compiled!")
    else:
        print("An error occurred during compilation.")
        for line in iter(process.stderr.readline, b""):
            print(line.decode().strip())
        process.stderr.close()


if __name__ == "__main__":
    main()
