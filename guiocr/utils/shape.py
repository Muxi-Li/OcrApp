
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPainter


class Rectangles(object):
    def __init__(self) -> None:
        super().__init__()
        self.painter = QPainter()
        
    def set_task(self,box):
        self.x = box[0][0]
        self.y = box[0][1]
        self.width = abs(box[0][1]-box[0][0])
        self.height = abs(box[1][1]-box[0][1])
    def add_rec(self):
        self.rec = QRect(self.x,self.y,self.width,self.height)
    def draw(self):
        self.painter.drawRect(self.rec)



        

        
