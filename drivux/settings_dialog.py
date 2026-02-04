"""Settings dialog for editing OneDrive service configurations."""

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, QWidget,
    QFormLayout, QLineEdit, QSpinBox, QCheckBox, QPushButton,
    QLabel, QMessageBox, QGroupBox,
)

from .config_manager import ConfigManager, CONFIG_KEYS
from .service_manager import ServiceManager, ServiceStatus
from .i18n import t


class ServiceConfigTab(QWidget):
    """Config editor tab for a single service."""

    def __init__(self, status: ServiceStatus, parent=None):
        super().__init__(parent)
        self._status = status
        self._config = ConfigManager(status.confdir / "config")
        self._widgets: dict[str, QWidget] = {}
        self._config_group_title = t("configuration")
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Service info
        info_group = QGroupBox(t("service"))
        info_layout = QFormLayout(info_group)
        info_layout.addRow(f"{t('name')}:", QLabel(self._status.display_name))
        info_layout.addRow(f"{t('status')}:", QLabel(
            f"{t('active') if self._status.active else t('inactive')} (PID {self._status.pid})"
        ))
        info_layout.addRow(f"{t('config_path')}:", QLabel(str(self._status.confdir / "config")))
        layout.addWidget(info_group)

        # Config values
        config_group = QGroupBox(self._config_group_title)
        form = QFormLayout(config_group)

        current = self._config.read()

        # Show existing config values
        for key, value in current.items():
            desc = CONFIG_KEYS.get(key, key)
            widget = QLineEdit(value)
            widget.setToolTip(desc)
            form.addRow(f"{key}:", widget)
            self._widgets[key] = widget

        layout.addWidget(config_group)

        # Add new parameter
        add_group = QGroupBox(t("add_parameter"))
        add_layout = QHBoxLayout(add_group)
        self._new_key = QLineEdit()
        self._new_key.setPlaceholderText(t("key"))
        add_layout.addWidget(self._new_key)
        self._new_value = QLineEdit()
        self._new_value.setPlaceholderText(t("value"))
        add_layout.addWidget(self._new_value)
        btn_add = QPushButton("+")
        btn_add.setFixedWidth(40)
        btn_add.clicked.connect(self._add_param)
        add_layout.addWidget(btn_add)
        layout.addWidget(add_group)

        layout.addStretch()

    def _add_param(self):
        key = self._new_key.text().strip()
        value = self._new_value.text().strip()
        if not key:
            return
        widget = QLineEdit(value)
        desc = CONFIG_KEYS.get(key, key)
        widget.setToolTip(desc)
        for group in self.findChildren(QGroupBox):
            if group.title() == self._config_group_title:
                group.layout().addRow(f"{key}:", widget)
                break
        self._widgets[key] = widget
        self._new_key.clear()
        self._new_value.clear()

    def save(self) -> bool:
        """Save current widget values to config file."""
        config = {}
        for key, widget in self._widgets.items():
            value = widget.text().strip()
            if value:
                config[key] = value
        try:
            self._config.write(config)
            return True
        except Exception as e:
            QMessageBox.critical(self, t("error"), f"{t('save_error')}\n{e}")
            return False


class SettingsDialog(QDialog):
    """Main settings dialog with tabs per service."""

    def __init__(self, service_mgr: ServiceManager, parent=None):
        super().__init__(parent)
        self._service_mgr = service_mgr
        self.setWindowTitle(f"Drivux - {t('settings')}")
        self.setMinimumSize(600, 500)
        self._tabs: list[ServiceConfigTab] = []
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        self._tab_widget = QTabWidget()
        for status in self._service_mgr.get_all_statuses():
            label = status.name.replace("onedrive-", "").replace("onedrive", t("personal"))
            tab = ServiceConfigTab(status)
            self._tab_widget.addTab(tab, label)
            self._tabs.append(tab)
        layout.addWidget(self._tab_widget)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_save = QPushButton(t("save"))
        btn_save.clicked.connect(self._save_all)
        btn_layout.addWidget(btn_save)

        btn_save_restart = QPushButton(t("save_restart"))
        btn_save_restart.clicked.connect(self._save_and_restart)
        btn_layout.addWidget(btn_save_restart)

        btn_cancel = QPushButton(t("cancel"))
        btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancel)

        layout.addLayout(btn_layout)

    def _save_all(self) -> bool:
        all_ok = all(tab.save() for tab in self._tabs)
        if all_ok:
            QMessageBox.information(self, "Drivux", t("config_saved"))
            self.accept()
        return all_ok

    def _save_and_restart(self):
        if not self._save_all():
            return
        for status in self._service_mgr.get_all_statuses():
            self._service_mgr.restart(status.name)
        QMessageBox.information(self, "Drivux", t("services_restarted"))
