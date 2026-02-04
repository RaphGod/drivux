<p align="center">
  <img src="docs/screenshot.png" alt="Drivux Screenshot" width="700"/>
</p>

<h1 align="center">Drivux</h1>

<p align="center">
  <strong>GUI manager for the <a href="https://github.com/abraunegg/onedrive">OneDrive Linux client</a></strong><br>
  Monitor, configure and control OneDrive sync services from your system tray.
</p>

<p align="center">
  <a href="https://github.com/RaphGod/drivux/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.10+-green" alt="Python">
  <img src="https://img.shields.io/badge/Qt6-PySide6-41cd52" alt="Qt">
  <img src="https://img.shields.io/badge/desktop-KDE%20%7C%20GNOME%20%7C%20XFCE-blue" alt="Desktop">
</p>

<p align="center">
  <a href="README.md">English</a> | <a href="docs/README_FR.md">Fran&ccedil;ais</a>
</p>

---

## Why Drivux?

The [abraunegg/onedrive](https://github.com/abraunegg/onedrive) client for Linux is powerful but has no graphical interface. Managing multiple OneDrive/SharePoint libraries means juggling config files, systemctl commands and journalctl logs manually.

**Drivux** provides a simple system tray GUI that brings it all together:

- See at a glance if your sync is healthy or broken
- Read live logs without touching the terminal
- Edit config files without a text editor
- Start, stop or restart services with one click

## Features

| Feature | Description |
|---------|------------|
| **System tray icon** | Changes color based on sync status (green = OK, red = error, orange = syncing) |
| **Service dashboard** | Overview of all OneDrive instances with status, PID, sync directory |
| **Live log viewer** | Real-time colored logs with per-service filtering |
| **Config editor** | Edit any OneDrive config parameter from the GUI |
| **Service controls** | Start / stop / restart individual or all services |
| **Multi-instance** | Manages multiple OneDrive and SharePoint libraries simultaneously |
| **Desktop notifications** | Get notified on sync errors (DNS failures, big deletes, etc.) |

## Requirements

- Linux with **systemd**
- [abraunegg/onedrive](https://github.com/abraunegg/onedrive) installed and running as **systemd user services**
- Python 3.10+

## Quick start

```bash
git clone https://github.com/RaphGod/drivux.git
cd drivux
python -m venv .venv
source .venv/bin/activate
pip install -e .
drivux
```

## Autostart at login

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/drivux.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Drivux
Comment=OneDrive sync manager
Exec=/path/to/drivux/.venv/bin/drivux
Icon=cloud
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF
```

Replace `/path/to/drivux` with your actual install path.

## How it works

Drivux is a **read/control layer** on top of the existing OneDrive client. It does **not** replace or modify the client itself.

```
Drivux (GUI)
    |
    +-- systemctl --user    --> manage services
    +-- journalctl --user   --> stream live logs
    +-- ~/.config/onedrive* --> read/write config files
    |
OneDrive client (abraunegg)
    |
Microsoft OneDrive / SharePoint
```

## Contributing

Contributions are welcome! Feel free to open issues or pull requests.

## License

[MIT](LICENSE)
