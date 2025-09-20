import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QPainter, QPen, QPolygonF
from PyQt5.QtCore import Qt, QPoint, QPointF
import math

class ArrowWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arrow Between Buttons")
        self.setGeometry(100, 100, 400, 300)

        # Create two buttons
        self.button1 = QPushButton("Start", self)
        self.button1.move(50, 100)

        self.button2 = QPushButton("End", self)
        self.button2.move(250, 150)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)

        # Get center positions of the buttons
        p1 = self.button1.geometry().center()
        p2 = self.button2.geometry().center()

        # Draw main line
        painter.drawLine(p1, p2)

        # Draw arrowhead
        self.draw_arrowhead(painter, p1, p2)

    def draw_arrowhead(self, painter, start, end):
        """Draws an arrowhead at the end point."""
        angle = math.atan2(end.y() - start.y(), end.x() - start.x())
        arrow_size = 10

        # Points for arrowhead
        p1 = QPointF(
            end.x() - arrow_size * math.cos(angle - math.pi / 6),
            end.y() - arrow_size * math.sin(angle - math.pi / 6)
        )
        p2 = QPointF(
            end.x() - arrow_size * math.cos(angle + math.pi / 6),
            end.y() - arrow_size * math.sin(angle + math.pi / 6)
        )

        arrow_head = QPolygonF([end, p1, p2])
        painter.setBrush(Qt.black)
        painter.drawPolygon(arrow_head)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ArrowWidget()
    window.show()
    sys.exit(app.exec_())