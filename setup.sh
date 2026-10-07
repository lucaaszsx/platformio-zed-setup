#!/usr/bin/env bash
set -euo pipefail

PACKAGE_REPOSITORY="git+https://github.com/lucaaszsx/platformio-zed-setup.git@main"

if ! command -v curl >/dev/null 2>&1; then
    echo "curl not found, install with: pacman -S curl"
    exit 1
fi

if ! command -v uv >/dev/null 2>&1; then
    echo "uv not found, installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "Installing from \"$PACKAGE_REPOSITORY\"..."
uv tool install --force "$PACKAGE_REPOSITORY"

echo "Running setup..."
zedio setup

echo "Done."
