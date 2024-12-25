CODE_SNIPPET_PATHS = [
    "src/code/pid",
    "src/code/bitbang_spi",
    "src/code/bitstream_parity",
    "src/code/keyword",
    "src/code/adc_init",
    "src/code/packet_parsing",
    "src/code/timer",
    "src/code/stack",
    "src/code/stack/stack_ex",
]

RUNNABLE_PATHS = [
    "src/code/packet_parsing/build",
    "src/code/stack/build",
    "src/code/stack/stack_ex/build",
]

import subprocess
import shutil
import os
import click
import argparse


def check_code_snippet(wd_path):
    CMD = [
        "rm -rf build",
        "mkdir -p build",
        "cd build && cmake ..",  # Combine cd and cmake for clarity
        "cd build && make",
    ]

    for command in CMD:
        result = subprocess.run(
            command,
            shell=True,
            check=False,  # Allow handling of return code manually
            cwd=wd_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode != 0:
            click.secho(f"Error executing: '{command}' in {wd_path}", fg="red")
            click.secho(result.stderr.decode(), fg="red")
            return False  # Stop execution on failure

    return True


def run_code_snippet(wd_path):
    # extract the name of the executable
    executable = wd_path.split("/")[-1]

    CMD = [f"./test_app"]

    for command in CMD:
        click.secho(f"Running: {command} in {wd_path}", fg="blue")
        result = subprocess.run(
            command,
            shell=True,
            check=False,  # Allow handling of return code manually
            cwd=wd_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode != 0:
            click.secho(f"Error executing: '{command}' in {wd_path}", fg="red")
            click.secho(result.stderr.decode(), fg="red")
            return False
        elif result.stdout:
            click.secho(result.stdout.decode(), fg="cyan")

    return True


def check_all_code_snippets():
    for path in CODE_SNIPPET_PATHS:
        path = os.path.abspath(path)
        if not check_code_snippet(path):
            raise RuntimeError(f"Error in running code snippet in {path}")
        else:
            click.secho(f"Code snippet in {path} is working correctly!", fg="green")

    for path in RUNNABLE_PATHS:
        path = os.path.abspath(path)
        if not run_code_snippet(path):
            raise RuntimeError(f"Error in running code snippet in {path}")
        else:
            click.secho(f"Run snippet in {path} is working correctly!", fg="green")


if __name__ == "__main__":
    check_all_code_snippets()
