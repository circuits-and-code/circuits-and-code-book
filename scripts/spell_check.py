import os
import shutil
import subprocess
import argparse
import language_tool_python
import click
import re
import json

RULE_EXCEPTIONS = [
    "UPPERCASE_SENTENCE_START",
    "WHITESPACE_RULE",
    "TOO_MANY_CONSECUTIVE_SPACES",
]

TEX_FILES_TO_SKIP = [
    "main.tex",
]

LANGUAGE_TOOL = None
CUSTOM_WORDS = set()  # To store words from the custom dictionary


def load_config(json_file):
    global CUSTOM_WORDS
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
            CUSTOM_WORDS = set(data.get("custom_words", []))
            click.secho(f"Loaded {len(CUSTOM_WORDS)} custom words", fg="cyan")
    except FileNotFoundError:
        click.secho(f"Custom words file '{json_file}' not found. Continuing without it.", fg="yellow")


def run_detex(input_file, output_file):
    with open(output_file, "w") as plain_file:
        result = subprocess.run(["detex", input_file], stdout=subprocess.PIPE, check=True, text=True)
        filtered_text = re.sub(r'\[.*?\]|\\.*?{.*?}', '', result.stdout)
        plain_file.write(filtered_text)


def run_spell_check(plain_text, spellcheck_file, print_check):
    global LANGUAGE_TOOL, CUSTOM_WORDS
    matches = LANGUAGE_TOOL.check(plain_text)

    with open(spellcheck_file, "w") as result_file:
        for match in matches:
            if match.ruleId in RULE_EXCEPTIONS:
                continue

            # Skip matches that involve custom words
            if any(custom_word in match.context for custom_word in CUSTOM_WORDS):
                continue

            match_str = str(match)
            match_str_without_suggestions = "\n".join(
                line
                for line in match_str.splitlines()
                if not line.startswith("Suggestion:")
            )
            result_file.write(f"{match_str_without_suggestions}\n")
            if print_check:
                print(match_str_without_suggestions)

    return len([m for m in matches if m.ruleId not in RULE_EXCEPTIONS and not any(custom_word in m.context for custom_word in CUSTOM_WORDS)]) > 0


def process_tex_file(filepath, plaintext_dir, spellcheck_dir, print_check):
    filename = os.path.basename(filepath)
    if filename in TEX_FILES_TO_SKIP:
        click.secho(f"Skipping {filename}", fg="yellow")
        return False

    click.secho(f"Processing {filename}...", fg="blue")
    plain_filepath = os.path.join(plaintext_dir, f"{os.path.splitext(filename)[0]}.txt")
    spellcheck_filepath = os.path.join(
        spellcheck_dir, f"{os.path.splitext(filename)[0]}_result.txt"
    )

    run_detex(filepath, plain_filepath)

    with open(plain_filepath, "r") as plain_file:
        plain_text = plain_file.read()

    has_errors = run_spell_check(plain_text, spellcheck_filepath, print_check)

    if has_errors:
        click.secho(f"Found spelling/grammar mistakes in {filename}", fg="red")
    else:
        click.secho(f"No spelling/grammar mistakes found in {filename}", fg="green")

    return has_errors


def process_tex_files(input_dir, output_dir, print_check):
    plaintext_dir = os.path.join(output_dir, "plaintext")
    spellcheck_dir = os.path.join(output_dir, "spellcheck")
    shutil.rmtree(plaintext_dir, ignore_errors=True)
    shutil.rmtree(spellcheck_dir, ignore_errors=True)
    os.makedirs(plaintext_dir, exist_ok=True)
    os.makedirs(spellcheck_dir, exist_ok=True)

    errors_found = False

    for filename in os.listdir(input_dir):
        if filename.endswith(".tex"):
            filepath = os.path.join(input_dir, filename)
            has_errors = process_tex_file(
                filepath, plaintext_dir, spellcheck_dir, print_check
            )
            if has_errors:
                errors_found = True

    return 1 if errors_found else 0


def main():
    global LANGUAGE_TOOL

    parser = argparse.ArgumentParser(description="LaTeX Spell Checker")
    parser.add_argument(
        "--input_dir",
        default="src",
        help="Directory containing .tex files (default: src)",
    )
    parser.add_argument(
        "--output_dir",
        default="output/plaintext/",
        help="Directory to save outputs (default: output/plaintext/)",
    )
    parser.add_argument(
        "--config",
        default="scripts/spell_check_config.json",
        help="JSON file containing custom words to ignore",
    )
    parser.add_argument(
        "--print_check",
        action="store_true",
        help="Print spell check matches to the console",
    )

    args = parser.parse_args()

    try:
        LANGUAGE_TOOL = language_tool_python.LanguageTool("en-US")
        load_config(args.config)
        retcode = process_tex_files(args.input_dir, args.output_dir, args.print_check)
        exit(retcode)
    finally:
        if LANGUAGE_TOOL:
            LANGUAGE_TOOL.close()


if __name__ == "__main__":
    main()
