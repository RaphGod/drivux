#!/bin/bash
# Drivux installer - OneDrive Linux GUI Manager
# Usage: curl -sSL https://raw.githubusercontent.com/RaphGod/drivux/main/install.sh | bash

set -e

INSTALL_DIR="$HOME/.local/share/drivux"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.config/autostart"
APP_DIR="$HOME/.local/share/applications"
REPO="https://github.com/RaphGod/drivux.git"

echo "==================================="
echo "  Drivux Installer"
echo "  OneDrive Linux GUI Manager"
echo "==================================="
echo ""

# Check dependencies
check_dep() {
    if ! command -v "$1" &>/dev/null; then
        echo "ERROR: $1 is required but not installed."
        echo "Install it with: $2"
        exit 1
    fi
}

check_dep git "sudo apt install git"
check_dep python3 "sudo apt install python3"

# Check python version
PY_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || ([ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 10 ]); then
    echo "ERROR: Python 3.10+ is required (found $PY_VERSION)"
    exit 1
fi
echo "[OK] Python $PY_VERSION"

# Check onedrive
if ! command -v onedrive &>/dev/null; then
    echo "WARNING: onedrive client (abraunegg) not found."
    echo "Drivux requires it to work. Install from:"
    echo "  https://github.com/abraunegg/onedrive"
    echo ""
    read -p "Continue anyway? [y/N] " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "[OK] OneDrive client found"
fi

# Clone or update
if [ -d "$INSTALL_DIR" ]; then
    echo "[..] Updating Drivux..."
    git -C "$INSTALL_DIR" pull --quiet
else
    echo "[..] Downloading Drivux..."
    git clone --quiet "$REPO" "$INSTALL_DIR"
fi
echo "[OK] Source downloaded"

# Create venv and install
echo "[..] Setting up Python environment..."
python3 -m venv "$INSTALL_DIR/.venv"
"$INSTALL_DIR/.venv/bin/pip" install --quiet -e "$INSTALL_DIR"
echo "[OK] Dependencies installed"

# Create bin symlink
mkdir -p "$BIN_DIR"
cat > "$BIN_DIR/drivux" << 'SCRIPT'
#!/bin/bash
exec "$HOME/.local/share/drivux/.venv/bin/python" -m drivux.main "$@"
SCRIPT
chmod +x "$BIN_DIR/drivux"
echo "[OK] Command 'drivux' installed in $BIN_DIR"

# Create .desktop file for app menu
mkdir -p "$APP_DIR"
cat > "$APP_DIR/drivux.desktop" << EOF
[Desktop Entry]
Type=Application
Name=Drivux
Comment=OneDrive sync manager for Linux
Exec=$BIN_DIR/drivux
Icon=cloud-download
Terminal=false
Categories=Utility;Network;FileTools;
Keywords=onedrive;sync;cloud;sharepoint;
StartupNotify=false
EOF
echo "[OK] Desktop entry created"

# Ask about autostart
echo ""
read -p "Start Drivux automatically at login? [Y/n] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    mkdir -p "$DESKTOP_DIR"
    cp "$APP_DIR/drivux.desktop" "$DESKTOP_DIR/drivux.desktop"
    echo "[OK] Autostart enabled"
fi

# Check PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo ""
    echo "NOTE: $BIN_DIR is not in your PATH."
    echo "Add this to your ~/.bashrc or ~/.zshrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

echo ""
echo "==================================="
echo "  Drivux installed successfully!"
echo ""
echo "  Run:  drivux"
echo "  Or find it in your application menu"
echo "==================================="
