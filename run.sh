#!/usr/bin/env bash
# Divinity Music Mod Manager Launcher
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

if [ -d "$DIR/.venv" ]; then
    "$DIR/.venv/bin/python3" "$DIR/app.py" "$@"
else
    python3 "$DIR/app.py" "$@"
fi
