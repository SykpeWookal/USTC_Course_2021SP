import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QWidget
from QtDesignerFiles import WelcomeView
from LoginFile import LoginDialog
from FunctionFile import FunWindow
from PyQt5 import QtCore


class WelcomeWindow(QMainWindow):
    show_funcform_signal = QtCore.pyqtSignal()
    " The Entrance of the Main window"
    def __init__(self):
        #初始化入口，以下代码在例化时自动执行
        super().__init__()
        self.dialog = None
        self.db = None
        self.dbname = ''

        #WelcomeView的UI实例
        self.ui = WelcomeView.Ui_WelcomeView()
        #调用Ui_WelcomeView类中的方法,向主窗口中添加控件
        self.ui.setupUi(self)

        self.initBinding()
        #显示窗口
        #self.show()


    def initBinding(self):   #将welcome页面上的动作绑定到实现函数上，仅含登录操作。
        self.ui.actionLogin.triggered.connect(self.Login)
            #self.ui.actionLogout.triggered.connect(self.jumpToFunform)


    def Login(self):
        print("login")
        self.dialog = LoginDialog(self)
        self.dialog.exec_()

        if self.db != None:
            self.jumpToFunform()

    def jumpToFunform(self):
        self.show_funcform_signal.emit()









