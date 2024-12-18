import subprocess
import os
import shutil
import click

# Constants
OUTPUT_DIR = "output"
MAIN_TEX_PATH = "main.tex"
GENERATED_IMAGES_DIR = os.path.abspath("src/generated_images")
IMAGE_GENERATION_COMMANDS = [
    f"python3 src/diagram_generator/rtos_task_diagram.py src/diagram_generator/priority_inversion_input.json --output_path={GENERATED_IMAGES_DIR}/priority_inversion.png",
    f"python3 src/diagram_generator/rtos_task_diagram.py src/diagram_generator/priority_inheritance_input.json --output_path={GENERATED_IMAGES_DIR}/priority_inheritance.png",
]


def remove_and_create_dir(directory_path):
    """Remove the directory if it exists, then recreate it."""
    if os.path.exists(directory_path):
        click.secho(f"Removing existing {directory_path} directory...", fg="yellow")
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)


def run_command(command):
    """Run a shell command and handle its output."""
    click.secho(f"Running command: {command}", fg="green")
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # Print stdout in real-time
    for line in process.stdout:
        print(line.strip())
    process.stdout.close()

    # Wait for process to finish and handle errors
    return_code = process.wait()
    if return_code != 0:
        click.secho("An error occurred:", fg="red")
        for line in process.stderr:
            print(line.strip())
        raise RuntimeError("Command failed: {}".format(command))


def generate_images():
    """Generate images using predefined commands."""
    remove_and_create_dir(GENERATED_IMAGES_DIR)
    for command in IMAGE_GENERATION_COMMANDS:
        run_command(command)


def execute_latex_build():
    """Compile the LaTeX document using latexmk."""
    remove_and_create_dir(OUTPUT_DIR)
    output_dir = os.path.abspath(OUTPUT_DIR)

    latexmk_command = (
        f"latexmk -pdf -pdflatex=pdflatex -interaction=nonstopmode "
        f"-synctex=1 -output-directory={output_dir} {MAIN_TEX_PATH}"
    )

    os.chdir("src")  # Change to the source directory
    try:
        run_command(latexmk_command)
        click.secho("PDF successfully compiled!", fg="green")
    except RuntimeError:
        click.secho("Failed to compile PDF.", fg="red")
        raise
    finally:
        os.chdir("..")  # Return to the original directory


def main():
    """Main entry point of the script."""
    generate_images()
    execute_latex_build()


if __name__ == "__main__":
    main()
