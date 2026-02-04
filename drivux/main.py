"""Drivux - OneDrive Linux GUI Manager."""

import sys

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QAction
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QStyle
from PySide6.QtSvg import QSvgRenderer

from pathlib import Path

from . import __version__, __app_name__
from .service_manager import ServiceManager
from .main_window import MainWindow
from .i18n import t


ICONS_DIR = Path(__file__).parent / "resources" / "icons"


class DrivuxTray(QSystemTrayIcon):
    """System tray icon with status and menu."""

    def __init__(self, service_mgr: ServiceManager, app: QApplication):
        super().__init__()
        self._service_mgr = service_mgr
        self._app = app
        self._main_window: MainWindow | None = None

        self._icons = {
            "ok": self._load_icon("ok.svg"),
            "error": self._load_icon("error.svg"),
            "syncing": self._load_icon("syncing.svg"),
        }

        self.setIcon(self._icons.get("ok", self.style_icon()))
        self.setToolTip(f"{__app_name__} v{__version__}")

        self._build_menu()
        self.activated.connect(self._on_activated)

        # Status check timer
        self._timer = QTimer()
        self._timer.timeout.connect(self._update_status)
        self._timer.start(15000)  # 15s
        self._update_status()

    def _load_icon(self, name: str) -> QIcon:
        path = ICONS_DIR / name
        if path.exists():
            renderer = QSvgRenderer(str(path))
            pixmap = QPixmap(64, 64)
            pixmap.fill(Qt.GlobalColor.transparent)
            painter = QPainter(pixmap)
            renderer.render(painter)
            painter.end()
            return QIcon(pixmap)
        return self.style_icon()

    def style_icon(self) -> QIcon:
        return QApplication.style().standardIcon(QStyle.StandardPixmap.SP_DriveNetIcon)

    def _build_menu(self):
        menu = QMenu()

        # Title
        title = menu.addAction(f"{__app_name__} v{__version__}")
        title.setEnabled(False)
        menu.addSeparator()

        # Service statuses (will be updated dynamically)
        self._status_actions: list[QAction] = []
        for svc in self._service_mgr.services:
            label = svc.replace("onedrive-", "").replace("onedrive", t("personal"))
            action = menu.addAction(f"  {label}: ...")
            action.setEnabled(False)
            self._status_actions.append(action)

        menu.addSeparator()

        # Actions
        menu.addAction(t("open_drivux"), self._show_window)
        menu.addAction(t("restart_all"), self._restart_all)
        menu.addSeparator()
        menu.addAction(t("quit"), self._quit)

        self.setContextMenu(menu)

    def _update_status(self):
        statuses = self._service_mgr.get_all_statuses()
        has_error = False

        for i, st in enumerate(statuses):
            if i >= len(self._status_actions):
                break
            label = st.name.replace("onedrive-", "").replace("onedrive", t("personal"))

            if not st.active:
                self._status_actions[i].setText(f"  {label}: {t('stopped')}")
                has_error = True
            else:
                errors = self._service_mgr.has_recent_errors(st.name)
                if errors:
                    self._status_actions[i].setText(f"  {label}: {t('error').upper()}")
                    has_error = True
                else:
                    self._status_actions[i].setText(f"  {label}: {t('ok')}")

        # Update tray icon
        if has_error:
            self.setIcon(self._icons.get("error", self.style_icon()))
            self.setToolTip(f"{__app_name__} - {t('error_detected')}")
        else:
            self.setIcon(self._icons.get("ok", self.style_icon()))
            self.setToolTip(f"{__app_name__} - {t('all_ok')}")

    def _on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self._show_window()

    def _show_window(self):
        if self._main_window is None:
            self._main_window = MainWindow(self._service_mgr)
        self._main_window.show()
        self._main_window.raise_()
        self._main_window.activateWindow()

    def _restart_all(self):
        for svc in self._service_mgr.services:
            self._service_mgr.restart(svc)
        self._update_status()

    def _quit(self):
        if self._main_window:
            self._main_window.close()
        self._app.quit()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName(__app_name__)
    app.setApplicationVersion(__version__)
    app.setQuitOnLastWindowClosed(False)

    service_mgr = ServiceManager()

    if not service_mgr.services:
        print(t("no_service"))
        sys.exit(1)

    tray = DrivuxTray(service_mgr, app)
    tray.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
