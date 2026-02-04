"""Internationalization support for Drivux."""

import locale

TRANSLATIONS = {
    "en": {
        "services": "Services",
        "service": "Service",
        "status": "Status",
        "folder": "Folder",
        "pid": "PID",
        "actions": "Actions",
        "active": "Active",
        "inactive": "Inactive",
        "error": "Error",
        "refresh": "Refresh",
        "settings": "Settings",
        "start": "Start",
        "stop": "Stop",
        "restart": "Restart",
        "restart_all": "Restart all",
        "open_drivux": "Open Drivux",
        "quit": "Quit",
        "all_ok": "All OK",
        "error_detected": "Error detected",
        "filter": "Filter",
        "filter_placeholder": "e.g. error, download, sync...",
        "clear": "Clear",
        "save": "Save",
        "save_restart": "Save & Restart",
        "cancel": "Cancel",
        "config_saved": "Configuration saved.",
        "services_restarted": "Services restarted.",
        "save_error": "Unable to save:",
        "add_parameter": "Add parameter",
        "key": "key",
        "value": "value",
        "configuration": "Configuration",
        "name": "Name",
        "config_path": "Config",
        "stopped": "stopped",
        "ok": "OK",
        "personal": "personal",
        "no_service": "No onedrive service detected.",
    },
    "fr": {
        "services": "Services",
        "service": "Service",
        "status": "Statut",
        "folder": "Dossier",
        "pid": "PID",
        "actions": "Actions",
        "active": "Actif",
        "inactive": "Inactif",
        "error": "Erreur",
        "refresh": "Actualiser",
        "settings": "Parametres",
        "start": "Demarrer",
        "stop": "Stop",
        "restart": "Redemarrer",
        "restart_all": "Tout redemarrer",
        "open_drivux": "Ouvrir Drivux",
        "quit": "Quitter",
        "all_ok": "Tout est OK",
        "error_detected": "Erreur detectee",
        "filter": "Filtre",
        "filter_placeholder": "ex: error, download, sync...",
        "clear": "Effacer",
        "save": "Sauvegarder",
        "save_restart": "Sauvegarder && Redemarrer",
        "cancel": "Annuler",
        "config_saved": "Configuration sauvegardee.",
        "services_restarted": "Services redemarres.",
        "save_error": "Impossible de sauvegarder:",
        "add_parameter": "Ajouter un parametre",
        "key": "cle",
        "value": "valeur",
        "configuration": "Configuration",
        "name": "Nom",
        "config_path": "Config",
        "stopped": "arrete",
        "ok": "OK",
        "personal": "perso",
        "no_service": "Aucun service onedrive detecte.",
    },
    "de": {
        "services": "Dienste",
        "service": "Dienst",
        "status": "Status",
        "folder": "Ordner",
        "pid": "PID",
        "actions": "Aktionen",
        "active": "Aktiv",
        "inactive": "Inaktiv",
        "error": "Fehler",
        "refresh": "Aktualisieren",
        "settings": "Einstellungen",
        "start": "Starten",
        "stop": "Stoppen",
        "restart": "Neustarten",
        "restart_all": "Alle neustarten",
        "open_drivux": "Drivux offnen",
        "quit": "Beenden",
        "all_ok": "Alles OK",
        "error_detected": "Fehler erkannt",
        "filter": "Filter",
        "filter_placeholder": "z.B. error, download, sync...",
        "clear": "Loschen",
        "save": "Speichern",
        "save_restart": "Speichern && Neustarten",
        "cancel": "Abbrechen",
        "config_saved": "Konfiguration gespeichert.",
        "services_restarted": "Dienste neugestartet.",
        "save_error": "Speichern nicht moglich:",
        "add_parameter": "Parameter hinzufugen",
        "key": "Schlussel",
        "value": "Wert",
        "configuration": "Konfiguration",
        "name": "Name",
        "config_path": "Konfig",
        "stopped": "gestoppt",
        "ok": "OK",
        "personal": "Personlich",
        "no_service": "Kein OneDrive-Dienst erkannt.",
    },
    "es": {
        "services": "Servicios",
        "service": "Servicio",
        "status": "Estado",
        "folder": "Carpeta",
        "pid": "PID",
        "actions": "Acciones",
        "active": "Activo",
        "inactive": "Inactivo",
        "error": "Error",
        "refresh": "Actualizar",
        "settings": "Configuracion",
        "start": "Iniciar",
        "stop": "Detener",
        "restart": "Reiniciar",
        "restart_all": "Reiniciar todo",
        "open_drivux": "Abrir Drivux",
        "quit": "Salir",
        "all_ok": "Todo OK",
        "error_detected": "Error detectado",
        "filter": "Filtro",
        "filter_placeholder": "ej: error, download, sync...",
        "clear": "Limpiar",
        "save": "Guardar",
        "save_restart": "Guardar && Reiniciar",
        "cancel": "Cancelar",
        "config_saved": "Configuracion guardada.",
        "services_restarted": "Servicios reiniciados.",
        "save_error": "No se pudo guardar:",
        "add_parameter": "Agregar parametro",
        "key": "clave",
        "value": "valor",
        "configuration": "Configuracion",
        "name": "Nombre",
        "config_path": "Config",
        "stopped": "detenido",
        "ok": "OK",
        "personal": "personal",
        "no_service": "Ningun servicio OneDrive detectado.",
    },
}

_current_lang = "en"


def detect_language() -> str:
    """Detect system language from locale."""
    try:
        lang = locale.getdefaultlocale()[0] or "en"
        lang = lang.split("_")[0].lower()
        if lang in TRANSLATIONS:
            return lang
    except Exception:
        pass
    return "en"


def set_language(lang: str) -> None:
    global _current_lang
    if lang in TRANSLATIONS:
        _current_lang = lang


def get_language() -> str:
    return _current_lang


def t(key: str) -> str:
    """Get translated string for current language."""
    return TRANSLATIONS.get(_current_lang, TRANSLATIONS["en"]).get(
        key, TRANSLATIONS["en"].get(key, key)
    )


# Auto-detect on import
_current_lang = detect_language()
