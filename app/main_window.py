import os

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QToolBar, QFileDialog, QLabel, QHBoxLayout,
    QPushButton, QWidget, QVBoxLayout, QMessageBox, QStatusBar,
)

from app.pdf_document import PdfDocument
from app.pdf_view import PdfGraphicsView


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDFSign")
        self.setMinimumSize(900, 700)

        self.pdf_doc = PdfDocument()
        self.current_page = 0

        self._setup_toolbar()
        self._setup_central()
        self._setup_statusbar()

    def _setup_toolbar(self):
        toolbar = QToolBar("Main")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        open_action = QAction("Open PDF", self)
        open_action.triggered.connect(self._on_open_pdf)
        toolbar.addAction(open_action)

        self._import_sig_action = QAction("Import Signature", self)
        self._import_sig_action.setEnabled(False)
        self._import_sig_action.triggered.connect(self._on_import_signature)
        toolbar.addAction(self._import_sig_action)

        self._add_text_action = QAction("Add Text", self)
        self._add_text_action.setEnabled(False)
        self._add_text_action.triggered.connect(self._on_add_text)
        toolbar.addAction(self._add_text_action)

        toolbar.addSeparator()

        self._prev_btn = QAction("< Prev", self)
        self._prev_btn.setEnabled(False)
        self._prev_btn.triggered.connect(self._on_prev_page)
        toolbar.addAction(self._prev_btn)

        self._page_label = QLabel("  Page 0 / 0  ")
        toolbar.addWidget(self._page_label)

        self._next_btn = QAction("Next >", self)
        self._next_btn.setEnabled(False)
        self._next_btn.triggered.connect(self._on_next_page)
        toolbar.addAction(self._next_btn)

    def _setup_central(self):
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        self.pdf_view = PdfGraphicsView()
        layout.addWidget(self.pdf_view, stretch=1)

        bottom = QHBoxLayout()
        bottom.addStretch()
        self._done_btn = QPushButton("Done")
        self._done_btn.setEnabled(False)
        self._done_btn.setFixedSize(120, 36)
        self._done_btn.clicked.connect(self._on_done)
        bottom.addWidget(self._done_btn)
        bottom.setContentsMargins(8, 4, 8, 8)
        layout.addLayout(bottom)

        self.setCentralWidget(central)

    def _setup_statusbar(self):
        self._statusbar = QStatusBar()
        self.setStatusBar(self._statusbar)
        self._statusbar.showMessage("Open a PDF to get started.")

    def open_pdf(self, path: str):
        try:
            self.pdf_doc.load(path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot open PDF:\n{e}")
            return
        self.current_page = 0
        self._show_page(0)
        self._import_sig_action.setEnabled(True)
        self._add_text_action.setEnabled(True)
        self._done_btn.setEnabled(True)
        self._update_nav()
        self._statusbar.showMessage(f"Opened: {os.path.basename(path)}")

    def _show_page(self, index: int):
        pixmap = self.pdf_doc.render_page(index)
        self.pdf_view.set_page(pixmap, index)
        self.current_page = index
        self._update_nav()

    def _update_nav(self):
        total = self.pdf_doc.page_count
        self._page_label.setText(f"  Page {self.current_page + 1} / {total}  ")
        self._prev_btn.setEnabled(self.current_page > 0)
        self._next_btn.setEnabled(self.current_page < total - 1)

    def _on_open_pdf(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open PDF", "", "PDF Files (*.pdf)")
        if path:
            self.open_pdf(path)

    def _on_import_signature(self):
        path, _ = QFileDialog.getOpenFileName(self, "Import Signature", "", "Images (*.png *.jpg *.jpeg)")
        if path:
            self.pdf_view.add_signature(path, self.current_page)
            self._statusbar.showMessage(f"Signature added on page {self.current_page + 1}.")

    def _on_add_text(self):
        self.pdf_view.add_text(self.current_page)
        self._statusbar.showMessage(f"Text box added on page {self.current_page + 1}. Double-click to edit.")

    def _on_prev_page(self):
        if self.current_page > 0:
            self._show_page(self.current_page - 1)

    def _on_next_page(self):
        if self.current_page < self.pdf_doc.page_count - 1:
            self._show_page(self.current_page + 1)

    def _on_done(self):
        overlays = self.pdf_view.get_all_overlays()
        if not overlays:
            QMessageBox.information(self, "Nothing to export", "Add a signature or text first.")
            return

        output_dir = os.path.dirname(self.pdf_doc.path)
        base_name = os.path.splitext(os.path.basename(self.pdf_doc.path))[0]
        output_path = os.path.join(output_dir, f"{base_name}_signed.pdf")

        try:
            self.pdf_doc.export(output_path, overlays)
            QMessageBox.information(
                self, "Done",
                f"Signed PDF saved as:\n{output_path}"
            )
            self._statusbar.showMessage(f"Exported: {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Export Error", f"Failed to export:\n{e}")
