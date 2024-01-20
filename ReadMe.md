# Royal Caribbean Timezone DB Assessment

This repo is my assessment for a position as a Full Stack Software Engineer at Royal Caribbean. The PDF for the assessment is available [here](./Assessment.pdf)

## Requirements

Python 3.7+ should work, however here are the below versions I used:

- python 3.11.6 [python](https://www.python.org/downloads/release/python-3116/)
- pip 23.3.1 [pip](https://pip.pypa.io/en/stable/)

## Setting up the environment

Normally the `.env` file is omitted from the repository to ensure API keys are hidden. For the purpose of making the assessment easy to run, I've left the `.env` file with the API key inside.

Ensure to run the correct command depending on your OS.

### Linux
```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

### Windows
```bash
python -m venv venv
./venv/bin/activate
pip install -r requirements.txt
```

# How to run
```bash
python main.py
```