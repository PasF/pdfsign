from PySide6.QtCore import Qt, QRectF, QPointF
from PySide6.QtGui import QPixmap, QPen, QColor, QPainter, QCursor
from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsSceneMouseEvent

HANDLE_SIZE = 8


class SignatureItem(QGraphicsPixmapItem):
    def __init__(self, png_path: str, page_index: int):
        super().__init__()
        self.png_path = png_path
        self.page_index = page_index
        self._original_pixmap = QPixmap(png_path)
        self._resizing = False
        self._resize_corner = None
        self._resize_origin = QPointF()
        self._resize_start_rect = QRectF()

        # Scale to a reasonable default width
        scaled = self._original_pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(scaled)

        self.setFlags(
            QGraphicsPixmapItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsPixmapItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    def _base_rect(self) -> QRectF:
        return super().boundingRect()

    def boundingRect(self) -> QRectF:
        m = HANDLE_SIZE / 2 + 2
        return self._base_rect().adjusted(-m, -m, m, m)

    def _handle_rects(self) -> list[QRectF]:
        br = self._base_rect()
        hs = HANDLE_SIZE
        return [
            QRectF(br.right() - hs, br.bottom() - hs, hs, hs),  # bottom-right
            QRectF(br.x(), br.bottom() - hs, hs, hs),           # bottom-left
            QRectF(br.right() - hs, br.y(), hs, hs),            # top-right
            QRectF(br.x(), br.y(), hs, hs),                     # top-left
        ]

    def paint(self, painter: QPainter, option, widget=None):
        super().paint(painter, option, widget)
        if self.isSelected():
            painter.setPen(QPen(QColor(0, 120, 215), 1.5, Qt.PenStyle.DashLine))
            painter.drawRect(self._base_rect())
            painter.setBrush(QColor(0, 120, 215))
            painter.setPen(Qt.PenStyle.NoPen)
            for hr in self._handle_rects():
                painter.drawRect(hr)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if self.isSelected() and event.button() == Qt.MouseButton.LeftButton:
            for i, hr in enumerate(self._handle_rects()):
                if hr.contains(event.pos()):
                    self._resizing = True
                    self._resize_corner = i
                    self._resize_origin = event.scenePos()
                    self._resize_start_rect = QRectF(self.pos(), self.boundingRect().size())
                    event.accept()
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent):
        if self._resizing:
            delta = event.scenePos() - self._resize_origin
            r = QRectF(self._resize_start_rect)

            if self._resize_corner == 0:  # bottom-right
                r.setWidth(max(40, r.width() + delta.x()))
                r.setHeight(max(40, r.height() + delta.y()))
            elif self._resize_corner == 1:  # bottom-left
                r.setLeft(r.left() + delta.x())
                r.setHeight(max(40, r.height() + delta.y()))
                if r.width() < 40:
                    r.setLeft(r.right() - 40)
            elif self._resize_corner == 2:  # top-right
                r.setWidth(max(40, r.width() + delta.x()))
                r.setTop(r.top() + delta.y())
                if r.height() < 40:
                    r.setTop(r.bottom() - 40)
            elif self._resize_corner == 3:  # top-left
                r.setLeft(r.left() + delta.x())
                r.setTop(r.top() + delta.y())
                if r.width() < 40:
                    r.setLeft(r.right() - 40)
                if r.height() < 40:
                    r.setTop(r.bottom() - 40)

            self.setPos(r.topLeft())
            scaled = self._original_pixmap.scaled(
                int(r.width()), int(r.height()),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.setPixmap(scaled)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent):
        if self._resizing:
            self._resizing = False
            self._resize_corner = None
            event.accept()
            return
        super().mouseReleaseEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsPixmapItem.GraphicsItemChange.ItemPositionChange and self.scene():
            scene_rect = self.scene().sceneRect()
            br = self.boundingRect()
            new_pos = value
            new_pos.setX(max(scene_rect.left(), min(new_pos.x(), scene_rect.right() - br.width())))
            new_pos.setY(max(scene_rect.top(), min(new_pos.y(), scene_rect.bottom() - br.height())))
            return new_pos
        return super().itemChange(change, value)
