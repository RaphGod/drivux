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

## Installation

**Installation en une ligne** (recommande) :

```bash
curl -sSL https://raw.githubusercontent.com/RaphGod/drivux/main/install.sh | bash
```

L'installeur va :
- Telecharger Drivux dans `~/.local/share/drivux`
- Creer un environnement Python avec les dependances
- Creer la commande `drivux` dans `~/.local/bin`
- Ajouter Drivux au menu des applications
- Proposer le demarrage automatique a la connexion

Puis lancez simplement :
```bash
drivux
```

<details>
<summary>Installation manuelle</summary>

```bash
git clone https://github.com/RaphGod/drivux.git
cd drivux
python -m venv .venv
source .venv/bin/activate
pip install -e .
drivux
```

</details>

### Desinstallation

```bash
curl -sSL https://raw.githubusercontent.com/RaphGod/drivux/main/uninstall.sh | bash
```

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

## Sponsors

<a href="https://dogma.fr">
  <img src="https://img.shields.io/badge/Developpe%20par-Dogma-blue?style=flat" alt="Dogma">
</a>

Drivux est developpe et maintenu par [Dogma](https://dogma.fr), societe de conseil en informatique.

## Licence

[GPL-3.0](../LICENSE)
