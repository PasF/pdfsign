from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPainter, QPixmap, QWheelEvent
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem

from app.items.signature_item import SignatureItem
from app.items.text_item import TextItem


class PdfGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scene = QGraphicsScene(self)
        self.setScene(self._scene)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self._bg_item: QGraphicsPixmapItem | None = None
        self._current_page: int = 0
        self._overlays: dict[int, list] = {}  # page_index -> list of items
        self._zoom = 1.0

    def set_page(self, pixmap: QPixmap, page_index: int):
        # Hide current page overlays
        for item in self._overlays.get(self._current_page, []):
            item.setVisible(False)

        self._current_page = page_index

        # Set background
        if self._bg_item:
            self._scene.removeItem(self._bg_item)
        self._bg_item = self._scene.addPixmap(pixmap)
        self._bg_item.setZValue(-1)
        self._bg_item.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable, False)
        self._bg_item.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable, False)
        self._scene.setSceneRect(QRectF(pixmap.rect()))

        # Show overlays for this page
        for item in self._overlays.get(page_index, []):
            item.setVisible(True)

    def add_signature(self, png_path: str, page_index: int) -> SignatureItem:
        item = SignatureItem(png_path, page_index)
        # Place at center of visible area
        center = self.mapToScene(self.viewport().rect().center())
        item.setPos(center - QPointF(item.boundingRect().width() / 2, item.boundingRect().height() / 2))
        self._scene.addItem(item)
        self._overlays.setdefault(page_index, []).append(item)
        if page_index != self._current_page:
            item.setVisible(False)
        return item

    def add_text(self, page_index: int) -> TextItem:
        item = TextItem(page_index)
        center = self.mapToScene(self.viewport().rect().center())
        item.setPos(center - QPointF(item.boundingRect().width() / 2, item.boundingRect().height() / 2))
        self._scene.addItem(item)
        self._overlays.setdefault(page_index, []).append(item)
        if page_index != self._current_page:
            item.setVisible(False)
        return item

    def get_all_overlays(self) -> dict[int, list[dict]]:
        result: dict[int, list[dict]] = {}
        for page_index, items in self._overlays.items():
            page_list = []
            for item in items:
                if isinstance(item, SignatureItem):
                    page_list.append({
                        "type": "signature",
                        "rect": QRectF(item.pos(), item.boundingRect().size()),
                        "png_path": item.png_path,
                    })
                elif isinstance(item, TextItem):
                    text = item.toPlainText().strip()
                    if text:
                        page_list.append({
                            "type": "text",
                            "pos": item.pos(),
                            "text": text,
                            "font_size": item.font().pointSize(),
                        })
            if page_list:
                result[page_index] = page_list
        return result

    def wheelEvent(self, event: QWheelEvent):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
            self._zoom *= factor
            self.scale(factor, factor)
            event.accept()
        else:
            super().wheelEvent(event)
