# PDFSign

Portable application (Windows & macOS) for signing PDF documents: overlay a PNG signature and text boxes directly on the document, then export the result.

## Features

- Open a PDF via the GUI or command line
- Import a signature image (PNG/JPG) and position it with drag-and-drop
- Resize the signature using corner handles
- Add one or more text boxes, move and edit them (double-click)
- Multi-page navigation
- Zoom with Ctrl + scroll wheel
- One-click export

## Prerequisites

- Python 3.10+

## Installation

```bash
# Clone the project
git clone https://github.com/PasF/pdfsign.git
cd pdfsign

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate    # macOS / Linux
venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Launch the GUI

```bash
python main.py
```

Then click **Open PDF** in the toolbar.

### Open a PDF directly

```bash
python main.py path/to/document.pdf
```

### Workflow

1. **Open a PDF** — via the button or command line
2. **Import a signature** — click "Import Signature", select a PNG/JPG. The signature appears on the page: drag and resize it.
3. **Add text** — click "Add Text". Double-click the text box to edit, then drag it into position.
4. **Navigate** — use the "Prev" / "Next" buttons to change pages. Elements are preserved per page.
5. **Export** — click the **Done** button in the bottom-right corner. The file `*_signed.pdf` is generated in the same directory as the source PDF.

### Shortcuts

| Action             | Shortcut          |
|--------------------|-------------------|
| Zoom in/out        | Ctrl + scroll     |
| Edit text          | Double-click      |
| Move an element    | Click and drag    |

## Build a portable executable

```bash
pip install pyinstaller

# macOS
pyinstaller --name pdfsign --windowed --onedir main.py

# Windows
pyinstaller --name pdfsign --windowed --onedir main.py
```

The executable is located in `dist/pdfsign/`. Distribute this folder as-is — no installation required.

> **macOS note**: on first launch, right-click > Open to bypass Gatekeeper.

## Project structure

```
pdfsign/
  main.py                  # Entry point
  app/
    main_window.py          # Main window
    pdf_view.py             # Interactive canvas (QGraphicsView)
    pdf_document.py         # PDF loading and export (PyMuPDF)
    items/
      signature_item.py     # Draggable signature element
      text_item.py          # Draggable/editable text element
    utils/
      coordinates.py        # Scene-to-PDF coordinate conversion
  requirements.txt
  README.md
```

## Technologies

- [PySide6](https://doc.qt.io/qtforpython-6/) — Cross-platform GUI (LGPL)
- [PyMuPDF](https://pymupdf.readthedocs.io/) — PDF rendering and manipulation
- [PyInstaller](https://pyinstaller.org/) — Portable executable packaging
