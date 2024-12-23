CODE_SNIPPET_PATHS = [
    "src/code/pid",
    "src/code/bitbang_spi",
    "src/code/bitstream_parity",
    "src/code/keyword",
    "src/code/adc_init",
]

import subprocess
import shutil
import os
import click


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


def check_all_code_snippets():
    for path in CODE_SNIPPET_PATHS:
        path = os.path.abspath(path)
        if not check_code_snippet(path):
            raise RuntimeError(f"Error in running code snippet in {path}")
        else:
            click.secho(f"Code snippet in {path} is working correctly!", fg="green")


if __name__ == "__main__":
    check_all_code_snippets()
