#!/bin/bash
# Drivux uninstaller

set -e

INSTALL_DIR="$HOME/.local/share/drivux"
BIN_DIR="$HOME/.local/bin"

echo "Uninstalling Drivux..."

# Kill running instance
pkill -f "drivux.main" 2>/dev/null || true

# Remove files
rm -f "$BIN_DIR/drivux"
rm -f "$HOME/.local/share/applications/drivux.desktop"
rm -f "$HOME/.config/autostart/drivux.desktop"
rm -rf "$INSTALL_DIR"

echo "Drivux has been uninstalled."
