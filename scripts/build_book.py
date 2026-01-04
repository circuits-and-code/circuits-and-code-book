import subprocess
import os
import shutil
import click
import check_code_snippets
import argparse
import sys

# Constants
OUTPUT_DIR = "output"
GENERATED_IMAGES_DIR = os.path.abspath("src/generated_images")
IMAGE_GENERATION_COMMANDS = [
    f"python3 src/diagram_generator/rtos_task_diagram.py src/diagram_generator/priority_inversion_input.json --output_path={GENERATED_IMAGES_DIR}/priority_inversion.png",
    f"python3 src/diagram_generator/rtos_task_diagram.py src/diagram_generator/priority_inheritance_input.json --output_path={GENERATED_IMAGES_DIR}/priority_inheritance.png",
    f"python3 src/diagram_generator/pid_discretization_integral.py --output_path={GENERATED_IMAGES_DIR}/pid_discretization_integral.png",
    f"python3 src/diagram_generator/pid_discretization_derivative.py --output_path={GENERATED_IMAGES_DIR}/pid_discretization_derivative.png",
    f"python3 scripts/build_svg_images.py --input-dir=src/images/svg/ --output-dir={GENERATED_IMAGES_DIR}/svg_generated",
    f"python3 src/diagram_generator/buck_ccm.py --output_path={GENERATED_IMAGES_DIR}/buck_ccm.png",
    f"python3 src/diagram_generator/buck_dcm.py --output_path={GENERATED_IMAGES_DIR}/buck_dcm.png",
    f"python3 src/diagram_generator/i2c.py --output_path={GENERATED_IMAGES_DIR}/i2c.png",
    f"python3 src/diagram_generator/i2c_comparison.py --output_path={GENERATED_IMAGES_DIR}/i2c_comparison.png",
    f"python3 src/diagram_generator/step_response_plotter.py --input_file=src/diagram_generator/step_responses.json  --output_path={GENERATED_IMAGES_DIR}",
    f"python3 src/diagram_generator/scope-trigger.py --output_path={GENERATED_IMAGES_DIR}/scope-trigger.png",
    f"python3 src/diagram_generator/hpf_bode_plot.py --output_path={GENERATED_IMAGES_DIR}/hpf_freq_response_plot.png",
    f"python3 src/diagram_generator/ac_dc.py --output_path={GENERATED_IMAGES_DIR}/ac_dc.png",
]


def remove_and_create_dir(directory_path):
    """Remove the directory if it exists, then recreate it."""
    if os.path.exists(directory_path):
        click.secho(f"Removing existing {directory_path} directory...", fg="yellow")
        shutil.rmtree(directory_path)
    os.makedirs(directory_path)


def run_command(command: str) -> None:
    """Run a shell command, stream output live, and raise on failure.

    Fixes UnicodeDecodeError by decoding with a tolerant error handler.
    """
    click.secho(f"Running command: {command}", fg="green")

    # Use the console's encoding if available; otherwise fall back to utf-8.
    encoding = sys.stdout.encoding or "utf-8"

    # Merge stderr into stdout so we stream everything and avoid stderr buffering issues.
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding=encoding,
        errors="replace",  # or "backslashreplace" if you want to see the bytes escaped
        bufsize=1,  # line-buffered (best effort)
        universal_newlines=True,
    )

    assert process.stdout is not None
    try:
        for line in process.stdout:
            # Avoid .strip() eating meaningful whitespace; just drop the trailing newline.
            print(line.rstrip("\n"))
    finally:
        process.stdout.close()

    return_code = process.wait()
    if return_code != 0:
        click.secho(f"Command failed with exit code {return_code}: {command}", fg="red")
        raise RuntimeError(f"Command failed: {command}")


def generate_images():
    """Generate images using predefined commands."""
    remove_and_create_dir(GENERATED_IMAGES_DIR)
    for command in IMAGE_GENERATION_COMMANDS:
        run_command(command)


def execute_latex_build(tex_path):
    """Compile the LaTeX document using latexmk."""
    output_dir = os.path.abspath(OUTPUT_DIR)
    latexmk_command = (
        f"latexmk -pdf -pdflatex=pdflatex -interaction=nonstopmode "
        f"-synctex=1 -output-directory={output_dir} {tex_path}"
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


def main(tex_paths_to_build=None):
    """Main entry point of the script."""
    if tex_paths_to_build is not None:
        remove_and_create_dir(OUTPUT_DIR)
    generate_images()

    if tex_paths_to_build is not None:
        for tex_path in tex_paths_to_build:
            execute_latex_build(tex_path)
    check_code_snippets.check_all_code_snippets()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the book")
    parser.add_argument(
        "--only-gen-images",
        action="store_true",
        help="Only generate images",
        default=False,
    )

    args = parser.parse_args()

    tex_paths = ["main.tex"]

    if args.only_gen_images:
        tex_paths = None

    main(tex_paths)
