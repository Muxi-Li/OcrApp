from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel

class LabelListWidget(QtWidgets.QListView):
    def __init__(self) -> None:
        super(LabelListWidget,self).__init__()
        # 设置内容模型
        self.slm = QStringListModel()
        self.list_result = ["测试1"]
        # 加载默认数据列表
        self.slm.setStringList(self.list_result)
        # 设置列表视图的模型
        self.setModel(self.slm)
        

