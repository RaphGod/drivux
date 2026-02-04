# Drivux

GUI manager for the [OneDrive Linux client](https://github.com/abraunegg/onedrive).

System tray application to monitor, configure and control OneDrive sync services on Linux.

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
![Qt](https://img.shields.io/badge/Qt-PySide6-41cd52)

## Features

- **System tray icon** with live sync status (OK / error / syncing)
- **Service management**: start, stop, restart OneDrive services
- **Live log viewer** with color coding and filtering
- **Configuration editor**: edit OneDrive config files from the GUI
- **Multi-instance support**: manages multiple OneDrive/SharePoint libraries
- **Desktop notifications** on sync errors
- **KDE/GNOME/XFCE compatible** (Qt6-based)

## Requirements

- Linux with systemd
- [abraunegg/onedrive](https://github.com/abraunegg/onedrive) installed and configured as systemd user services
- Python 3.10+
- PySide6

## Installation

```bash
git clone https://github.com/rapmusic/drivux.git
cd drivux
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage

```bash
# Run from venv
source .venv/bin/activate
drivux
```

Or run directly:

```bash
.venv/bin/python -m drivux.main
```

### Autostart

To start Drivux automatically at login, create a desktop entry:

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/drivux.desktop << EOF
[Desktop Entry]
Type=Application
Name=Drivux
Exec=/path/to/drivux/.venv/bin/drivux
Icon=cloud
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF
```

## How it works

Drivux interacts with OneDrive through:
- `systemctl --user` to manage services
- `journalctl --user` to stream logs in real-time
- Direct config file editing (`~/.config/onedrive*/config`)

It does **not** replace or modify the OneDrive client itself.

## License

MIT
