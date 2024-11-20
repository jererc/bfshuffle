#!/bin/bash
curl -s "https://raw.githubusercontent.com/jererc/bfshuffle/refs/heads/main/bootstrap/bootstrap.py" | python3
if [ ! -e "user_settings.py" ]; then
    curl -O "https://raw.githubusercontent.com/jererc/bfshuffle/refs/heads/main/bootstrap/user_settings.py"
fi
