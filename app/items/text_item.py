from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QPen, QColor, QPainter, QFont, QCursor, QFocusEvent
from PySide6.QtWidgets import QGraphicsTextItem, QGraphicsSceneMouseEvent


class TextItem(QGraphicsTextItem):
    def __init__(self, page_index: int, text: str = "Text"):
        super().__init__(text)
        self.page_index = page_index
        self._editing = False

        self.setFont(QFont("Helvetica", 14))
        self.setDefaultTextColor(QColor(0, 0, 0))
        self.setFlags(
            QGraphicsTextItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsTextItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsTextItem.GraphicsItemFlag.ItemSendsGeometryChanges
        )
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))

    def boundingRect(self) -> QRectF:
        return super().boundingRect().adjusted(-3, -3, 3, 3)

    def paint(self, painter: QPainter, option, widget=None):
        # Draw text within the original rect
        super().paint(painter, option, widget)
        if self.isSelected() or self._editing:
            painter.setPen(QPen(QColor(0, 120, 215), 1.0, Qt.PenStyle.DashLine))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(super().boundingRect())

    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent):
        self._editing = True
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.setFocus(Qt.FocusReason.MouseFocusReason)
        super().mouseDoubleClickEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        self._editing = False
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
        self.setCursor(QCursor(Qt.CursorShape.OpenHandCursor))
        super().focusOutEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsTextItem.GraphicsItemChange.ItemPositionChange and self.scene():
            scene_rect = self.scene().sceneRect()
            br = self.boundingRect()
            new_pos = value
            new_pos.setX(max(scene_rect.left(), min(new_pos.x(), scene_rect.right() - br.width())))
            new_pos.setY(max(scene_rect.top(), min(new_pos.y(), scene_rect.bottom() - br.height())))
            return new_pos
        return super().itemChange(change, value)
