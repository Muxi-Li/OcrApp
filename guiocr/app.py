import os
from PyQt5.QtWidgets import QMainWindow,QFileDialog,QWidget,QLabel
from guiocr.widgets.main_window import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from guiocr.utils.ocr_utils import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fileName = ""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("OcrDemo_v1.0")
        self.ocrObj = OcrQt()
        # 按钮信号函数
        self.ui.btnOpenfile.clicked.connect(self.openFile)
        self.ui.btnStart.clicked.connect(self.ocrStart)


    def openFile(self):
        fileName,fileType = QFileDialog.getOpenFileName(self,"选取文件",os.getcwd(),"All Files(*);;Files(*.jpg)")
        self.fileName = str(fileName)
        image = QPixmap(fileName)
        w = image.width()
        h = image.height()
        self.qwidget = QWidget()
        # 设置尺寸不可改变
        self.qwidget.setFixedSize(w,h)
        self.label = QLabel(self.qwidget)
        self.label.setFixedSize(w,h)
        self.label.setPixmap(image)
        self.ui.scrollAreaCanvas.setWidget(self.label)
    
    def ocrStart(self):
        if self.fileName:
            self.ocrObj.set_task(self.fileName)
        self.ocrObj.start()
        self.ocrObj.show_result()
        

    


