<p align="center">
  <img src="screenshot.png" alt="Drivux Screenshot" width="700"/>
</p>

<h1 align="center">Drivux</h1>

<p align="center">
  <strong>Interface graphique pour le <a href="https://github.com/abraunegg/onedrive">client OneDrive Linux</a></strong><br>
  Surveillez, configurez et controlez vos services de synchronisation OneDrive depuis le systray.
</p>

<p align="center">
  <a href="../README.md">English</a> | <a href="README_FR.md">Fran&ccedil;ais</a>
</p>

---

## Pourquoi Drivux ?

Le client [abraunegg/onedrive](https://github.com/abraunegg/onedrive) pour Linux est puissant mais n'a aucune interface graphique. Gerer plusieurs bibliotheques OneDrive/SharePoint oblige a jongler entre fichiers de config, commandes systemctl et logs journalctl.

**Drivux** reunit tout dans une interface systray simple :

- Voir d'un coup d'oeil si la synchro fonctionne ou non
- Lire les logs en direct sans ouvrir un terminal
- Modifier la configuration sans editeur de texte
- Demarrer, arreter ou redemarrer les services en un clic

## Fonctionnalites

| Fonctionnalite | Description |
|----------------|------------|
| **Icone systray** | Change de couleur selon l'etat de synchro (vert = OK, rouge = erreur, orange = en cours) |
| **Tableau de bord** | Vue d'ensemble de toutes les instances OneDrive avec statut, PID, repertoire de synchro |
| **Logs en direct** | Logs en temps reel avec coloration et filtrage par service |
| **Editeur de config** | Modifier tous les parametres OneDrive depuis l'interface |
| **Controle des services** | Demarrer / arreter / redemarrer individuellement ou tous les services |
| **Multi-instances** | Gere simultanement plusieurs bibliotheques OneDrive et SharePoint |
| **Notifications desktop** | Alertes en cas d'erreur de synchro (DNS, big delete, etc.) |

## Prerequis

- Linux avec **systemd**
- [abraunegg/onedrive](https://github.com/abraunegg/onedrive) installe et configure en **services systemd utilisateur**
- Python 3.10+

## Installation rapide

```bash
git clone https://github.com/RaphGod/drivux.git
cd drivux
python -m venv .venv
source .venv/bin/activate
pip install -e .
drivux
```

## Demarrage automatique

```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/drivux.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=Drivux
Comment=Gestionnaire de synchronisation OneDrive
Exec=/chemin/vers/drivux/.venv/bin/drivux
Icon=cloud
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF
```

Remplacez `/chemin/vers/drivux` par votre chemin d'installation.

## Fonctionnement

Drivux est une **couche de controle** au-dessus du client OneDrive existant. Il ne remplace ni ne modifie le client lui-meme.

```
Drivux (GUI)
    |
    +-- systemctl --user    --> gestion des services
    +-- journalctl --user   --> lecture des logs en direct
    +-- ~/.config/onedrive* --> lecture/ecriture des fichiers de config
    |
Client OneDrive (abraunegg)
    |
Microsoft OneDrive / SharePoint
```

## Contribuer

Les contributions sont les bienvenues ! N'hesitez pas a ouvrir des issues ou des pull requests.

## Licence

[MIT](../LICENSE)
