from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap,QPainter,QPen
from PyQt5.QtCore import Qt
# from guiocr.utils.shape import Rectangle
class Canvas(QWidget):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shapes = []
        self.pixmap = QPixmap()
        self._painter = QPainter()

    def loadPixmap(self,pixmap):
        self.pixmap = pixmap

    def loadShapes(self,shapes):
        self.shapes = shapes

    def paintEvent(self, event):
        p = self._painter
        p.begin(self)
        p.setRenderHint(QPainter.Antialiasing)
        p.setRenderHint(QPainter.HighQualityAntialiasing)
        p.setRenderHint(QPainter.SmoothPixmapTransform)
        p.drawPixmap(0, 0, self.pixmap)
        p.setPen(QPen(Qt.red,2,Qt.SolidLine))
        if self.shapes:
            for shape in self.shapes:
                p.drawRect(shape)
        p.end()
    
    def resetState(self):
        self.pixmap = None
        self.update()
