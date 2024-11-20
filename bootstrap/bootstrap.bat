@echo off
curl -s "https://raw.githubusercontent.com/jererc/bfshuffle/refs/heads/main/bootstrap/bootstrap.py" | python
if not exist "user_settings.py" (
    curl -O "https://raw.githubusercontent.com/jererc/bfshuffle/refs/heads/main/bootstrap/user_settings.py"
)
