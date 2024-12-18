import subprocess
import os
import shutil

# Constants for the output directory and main .tex file
OUTPUT_DIR = "output"
MAIN_TEX_PATH = "main.tex"


def main():
    # Remove the output directory if it exists, then recreate it
    if os.path.exists(OUTPUT_DIR):
        print(f"Removing existing {OUTPUT_DIR} directory...")
        shutil.rmtree(OUTPUT_DIR)
    print(f"Creating {OUTPUT_DIR} directory...")
    os.makedirs(OUTPUT_DIR)
    output_dir = os.path.abspath(OUTPUT_DIR)

    # Construct the latexmk command
    latexmk_command = [
        "latexmk",
        "-pdf",  # Generate PDF using pdflatex
        "-pdflatex=pdflatex",
        "-interaction=nonstopmode",
        "-synctex=1",
        f"-output-directory={output_dir}",
        MAIN_TEX_PATH,
    ]

    os.chdir("src")

    # Run the latexmk command and show the output in the console
    print(f"Running command: {' '.join(latexmk_command)}")
    process = subprocess.Popen(
        latexmk_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # chdir to src
    # Print the output in real-time
    for line in process.stdout:
        print(line.strip())
    process.stdout.close()

    # Wait for the process to finish and check the exit status
    return_code = process.wait()
    if return_code == 0:
        print("PDF successfully compiled!")
    else:
        print("An error occurred during compilation.")
        for line in process.stderr:
            print(line.strip())
        process.stderr.close()


if __name__ == "__main__":
    main()
