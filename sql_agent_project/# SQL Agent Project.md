# SQL Agent Project

Minimal instructions to install dependencies in a virtual environment and run the project.

Prerequisites
- Python 3.10+ installed

Setup

1. Create and activate a virtual environment
```sh
# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1

# Windows (cmd)
python -m venv .venv
.\\.venv\\Scripts\\activate.bat
```

2. Upgrade pip and install dependencies
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

3. Run the project
```sh
python main.py
```

Notes
- Entry script: [main.py](main.py) which uses [`generate_query`](main.py), [`execute_query`](main.py) and calls [`app.invoke`](main.py).
- Dependencies are listed in [requirements.txt](requirements.txt).