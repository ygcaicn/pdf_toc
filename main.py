#!/usr/bin/env python3
import sys
import os
import threading
import string
from random import sample

from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal, QTimer, QDateTime, QRect
from PyQt5.uic import loadUiType

from PyQt5.Qsci import QsciScintilla, QsciLexerPython

# 生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # 是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# 打包资源时添加path 相当于Pycharm中 mark Directory as sourceRoot
sys.path.append(resource_path('./resource'))

ui_file = resource_path('./pyqt5_ui/main.ui')
(class_ui, class_basic_class) = loadUiType(ui_file)


class CodeWidget(QsciScintilla):

    def __init__(self, parent=None):
        super(QsciScintilla, self).__init__(parent)

        self.setEolMode(self.SC_EOL_LF)    # 以\n换行
        self.setWrapMode(self.WrapWord)    # 自动换行。self.WrapWord是父类QsciScintilla的
        self.setAutoCompletionSource(self.AcsAll)  # 自动补全。对于所有Ascii字符
        self.setAutoCompletionCaseSensitivity(False)  # 自动补全大小写敏感
        self.setAutoCompletionThreshold(1)  # 输入多少个字符才弹出补全提示
        self.setFolding(True)  # 代码可折叠
        self.setFont(QFont('Consolas', 16))  # 设置默认字体
        # self.setMarginType(0, self.NumberMargin)    # 0~4。第0个左边栏显示行号
        # self.setMarginLineNumbers(0, True)  # 我也不知道
        # self.setMarginsBackgroundColor(QtGui.QColor(120, 220, 180))  # 边栏背景颜色
        # self.setMarginWidth(0, 30)  # 边栏宽度
        self.setAutoIndent(True)  # 换行后自动缩进
        self.setUtf8(True)  # 支持中文字符

class MainWindow(class_basic_class, class_ui):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setupUi(self)
        self.code = CodeWidget(self.centralwidget)

        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.addWidget(self.code, 0)


        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(
            Qt.CustomizeWindowHint | Qt.WindowCloseButtonHint)
        self.setFocus()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
