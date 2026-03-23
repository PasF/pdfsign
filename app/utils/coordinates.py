from PySide6.QtCore import QPointF, QRectF


def scene_to_pdf_point(scene_pos: QPointF, dpi: int) -> tuple[float, float]:
    ratio = 72.0 / dpi
    return scene_pos.x() * ratio, scene_pos.y() * ratio


def scene_to_pdf_rect(scene_rect: QRectF, dpi: int) -> tuple[float, float, float, float]:
    ratio = 72.0 / dpi
    return (
        scene_rect.x() * ratio,
        scene_rect.y() * ratio,
        (scene_rect.x() + scene_rect.width()) * ratio,
        (scene_rect.y() + scene_rect.height()) * ratio,
    )
