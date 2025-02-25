# Circuits & Code Book Source
Circuits and Code offers over 20 interview-style questions and answers designed for embedded software and electrical engineering interns. Written by two authors with experience hiring and mentoring interns for embedded software and electrical engineering roles, it draws on their academic background and industry expertise to focus on the concepts that matter most to interviewers.

## Download
- Official PDF Download Link: https://circuits-and-code.github.io/

## Development Instructions

### Setup (Ubuntu, Non-Docker, VSCode-Style)
- Run WSL
- Setup sshkey
- Clone repo
- Run `code .` in VsCode to open the repo in WSL
- Download `Code Spell Checker` from VSCode Extension Marketplace
- Download `LaTeX Workshop` from VSCode Extension Marketplace
- Use a `venv` environment for this project, `source <VENV_NAME>/bin/activate`
- Run `python3 scripts/setup.py` to install everything required for building

Note: There is a `DOCKERFILE` that can also be used to compile the book (and is used in CI). However, we strongly recommend the above workflow with VSCode for development as it's a lot more interactive, even though it involves installing system packages.

### Building
- Run `python3 scripts/build_book.py`

Note: it's also possible to:
- Open and save `main.tex` to compile the entire directory 
- Open and save `{filename}.tex` to compile an individual file

However, this will not generate images or check code snippets. 

## Internal Tracking Documents
- Initial Notes: https://docs.google.com/document/d/1Akp2vB-8zvOjKRvKKtQ4xRd1HW5HwOgYOPMeZlsEUBo/edit
- Progress Tracking Sheet: https://docs.google.com/spreadsheets/d/1r3ARHjxrXqaiC7ljZWcs_fc2r5LI8fe7ycGm_sgxs3k/edit?gid=0#gid=0
- Internal Splitwise Finance: https://secure.splitwise.com/#/groups/76688172 