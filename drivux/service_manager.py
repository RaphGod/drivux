"""Manage OneDrive systemd user services."""

import subprocess
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ServiceStatus:
    name: str
    display_name: str
    active: bool = False
    status_text: str = "unknown"
    confdir: Path = field(default_factory=lambda: Path())
    sync_dir: str = ""
    pid: int = 0


class ServiceManager:
    """Wrapper around systemctl --user for onedrive services."""

    def __init__(self):
        self._services: list[str] = []
        self.discover_services()

    def discover_services(self) -> list[str]:
        """Find all onedrive user services."""
        result = subprocess.run(
            ["systemctl", "--user", "list-units", "--type=service",
             "--all", "--no-legend", "--no-pager"],
            capture_output=True, text=True
        )
        self._services = []
        for line in result.stdout.splitlines():
            parts = line.split()
            if parts and "onedrive" in parts[0] and "monitor" not in parts[0]:
                name = parts[0].replace(".service", "")
                self._services.append(name)
        return self._services

    @property
    def services(self) -> list[str]:
        return list(self._services)

    def get_status(self, service_name: str) -> ServiceStatus:
        """Get detailed status for a service."""
        confdir = self._get_confdir(service_name)
        sync_dir = ""
        if confdir and confdir.exists():
            config_file = confdir / "config"
            if config_file.exists():
                for line in config_file.read_text().splitlines():
                    if line.strip().startswith("sync_dir"):
                        sync_dir = line.split("=", 1)[1].strip().strip('"')
                        break

        # Get display name from unit description
        result = subprocess.run(
            ["systemctl", "--user", "show", f"{service_name}.service",
             "--property=Description,ActiveState,MainPID", "--no-pager"],
            capture_output=True, text=True
        )
        props = {}
        for line in result.stdout.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                props[k] = v

        active = props.get("ActiveState", "") == "active"
        display_name = props.get("Description", service_name)
        pid = int(props.get("MainPID", "0"))

        return ServiceStatus(
            name=service_name,
            display_name=display_name,
            active=active,
            status_text="active" if active else "inactive",
            confdir=confdir or Path(),
            sync_dir=sync_dir,
            pid=pid,
        )

    def get_all_statuses(self) -> list[ServiceStatus]:
        """Get status for all discovered services."""
        return [self.get_status(s) for s in self._services]

    def start(self, service_name: str) -> tuple[bool, str]:
        return self._run_ctl("start", service_name)

    def stop(self, service_name: str) -> tuple[bool, str]:
        return self._run_ctl("stop", service_name)

    def restart(self, service_name: str) -> tuple[bool, str]:
        return self._run_ctl("restart", service_name)

    def has_recent_errors(self, service_name: str, minutes: int = 10) -> list[str]:
        """Check journalctl for recent errors."""
        result = subprocess.run(
            ["journalctl", "--user", "-u", f"{service_name}.service",
             "--since", f"{minutes} minutes ago", "--no-pager", "-q"],
            capture_output=True, text=True
        )
        errors = []
        for line in result.stdout.splitlines():
            lower = line.lower()
            if "error" in lower or "cannot connect" in lower or "big_delete" in lower:
                errors.append(line)
        return errors

    def get_logs(self, service_name: str, lines: int = 100) -> str:
        """Get recent logs for a service."""
        result = subprocess.run(
            ["journalctl", "--user", "-u", f"{service_name}.service",
             "-n", str(lines), "--no-pager", "-q"],
            capture_output=True, text=True
        )
        return result.stdout

    def _run_ctl(self, action: str, service_name: str) -> tuple[bool, str]:
        result = subprocess.run(
            ["systemctl", "--user", action, f"{service_name}.service"],
            capture_output=True, text=True
        )
        return result.returncode == 0, result.stderr.strip()

    def _get_confdir(self, service_name: str) -> Path | None:
        """Determine config directory for a service."""
        # Read ExecStart from service unit to find --confdir
        result = subprocess.run(
            ["systemctl", "--user", "show", f"{service_name}.service",
             "--property=ExecStart", "--no-pager"],
            capture_output=True, text=True
        )
        output = result.stdout
        if "--confdir=" in output:
            for part in output.split():
                if part.startswith("--confdir=") or part.startswith("confdir="):
                    path = part.split("confdir=", 1)[1].rstrip(";")
                    return Path(path)
        # Default fallback
        home = Path.home()
        if service_name == "onedrive":
            return home / ".config" / "onedrive"
        return home / ".config" / service_name
