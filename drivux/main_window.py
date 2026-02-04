"""Main window with service overview and live logs."""

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton,
    QHeaderView, QSplitter, QLabel, QMenu,
)
from PySide6.QtGui import QColor, QIcon, QAction

from .service_manager import ServiceManager
from .log_viewer import LogViewer
from .settings_dialog import SettingsDialog


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, service_mgr: ServiceManager, parent=None):
        super().__init__(parent)
        self._service_mgr = service_mgr
        self.setWindowTitle("Drivux - OneDrive Manager")
        self.setMinimumSize(900, 600)
        self._setup_ui()
        self._refresh_timer = QTimer(self)
        self._refresh_timer.timeout.connect(self._refresh_status)
        self._refresh_timer.start(10000)  # 10s
        self._refresh_status()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        splitter = QSplitter(Qt.Orientation.Vertical)

        # Top: service table
        top = QWidget()
        top_layout = QVBoxLayout(top)
        top_layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        header_layout.addWidget(QLabel("Services OneDrive"))
        header_layout.addStretch()

        btn_refresh = QPushButton("Actualiser")
        btn_refresh.clicked.connect(self._refresh_status)
        header_layout.addWidget(btn_refresh)

        btn_settings = QPushButton("Parametres")
        btn_settings.clicked.connect(self._open_settings)
        header_layout.addWidget(btn_settings)

        top_layout.addLayout(header_layout)

        self._table = QTableWidget(0, 5)
        self._table.setHorizontalHeaderLabels([
            "Service", "Statut", "Dossier", "PID", "Actions"
        ])
        self._table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.Stretch
        )
        self._table.horizontalHeader().setSectionResizeMode(
            2, QHeaderView.ResizeMode.Stretch
        )
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self._table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self._table.customContextMenuRequested.connect(self._context_menu)
        top_layout.addWidget(self._table)
        splitter.addWidget(top)

        # Bottom: log viewer
        self._log_viewer = LogViewer(self._service_mgr.services)
        splitter.addWidget(self._log_viewer)

        splitter.setSizes([250, 350])
        layout.addWidget(splitter)

    def _refresh_status(self):
        statuses = self._service_mgr.get_all_statuses()
        self._table.setRowCount(len(statuses))

        for row, st in enumerate(statuses):
            # Name
            label = st.display_name or st.name
            self._table.setItem(row, 0, QTableWidgetItem(label))

            # Status
            status_item = QTableWidgetItem("Actif" if st.active else "Inactif")
            if st.active:
                errors = self._service_mgr.has_recent_errors(st.name)
                if errors:
                    status_item.setText("Erreur")
                    status_item.setForeground(QColor("#f38ba8"))
                else:
                    status_item.setForeground(QColor("#a6e3a1"))
            else:
                status_item.setForeground(QColor("#f9e2af"))
            self._table.setItem(row, 1, status_item)

            # Sync dir
            self._table.setItem(row, 2, QTableWidgetItem(st.sync_dir))

            # PID
            self._table.setItem(row, 3, QTableWidgetItem(str(st.pid) if st.pid else "-"))

            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(4, 2, 4, 2)

            if st.active:
                btn_restart = QPushButton("Redemarrer")
                btn_restart.setProperty("service", st.name)
                btn_restart.clicked.connect(self._restart_service)
                actions_layout.addWidget(btn_restart)

                btn_stop = QPushButton("Stop")
                btn_stop.setProperty("service", st.name)
                btn_stop.clicked.connect(self._stop_service)
                actions_layout.addWidget(btn_stop)
            else:
                btn_start = QPushButton("Demarrer")
                btn_start.setProperty("service", st.name)
                btn_start.clicked.connect(self._start_service)
                actions_layout.addWidget(btn_start)

            self._table.setCellWidget(row, 4, actions_widget)

    def _restart_service(self):
        name = self.sender().property("service")
        self._service_mgr.restart(name)
        self._refresh_status()

    def _stop_service(self):
        name = self.sender().property("service")
        self._service_mgr.stop(name)
        self._refresh_status()

    def _start_service(self):
        name = self.sender().property("service")
        self._service_mgr.start(name)
        self._refresh_status()

    def _open_settings(self):
        dialog = SettingsDialog(self._service_mgr, self)
        dialog.exec()
        self._refresh_status()

    def _context_menu(self, pos):
        row = self._table.rowAt(pos.y())
        if row < 0:
            return
        statuses = self._service_mgr.get_all_statuses()
        if row >= len(statuses):
            return
        st = statuses[row]

        menu = QMenu(self)
        if st.active:
            menu.addAction("Redemarrer", lambda: (
                self._service_mgr.restart(st.name), self._refresh_status()
            ))
            menu.addAction("Arreter", lambda: (
                self._service_mgr.stop(st.name), self._refresh_status()
            ))
        else:
            menu.addAction("Demarrer", lambda: (
                self._service_mgr.start(st.name), self._refresh_status()
            ))
        menu.exec(self._table.viewport().mapToGlobal(pos))

    def closeEvent(self, event):
        self._log_viewer.cleanup()
        self._refresh_timer.stop()
        event.accept()
