from ast import walk
import os
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QLabel, QButtonGroup, QListWidgetItem
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRect
from guiocr.widgets.main_window import Ui_MainWindow
from guiocr.widgets.canvas import Canvas
from guiocr import __appname__, __appversion__
from PyQt5.QtGui import QPixmap, QImage
from guiocr.utils.ocr_utils import *
# from guiocr.utils.shape import Rectangle
import PIL.Image
import io
here = os.path.dirname(__file__)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.fileName = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle(__appname__+'_'+__appversion__)
        self.ocrObj = OcrQt()
        self.canvas = Canvas()

        # 单选按钮组
        self.checBtnGroup = QButtonGroup(self)
        self.checBtnGroup.addButton(self.ui.checkBox_ocr)
        self.checBtnGroup.addButton(self.ui.checkBox_det)
        self.checBtnGroup.addButton(self.ui.checkBox_recog)
        self.checBtnGroup.addButton(self.ui.checkBox_layoutparser)
        self.checBtnGroup.setExclusive(True)

        # 添加按钮icon
        self.ui.btnOpenImg.setIcon(self.getIcon("open_img_grey"))
        self.ui.btnOpenDir.setIcon(self.getIcon("folder_open_grey"))
        self.ui.btnNext.setIcon(self.getIcon("next_grey"))
        self.ui.btnPrev.setIcon(self.getIcon("before_grey"))
        self.ui.btnAddShape.setIcon(self.getIcon("add_grey"))
        self.ui.btnEditShape.setIcon(self.getIcon("edit_grey"))
        self.ui.btnSaveAll.setIcon(self.getIcon("done_grey"))
        self.ui.btnBrightness.setIcon(self.getIcon("brightness_grey"))

        self.ui.scrollAreaCanvas.setWidget(self.canvas)

        # 信号与槽函数
        self.ui.btnOpenImg.clicked.connect(self.openFile)
        self.ui.btnOpenDir.clicked.connect(self.openDirDialog)
        self.ui.btnNext.clicked.connect(self.openNextImg)
        self.ui.btnPrev.clicked.connect(self.openPreImg)
        self.ui.btnStartProcess.clicked.connect(self.startProcess)
        self.ui.btnCopyAll.clicked.connect(self.copyToClipboard)
        self.ui.btnSaveAll.clicked.connect(self.saveToFile)
        self.ui.listWidgetResults.clicked.connect(self.onItemResultClicked)

        self.ui.listWidgetResults.clear()

    def onItemResultClicked(self):
        pass

    def saveToFile(self):
        pass

    def copyToClipboard(self):
        pass

    def startProcess(self):
        if self.fileName:
            self.ocrObj.set_task(self.fileName)
        self.ocrObj.start()
        self.ocr_result = self.ocrObj.result
        self.addOcrResult()

    def openPreImg(self):
        currIndex = self.imageList.index(self.fileName)
        if currIndex-1 >= 0:
            filename = self.imageList[currIndex-1]
            self.loadFile(filename)
        self.fileName = filename

    def openNextImg(self):
        filename = None
        if self.fileName is None:
            filename = self.imageList[0]
        else:
            currIndex = self.imageList.index(self.fileName)
            if currIndex + 1 < len(self.imageList):
                filename = self.imageList[currIndex+1]
            else:
                filename = self.imageList[-1]
        self.fileName = filename
        self.loadFile(self.fileName)

    def openDirDialog(self, dirpath=None):
        defaultOpenDirPath = dirpath if dirpath else "."
        targetDirPath = str(
            QFileDialog.getExistingDirectory(
                self,
                "Open Directory",
                defaultOpenDirPath,
                QFileDialog.ShowDirsOnly
            )
        )
        self.importDirImages(targetDirPath)

    def getIcon(self, iconName):
        self.icon_dir = os.path.join(here, "./icons")
        path = os.path.join(self.icon_dir, f"{iconName}.png")
        return QtGui.QIcon(path)

    def openFile(self):
        filename, fileType = QFileDialog.getOpenFileName(
            self, "选取文件", os.getcwd(), "All Files(*);;Files(*.jpg)")
        self.fileName = filename
        self.loadFile(filename)

    def importDirImages(self, dirpath):
        self.imageList = self.scanAllImages(dirpath)
        self.openNextImg()

    def scanAllImages(self, dirpath):
        images = []
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                relativePath = os.path.join(root, file)
                images.append(relativePath)
        return images

    def loadFile(self, filename=None):
        self.resetState()
        self.imageData = self.loadImageFile(filename)
        self.image = QImage.fromData(self.imageData)
        self.canvas.loadPixmap(QPixmap.fromImage(self.image))

    def resetState(self):
        # self.fileName = None
        self.imageData = None
        self.image = None
        self.canvas.resetState()

    def loadImageFile(self, filename):
        image_pil = PIL.Image.open(filename)
        with io.BytesIO() as f:
            image_pil.save(f, "JPEG")
            f.seek(0)
            return f.read()

    def addOcrResult(self):
        txts = [line[1][0] for line in self.ocr_result]
        boxes = [line[0] for line in self.ocr_result]
        shapes = []
        self.ui.listWidgetResults.clear()
        for i in range(len(txts)):
            x1 = boxes[i][0][0]
            y1 = boxes[i][0][1]
            x2 = boxes[i][2][0]
            y2 = boxes[i][2][1]
            rec = QRect(x1,y1,x2-x1,y2-y1)
            shapes.append(rec)
            self.addResultItem(txts[i],rec)
        self.canvas.loadShapes(shapes)
    def addResultItem(self, txt,rec):
        newItem = QListWidgetItem(txt, self.ui.listWidgetResults)
        newItem.setCheckState(Qt.Checked)
        newItem.setFlags(Qt.ItemIsEditable |
                         Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        self.ui.listWidgetResults.addItem(newItem)
