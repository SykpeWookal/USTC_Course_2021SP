# import sys
# from PyQt5 import QtWidgets
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWidgets import QMainWindow
# from QtDesignerFiles.test import Ui_MainWindow
#
# class MyPyQT_Form(QMainWindow):
#     def __init__(self):
#         super(MyPyQT_Form,self).__init__()
#         self.ui = Ui_MainWindow()
#         self.ui.setupUi(self)
#         self.show()
#
#     #实现pushButton_click()函数，textEdit是文本框的id
#     def testbutton1(self):
#         self.ui.textEdit.setText("你点击了按钮")
#
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     w = MyPyQT_Form()
#     sys.exit(app.exec_())



import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from WelcomeWindow import WelcomeWindow
from FunctionFile import FunWindow


def show_funform():
    funform.db = mainform.db
    funform.dbname = mainform.dbname
    mainform.hide()
    funform.show()

def show_mainform():
    funform.db = None
    funform.dbname = None
    funform.hide()
    mainform.db = None
    mainform.dbname = None
    mainform.show()

if __name__=='__main__':
    app = QApplication(sys.argv)

    mainform = WelcomeWindow()
    mainform.show()
    funform = FunWindow()

    mainform.show_funcform_signal.connect(show_funform)
    funform.show_main_signal.connect(show_mainform)

    sys.exit(app.exec_())
