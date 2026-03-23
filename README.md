# PDFSign

Application portable (Windows & macOS) pour signer des documents PDF : positionnez une signature PNG et des zones de texte directement sur le document, puis exportez le résultat.

## Fonctionnalités

- Ouvrir un PDF via l'interface graphique ou en ligne de commande
- Importer une image de signature (PNG/JPG) et la positionner par glisser-déposer
- Redimensionner la signature via les poignées aux coins
- Ajouter une ou plusieurs zones de texte, les déplacer et les éditer (double-clic)
- Navigation multi-pages
- Zoom avec Ctrl + molette
- Export en un clic

## Prérequis

- Python 3.10+

## Installation

```bash
# Cloner le projet
git clone https://github.com/PasF/pdfsign.git
cd pdfsign

# Créer un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate    # macOS / Linux
venv\Scripts\activate       # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

### Lancement via l'interface graphique

```bash
python main.py
```

Puis cliquer sur **Open PDF** dans la barre d'outils.

### Lancement avec un fichier PDF

```bash
python main.py chemin/vers/document.pdf
```

### Workflow

1. **Ouvrir un PDF** — via le bouton ou en ligne de commande
2. **Importer une signature** — cliquer sur "Import Signature", sélectionner un PNG/JPG. La signature apparaît sur la page : déplacez-la et redimensionnez-la.
3. **Ajouter du texte** — cliquer sur "Add Text". Double-cliquer sur la zone pour éditer le texte, puis la déplacer.
4. **Naviguer** — utiliser les boutons "Prev" / "Next" pour changer de page. Les éléments sont conservés par page.
5. **Exporter** — cliquer sur le bouton **Done** en bas à droite. Le fichier `*_signed.pdf` est généré dans le même répertoire que le PDF source.

### Raccourcis

| Action          | Raccourci           |
|-----------------|---------------------|
| Zoom avant/arrière | Ctrl + molette   |
| Éditer un texte | Double-clic         |
| Déplacer un élément | Cliquer-glisser |

## Créer un exécutable portable

```bash
pip install pyinstaller

# macOS
pyinstaller --name pdfsign --windowed --onedir main.py

# Windows
pyinstaller --name pdfsign --windowed --onedir main.py
```

L'exécutable se trouve dans `dist/pdfsign/`. Distribuez ce dossier tel quel — aucune installation n'est requise.

> **Note macOS** : au premier lancement, faites clic droit > Ouvrir pour contourner Gatekeeper.

## Structure du projet

```
pdfsign/
  main.py                  # Point d'entrée
  app/
    main_window.py          # Fenêtre principale
    pdf_view.py             # Canvas interactif (QGraphicsView)
    pdf_document.py         # Chargement et export PDF (PyMuPDF)
    items/
      signature_item.py     # Élément signature draggable
      text_item.py          # Élément texte draggable/éditable
    utils/
      coordinates.py        # Conversion coordonnées scène ↔ PDF
  requirements.txt
  README.md
```

## Technologies

- [PySide6](https://doc.qt.io/qtforpython-6/) — Interface graphique cross-platform (LGPL)
- [PyMuPDF](https://pymupdf.readthedocs.io/) — Rendu et manipulation PDF
- [PyInstaller](https://pyinstaller.org/) — Packaging en exécutable portable
