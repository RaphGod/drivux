"""Read and write OneDrive configuration files."""

from pathlib import Path

# Known config keys with descriptions
CONFIG_KEYS = {
    "sync_dir": "Local directory to sync",
    "drive_id": "SharePoint/OneDrive Drive ID",
    "use_device_auth": "Use device authentication flow",
    "disable_notifications": "Disable desktop notifications",
    "classify_as_big_delete": "Threshold for big delete protection",
    "skip_dir": "Directories to skip (regex)",
    "skip_file": "Files to skip (regex)",
    "skip_dotfiles": "Skip dotfiles",
    "skip_symlinks": "Skip symbolic links",
    "monitor_interval": "Sync interval in seconds (monitor mode)",
    "monitor_fullscan_frequency": "Full scan frequency (number of syncs)",
    "download_only": "Only download, never upload",
    "upload_only": "Only upload, never download",
    "no_remote_delete": "Don't delete remote files",
    "check_nosync": "Check for .nosync files",
    "log_level": "Log verbosity (v, vv, vvv)",
    "rate_limit": "Bandwidth limit in bytes/s",
}


class ConfigManager:
    """Read/write onedrive config files."""

    def __init__(self, config_path: Path):
        self.path = config_path

    def read(self) -> dict[str, str]:
        """Parse config file into key-value dict."""
        config = {}
        if not self.path.exists():
            return config
        for line in self.path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip().strip('"')
        return config

    def write(self, config: dict[str, str]) -> None:
        """Write config dict back to file, preserving comments."""
        lines = []
        if self.path.exists():
            existing = self.path.read_text().splitlines()
        else:
            existing = []

        written_keys = set()
        for line in existing:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                lines.append(line)
                continue
            if "=" in stripped:
                key = stripped.split("=", 1)[0].strip()
                if key in config:
                    lines.append(f'{key} = "{config[key]}"')
                    written_keys.add(key)
                # Skip keys removed from config
                continue
            lines.append(line)

        # Add new keys
        for key, value in config.items():
            if key not in written_keys:
                lines.append(f'{key} = "{value}"')

        self.path.write_text("\n".join(lines) + "\n")

    def get(self, key: str, default: str = "") -> str:
        config = self.read()
        return config.get(key, default)

    def set(self, key: str, value: str) -> None:
        config = self.read()
        config[key] = value
        self.write(config)

    def remove(self, key: str) -> None:
        config = self.read()
        config.pop(key, None)
        self.write(config)
