import os

import fitz
from PySide6.QtCore import QRectF
from PySide6.QtGui import QImage, QPixmap

from app.utils.coordinates import scene_to_pdf_rect, scene_to_pdf_point


class PdfDocument:
    DPI = 150

    def __init__(self):
        self.doc: fitz.Document | None = None
        self.path: str = ""
        self.page_count: int = 0

    def load(self, path: str):
        self.doc = fitz.open(path)
        self.path = path
        self.page_count = len(self.doc)

    def render_page(self, page_index: int) -> QPixmap:
        if not self.doc:
            return QPixmap()
        page = self.doc[page_index]
        mat = fitz.Matrix(self.DPI / 72, self.DPI / 72)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format.Format_RGB888)
        return QPixmap.fromImage(img)

    def export(self, output_path: str, overlays: dict[int, list]):
        if not self.doc:
            return
        # Reopen the document to avoid modifying the displayed copy
        export_doc = fitz.open(self.path)
        for page_index, items in overlays.items():
            if page_index >= len(export_doc):
                continue
            page = export_doc[page_index]
            for item in items:
                if item["type"] == "signature":
                    rect = scene_to_pdf_rect(item["rect"], self.DPI)
                    pdf_rect = fitz.Rect(*rect)
                    page.insert_image(pdf_rect, filename=item["png_path"])
                elif item["type"] == "text":
                    px, py = scene_to_pdf_point(item["pos"], self.DPI)
                    font_size = item.get("font_size", 14) * (72.0 / self.DPI)
                    page.insert_text(
                        fitz.Point(px, py + font_size),
                        item["text"],
                        fontsize=font_size,
                        fontname="helv",
                        color=(0, 0, 0),
                    )
        export_doc.save(output_path)
        export_doc.close()
