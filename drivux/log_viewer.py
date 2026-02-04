"""Live log viewer widget using journalctl --follow."""

import subprocess

from PySide6.QtCore import QProcess, Signal, QObject
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit,
    QComboBox, QLabel, QPushButton, QLineEdit,
)
from PySide6.QtGui import QTextCharFormat, QColor, QFont


class LogStream(QObject):
    """Streams journalctl output for a service."""
    new_line = Signal(str)
    error = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._process: QProcess | None = None

    def start(self, service_name: str):
        self.stop()
        self._process = QProcess(self)
        self._process.setProcessChannelMode(QProcess.MergedChannels)
        self._process.readyReadStandardOutput.connect(self._on_output)
        self._process.start("journalctl", [
            "--user", "-u", f"{service_name}.service",
            "-f", "--no-pager", "-q", "-n", "200",
        ])

    def stop(self):
        if self._process and self._process.state() != QProcess.NotRunning:
            self._process.kill()
            self._process.waitForFinished(1000)
            self._process = None

    def _on_output(self):
        if self._process:
            data = self._process.readAllStandardOutput().data().decode("utf-8", errors="replace")
            for line in data.splitlines():
                if line.strip():
                    self.new_line.emit(line)


class LogViewer(QWidget):
    """Widget displaying live logs with filtering."""

    def __init__(self, service_names: list[str], parent=None):
        super().__init__(parent)
        self._service_names = service_names
        self._stream = LogStream(self)
        self._stream.new_line.connect(self._append_line)
        self._setup_ui()

        if service_names:
            self._on_service_changed(0)

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Toolbar
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("Service:"))

        self._combo = QComboBox()
        for name in self._service_names:
            label = name.replace("onedrive-", "").replace("onedrive", "perso")
            self._combo.addItem(label, name)
        self._combo.currentIndexChanged.connect(self._on_service_changed)
        toolbar.addWidget(self._combo, 1)

        toolbar.addWidget(QLabel("Filtre:"))
        self._filter = QLineEdit()
        self._filter.setPlaceholderText("ex: error, download, sync...")
        self._filter.textChanged.connect(self._apply_filter)
        toolbar.addWidget(self._filter, 1)

        self._btn_clear = QPushButton("Effacer")
        self._btn_clear.clicked.connect(self._clear_logs)
        toolbar.addWidget(self._btn_clear)

        layout.addLayout(toolbar)

        # Log area
        self._log_area = QTextEdit()
        self._log_area.setReadOnly(True)
        self._log_area.setFont(QFont("Monospace", 9))
        self._log_area.setStyleSheet(
            "QTextEdit { background-color: #1e1e2e; color: #cdd6f4; }"
        )
        layout.addWidget(self._log_area)

        self._all_lines: list[str] = []

    def _on_service_changed(self, index: int):
        self._all_lines.clear()
        self._log_area.clear()
        service = self._combo.itemData(index)
        if service:
            self._stream.start(service)

    def _append_line(self, line: str):
        self._all_lines.append(line)
        filter_text = self._filter.text().lower()
        if not filter_text or filter_text in line.lower():
            self._colorize_and_append(line)

    def _colorize_and_append(self, line: str):
        cursor = self._log_area.textCursor()
        fmt = QTextCharFormat()

        lower = line.lower()
        if "error" in lower or "cannot connect" in lower:
            fmt.setForeground(QColor("#f38ba8"))  # Red
        elif "warning" in lower or "deprec" in lower:
            fmt.setForeground(QColor("#fab387"))  # Orange
        elif "downloading" in lower:
            fmt.setForeground(QColor("#89b4fa"))  # Blue
        elif "sync with microsoft onedrive is complete" in lower:
            fmt.setForeground(QColor("#a6e3a1"))  # Green
        else:
            fmt.setForeground(QColor("#cdd6f4"))  # Default

        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(line + "\n", fmt)
        self._log_area.ensureCursorVisible()

    def _apply_filter(self, text: str):
        self._log_area.clear()
        filter_text = text.lower()
        for line in self._all_lines:
            if not filter_text or filter_text in line.lower():
                self._colorize_and_append(line)

    def _clear_logs(self):
        self._all_lines.clear()
        self._log_area.clear()

    def cleanup(self):
        self._stream.stop()
