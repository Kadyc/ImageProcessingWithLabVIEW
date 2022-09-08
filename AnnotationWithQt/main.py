# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPainter, QPixmap, QPen
from PyQt5.QtCore import Qt, QPoint
import sys
from PIL import ImageQt, Image
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel

from FileTest import Ui_MainWindow

class MyLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.drawable = False

    # 是否允许作图
    def drawingPermission(self, a):
        if isinstance(a, bool):
            self.drawable = a

    # 初始化画布
    def initDrawing(self, img):
        self.pix = img  # 当前图
        self.tmpPix = self.pix.copy()  # 上一张图
        self.lastPoint = QPoint()
        self.endPoint = QPoint()

    def paintEvent(self, event):
        # 先执行父类方法，必须加上
        super().paintEvent(event)
        if self.drawable:
            pp = QPainter(self)
            pp.begin(self)
            pp.drawPixmap(0, 0, self.pix)
            pp.end()

    def mousePressEvent(self, event):
        # 先执行父类方法，可不加
        super().mousePressEvent(event)
        if self.drawable:
            # 鼠标左键按下
            if event.button() == Qt.LeftButton:
                self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        # 先执行父类方法，可不加
        super().mouseMoveEvent(event)
        if self.drawable:
            # 鼠标左键按下的同时移动鼠标
            if event.buttons() and Qt.LeftButton:
                self.endPoint = event.pos()

                # 当前图复制上一张图
                self.pix = self.tmpPix.copy()

                pp = QPainter(self.pix)
                pp.setPen(QPen(Qt.green, 5))
                pp.drawRect(self.lastPoint.x(), self.lastPoint.y(),
                            self.endPoint.x() - self.lastPoint.x(),
                            self.endPoint.y() - self.lastPoint.y())
                # 更新label
                self.update()

    def mouseReleaseEvent(self, event):
        # 先执行父类方法，可不加
        super().mouseReleaseEvent(event)
        if self.drawable:
            # 鼠标左键释放
            if event.button() == Qt.LeftButton:
                # 上一张图指向当前图
                self.tmpPix = self.pix

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 初始化label背景
        # img = Image.open(r'./1.jpg')
        # img = self.transImg(img)
        # self.label.setPixmap(img)
        # 设置当前不可作图
        self.flagPaint = False

        self.label = MyLabel()

        self.pushButton.clicked.connect(self.getImage)
        self.pushButton_2.clicked.connect(self.saveImage)

    def getImage(self):
        fdir, ftype = QFileDialog.getOpenFileName(self,
                                                  "Select Image",
                                                  "./",
                                                  "Image Files (*.png *.jpg)")
        # 把选择的图片展示在label上
        img = Image.open(fdir)
        img = self.transImg(img)
        self.label.setPixmap(img)

        # 初始化画布，允许作图
        self.label.initDrawing(img)
        self.label.drawingPermission(True)
        self.flagPaint = True

    def saveImage(self):
        if self.flagPaint:
            img = self.label.pix.toImage()
            # 该方法同上
            fdir, ftype = QFileDialog.getSaveFileName(self, "Save Image",
                                                      "./", "Image Files (*.jpg)")
            img.save(fdir)

    def transImg(self, img):
        '''
        use to trans PIL img to Qt img
        :param img: PIL object
        :return: Qt object
        '''
        img = img.resize((self.label.width(), self.label.height()))
        return ImageQt.toqpixmap(img)


if __name__ == "__main__":
    # 此句解决Qt Designer和Pycharm显示不同的问题
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())

