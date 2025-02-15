# Circuits & Code Book Source
Circuits and Code offers over 20 interview-style questions and answers designed for embedded software and electrical engineering interns. Written by two authors with experience hiring and mentoring interns for embedded software and electrical engineering roles, it draws on their academic background and industry expertise to focus on the concepts that matter most to interviewers.

## Download
- Official PDF Download Link: https://circuits-and-code.github.io/

### Internal Tracking Documents
- Initial Notes: https://docs.google.com/document/d/1Akp2vB-8zvOjKRvKKtQ4xRd1HW5HwOgYOPMeZlsEUBo/edit
- Progress Tracking Sheet: https://docs.google.com/spreadsheets/d/1r3ARHjxrXqaiC7ljZWcs_fc2r5LI8fe7ycGm_sgxs3k/edit?gid=0#gid=0
- Internal Splitwise Finance: https://secure.splitwise.com/#/groups/76688172 

## Development Instructions

### CLI Approach:
- Run `python3 scripts/build_book.py`

### Latex Extension Approach:
- Download `Code Spell Checker` from VSCode Extension Marketplace
- Download `LaTeX Workshop` from VSCode Extension Marketplace
- Open and save `main.tex` to compile the entire directory 
- Open and save `{filename}.tex` to compile an individual file

### Windows Approach:
- Install VSCode
- Install Python
- Install MikTex
- Install Perl
- Restart your computer
- Install latexmk from MikTex console
- Install `Code Spell Checker` from VSCode Extension Marketplace
- Install `LaTeX Workshop` from VSCode Extension Marketplace
- Install `scripts/python_requirements.txt`
- Ensure "python3" is in PATH and works
- Install GTK gvsbuild for use with CairoSVG and add it to PATH to build svg images (required for building the book now)
- Restart computer 
- Run `scripts/build_book.py` script to build
- Use the build button in VSCode on `main.tex` to compile the entire directory 

## WSL Approach:
- Run WSL
- Setup sshkey
- Clone repo
- Run `code .` in VsCode to open the repo in WSL
- Install latex workshop for wsl
- Install python `venv` if this isn't already done (it might be in later versions of wsl)
- Use a `venv` environment for this project, `source name/bin/activate`
- Run `scripts/setup.py` to install everything required for building 
