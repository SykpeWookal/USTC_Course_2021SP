import datetime
from QtDesignerFiles import function
from PyQt5.QtWidgets import QWidget,QHeaderView,QTableWidgetItem,QMessageBox
from PyQt5 import QtCore
import MySQLdb
from MySQLdb._exceptions import OperationalError
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

currentDate = datetime.datetime.now()
# print ("当前的日期和时间是 %s" % currentDate)
# print ("ISO格式的日期和时间是 %s" % currentDate.isoformat() )
# print ("当前的年份是 %s" %currentDate.year)
# print ("当前的月份是 %s" %currentDate.month)
# print ("当前的日期是  %s" %currentDate.day)
# print ("dd/mm/yyyy 格式是  %s/%s/%s" % (currentDate.day, currentDate.month, currentDate.year) )
# print ("当前小时是 %s" %currentDate.hour)
# print ("当前分钟是 %s" %currentDate.minute)
# print ("当前秒是  %s" %currentDate.second)

class FunWindow(QWidget):
    show_main_signal = QtCore.pyqtSignal()
    db = None
    dbname = ''
    #" The Entrance"
    # def __init__(self,parent):
    #     super(FunWindow, self).__init__(parent)
    #     self.parent = parent
    #     self.db = self.parent.db
    #     self.dbname = self.parent.dbname
    #
    #     self.ui = function.Ui_FunctionView()
    #     self.ui.setupUi(self)
    #     self.show()

    def __init__(self):
        super().__init__()
        self.ui = function.Ui_FunctionView()
        self.ui.setupUi(self)

        self.ui.KH_Table.setColumnCount(8) # 不设置不显示这些列
        self.ui.KH_Table.setHorizontalHeaderLabels(['客户身份证号', '客户姓名','客户联系电话','客户地址','联系人姓名','联系人手机号','联系人邮箱地址','联系人与客户关系'])
        self.ui.KH_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.KH_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        self.ui.ZH_CX_Table.setColumnCount(8) # 不设置不显示这些列
        self.ui.ZH_CX_Table.setHorizontalHeaderLabels(['账户号', '利率','货币类型','账户余额','开户日期','开户支行','所有者ID','最近访问日期'])
        self.ui.ZH_CX_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.ZH_CX_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        self.ui.ZH_ZP_Table.setColumnCount(7) # 不设置不显示这些列
        self.ui.ZH_ZP_Table.setHorizontalHeaderLabels(['账户号','透支额','账户余额','开户日期','开户支行','所有者ID','最近访问日期'])
        self.ui.ZH_ZP_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.ZH_ZP_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        self.ui.DK_Table.setColumnCount(8)
        self.ui.DK_Table.setHorizontalHeaderLabels(['贷款号','支行名','贷款总额','贷款客户号','发款日期','发款金额','未发款数','当前状态'])
        self.ui.DK_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.DK_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        self.initBinding()

        #为某些框设立正则表达式
        #email型输入
        regEAMIL = QRegExp('^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$')
        validatorEAMIL = QRegExpValidator(self)
        validatorEAMIL.setRegExp(regEAMIL)

        #date型输入，年月日格式
        regDATE = QRegExp('^[1-9][0-9][0-9][0-9]-((0([1-9]{1}))|(1[0|1|2]))-(([0-2]([1-9]{1}))|(3[0|1]))$')
        validatorDATE = QRegExpValidator(self)
        validatorDATE.setRegExp(regDATE)

        #电话匹配
        regPHONE = QRegExp('^[1-9][0-9]*$')
        validatorPHONE = QRegExpValidator(self)
        validatorPHONE.setRegExp(regPHONE)

        #浮点数匹配
        regFLOAT = QRegExp('^[-]{0,1}([1-9][0-9]*|0).[0-9]*$')
        validatorFLOAT = QRegExpValidator(self)
        validatorFLOAT.setRegExp(regFLOAT)

        #统一给输入框赋正则表达式
        self.ui.KH_L_Eamil.setValidator(validatorEAMIL)

        self.ui.ZH_ZP_Date.setValidator(validatorDATE)
        self.ui.ZH_CX_Date.setValidator(validatorDATE)
        self.ui.DK_ProvideDate.setValidator(validatorDATE)

        self.ui.KH_Phone.setValidator(validatorPHONE)
        self.ui.KH_L_Phone.setValidator(validatorPHONE)

        self.ui.ZH_CX_Rate.setValidator(validatorFLOAT)
        self.ui.ZH_CX_Balance.setValidator(validatorFLOAT)
        self.ui.ZH_ZP_Balance.setValidator(validatorFLOAT)
        self.ui.DK_TotalAmount.setValidator(validatorFLOAT)
        self.ui.DK_ProvideAmount.setValidator(validatorFLOAT)

    def initBinding(self):   #将welcome页面上的动作绑定到实现函数上，仅含登录操作。
        #ui = WelcomeView.Ui_WelcomeView()
        #关闭按钮绑定
        self.ui.pushButton_5.clicked.connect(self.jumpToMain)
        #客户管理绑定
        self.ui.KH_showallButton.clicked.connect(self.fun_KH_showallinfo)
        self.ui.KH_Add_Button.clicked.connect(self.fun_KH_Addinfo)
        self.ui.KH_Delete_Button.clicked.connect(self.fun_KH_Deleteinfo)
        self.ui.KH_Modify_Button.clicked.connect(self.fun_KH_Modifyinfo)
        self.ui.KH_Find_Button.clicked.connect(self.fun_KH_FindInfo)
        self.ui.KH_ExactFind_Button.clicked.connect(self.fun_KH_ExactFindInfo)
        self.ui.KH_FindZH_Button.clicked.connect(self.fun_KH_FindZH)
        self.ui.KH_FindLoan_Button.clicked.connect(self.fun_KH_FindDK)
        self.ui.KH_EXIT_Button.clicked.connect(self.jumpToMain)
        #账户管理绑定
        self.ui.ZH_showallButton.clicked.connect(self.fun_ZH_showallinfo)
        self.ui.ZH_Add_Button.clicked.connect(self.fun_ZH_Addinfo)
        self.ui.ZH_Delete_Button.clicked.connect(self.fun_ZH_Deleteinfo)
        self.ui.ZH_Modify_Button.clicked.connect(self.fun_ZH_Modifyinfo)
        self.ui.ZH_Find_Button.clicked.connect(self.fun_ZH_FindInfo)
        self.ui.ZH_ExactFind_Button.clicked.connect(self.fun_ZH_ExactFindInfo)
        self.ui.ZH_DELOwner_Button.clicked.connect(self.fun_ZH_DeleteOwner)
        self.ui.ZH_EXIT_Button.clicked.connect(self.jumpToMain)
        #贷款管理绑定
        self.ui.DK_showallButton.clicked.connect(self.fun_DK_showallinfo)
        self.ui.DK_Find_Button.clicked.connect(self.fun_DK_FindInfo)
        self.ui.DK_AddLoan_Button.clicked.connect(self.fun_DK_AddLoaninfo)
        self.ui.DK_AddProvide_Button.clicked.connect(self.fun_DK_AddProvideinfo)
        self.ui.DK_DeleteLoan_Button.clicked.connect(self.fun_DK_LoanDeleteinfo)
        self.ui.DK_EXIT_Button.clicked.connect(self.jumpToMain)
        #业务统计绑定
        self.ui.TJ_FK_Month_Button.clicked.connect(self.fun_TJ_FK_Month)
        self.ui.TJ_FK_Quarter_Button.clicked.connect(self.fun_TJ_FK_Quarter)
        self.ui.TJ_FK_Year_Button.clicked.connect(self.fun_TJ_FK_Year)
        self.ui.TJ_CX_Month_Button.clicked.connect(self.fun_TJ_CX_Month)
        self.ui.TJ_CX_Quarter_Button.clicked.connect(self.fun_TJ_CX_Quarter)
        self.ui.TJ_CX_Year_Button.clicked.connect(self.fun_TJ_CX_Year)
        self.ui.TJ_EXIT_Button.clicked.connect(self.jumpToMain)


    def jumpToMain(self):   #跳转到主界面
        self.show_main_signal.emit()
        self.ui.KH_Table.setRowCount(0)


    def fun_KH_showallinfo(self):
        self.ui.KH_Table.setRowCount(0)
        self.ui.KH_Table.setColumnCount(8) # 不设置不显示这些列
        self.ui.KH_Table.setHorizontalHeaderLabels(['客户身份证号', '客户姓名','客户联系电话','客户地址','联系人姓名','联系人手机号','联系人邮箱地址','联系人与客户关系'])
        self.ui.KH_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.KH_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")
        print("fun_KH_showallinfo")
        cur = self.db.cursor()
        sql = "select distinct * from 客户 left join 联系人 USING(客户身份证号)"
        cur.execute(sql)
        data = cur.fetchall()
        print(data)
        cur.close()

        currentRowCount = self.ui.KH_Table.rowCount()
        for i in data:
            self.ui.KH_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item4 = QTableWidgetItem(str(i[4]))
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            item5 = QTableWidgetItem(str(i[5]))
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            item6 = QTableWidgetItem(str(i[6]))
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            item7 = QTableWidgetItem(str(i[7]))
            item7.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.KH_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.KH_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.KH_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.KH_Table.setItem(currentRowCount, 3, item3) #列4
            self.ui.KH_Table.setItem(currentRowCount, 4, item4) #列5
            self.ui.KH_Table.setItem(currentRowCount, 5, item5) #列6
            self.ui.KH_Table.setItem(currentRowCount, 6, item6) #列7
            self.ui.KH_Table.setItem(currentRowCount, 7, item7) #列8

            currentRowCount += 1


    def fun_KH_FindInfo(self):
        self.ui.KH_Table.setRowCount(0)
        self.ui.KH_Table.setColumnCount(8) # 不设置不显示这些列
        self.ui.KH_Table.setHorizontalHeaderLabels(['客户身份证号', '客户姓名','客户联系电话','客户地址','联系人姓名','联系人手机号','联系人邮箱地址','联系人与客户关系'])
        self.ui.KH_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.KH_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")
        print("fun_KH_FindInfo")

        id = self.ui.KH_ID.text()
        name = self.ui.KH_Name.text()
        phone = self.ui.KH_Phone.text()
        addr = self.ui.KH_Addr.text()
        Lname = self.ui.KH_L_Name.text()
        Lphone =  self.ui.KH_L_Phone.text()
        Lrelationship = self.ui.KH_L_Relationship.text()
        Lemail = self.ui.KH_L_Eamil.text()

        name = name.replace("\'","\\\'")
        Lname = Lname.replace("\'","\\\'")

        condition = ''
        if id != '':
            condition = condition + " and 客户身份证号 like '%s'"%('%'+id+'%')
        if name != '':
            condition = condition + " and 客户.姓名 like '%s'"%('%'+name+'%')
        if phone != '':
            condition = condition + " and 客户.联系电话 like '%s'"%('%'+phone+'%')
        if addr != '':
            condition = condition + " and 客户.家庭住址 like '%s'"%('%'+addr+'%')
        if Lname != '':
            condition = condition + " and 联系人.姓名 like '%s'"%('%'+Lname+'%')
        if Lphone != '':
            condition = condition + " and 联系人.手机号 like '%s'"%('%'+Lphone+'%')
        if Lrelationship != '':
            condition = condition + " and 联系人.与客户关系 like '%s'"%('%'+Lrelationship+'%')
        if Lemail != '':
            condition = condition + " and 联系人.邮箱地址 like '%s'"%('%'+Lemail+'%')

        cur = self.db.cursor()
        sql = "select distinct * from 客户 left join 联系人 USING(客户身份证号) where 1 = 1" + condition
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
        print(data)
        cur.close()

        currentRowCount = self.ui.KH_Table.rowCount()
        for i in data:
            self.ui.KH_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item4 = QTableWidgetItem(str(i[4]))
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            item5 = QTableWidgetItem(str(i[5]))
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            item6 = QTableWidgetItem(str(i[6]))
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            item7 = QTableWidgetItem(str(i[7]))
            item7.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.KH_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.KH_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.KH_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.KH_Table.setItem(currentRowCount, 3, item3) #列4
            self.ui.KH_Table.setItem(currentRowCount, 4, item4) #列5
            self.ui.KH_Table.setItem(currentRowCount, 5, item5) #列6
            self.ui.KH_Table.setItem(currentRowCount, 6, item6) #列7
            self.ui.KH_Table.setItem(currentRowCount, 7, item7) #列8

            currentRowCount += 1


    def fun_KH_ExactFindInfo(self):
        self.ui.KH_Table.setRowCount(0)
        self.ui.KH_Table.setColumnCount(8) # 不设置不显示这些列
        self.ui.KH_Table.setHorizontalHeaderLabels(['客户身份证号', '客户姓名','客户联系电话','客户地址','联系人姓名','联系人手机号','联系人邮箱地址','联系人与客户关系'])
        self.ui.KH_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.KH_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")
        print("fun_KH_ExactFindInfo")

        id = self.ui.KH_ID.text()
        name = self.ui.KH_Name.text()
        phone = self.ui.KH_Phone.text()
        addr = self.ui.KH_Addr.text()
        Lname = self.ui.KH_L_Name.text()
        Lphone =  self.ui.KH_L_Phone.text()
        Lrelationship = self.ui.KH_L_Relationship.text()
        Lemail = self.ui.KH_L_Eamil.text()

        name = name.replace("\'","\\\'")
        Lname = Lname.replace("\'","\\\'")

        condition = ''
        if id != '':
            condition = condition + " and 客户身份证号 = '%s'"%(id)
        if name != '':
            condition = condition + " and 客户.姓名 = '%s'"%(name)
        if phone != '':
            condition = condition + " and 客户.联系电话 = '%s'"%(phone)
        if addr != '':
            condition = condition + " and 客户.家庭住址 = '%s'"%(addr)
        if Lname != '':
            condition = condition + " and 联系人.姓名 = '%s'"%(Lname)
        if Lphone != '':
            condition = condition + " and 联系人.手机号 = '%s'"%(Lphone)
        if Lrelationship != '':
            condition = condition + " and 联系人.与客户关系 = '%s'"%(Lrelationship)
        if Lemail != '':
            condition = condition + " and 联系人.邮箱地址 = '%s'"%(Lemail)

        cur = self.db.cursor()
        sql = "select distinct * from 客户 left join 联系人 USING(客户身份证号) where 1 = 1" + condition
        print(sql)
        cur.execute(sql)
        data = cur.fetchall()
        print(data)
        cur.close()

        currentRowCount = self.ui.KH_Table.rowCount()
        for i in data:
            self.ui.KH_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item4 = QTableWidgetItem(str(i[4]))
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            item5 = QTableWidgetItem(str(i[5]))
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            item6 = QTableWidgetItem(str(i[6]))
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            item7 = QTableWidgetItem(str(i[7]))
            item7.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.KH_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.KH_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.KH_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.KH_Table.setItem(currentRowCount, 3, item3) #列4
            self.ui.KH_Table.setItem(currentRowCount, 4, item4) #列5
            self.ui.KH_Table.setItem(currentRowCount, 5, item5) #列6
            self.ui.KH_Table.setItem(currentRowCount, 6, item6) #列7
            self.ui.KH_Table.setItem(currentRowCount, 7, item7) #列8

            currentRowCount += 1


    def fun_KH_Addinfo(self):
        #pass
        print("fun_KH_Addinfo")
        id = self.ui.KH_ID.text()
        name = self.ui.KH_Name.text()
        phone = self.ui.KH_Phone.text()
        addr = self.ui.KH_Addr.text()
        Lname = self.ui.KH_L_Name.text()
        Lphone =  self.ui.KH_L_Phone.text()
        Lrelationship = self.ui.KH_L_Relationship.text()
        Lemail = self.ui.KH_L_Eamil.text()

        name = name.replace("\"","\\\"")
        Lname = Lname.replace("\"","\\\"")
        # print(id)
        # print(name)
        # print(phone)
        # print(addr)
        if id == '':
            QMessageBox.information(self,'Message','请输入客户身份证号~', QMessageBox.Close, QMessageBox.Close)
            return
        try:
            cur = self.db.cursor()
            if name == '' and phone == '' and addr == '':
                print("仅添加联系人")
                sql = "insert into 联系人 value('%s',\"%s\", '%s', '%s', '%s');"%(id,Lname,Lphone,Lemail,Lrelationship)
                cur.execute(sql)
                QMessageBox.information(self,'Message','联系人信息已增加', QMessageBox.Close, QMessageBox.Close)
            else:
                print("添加客户与联系人")
                sql = "insert into 客户 value('%s', \"%s\", '%s', '%s');"%(id,name,phone,addr)
                cur.execute(sql)
                sql = "insert into 联系人 value('%s',\"%s\", '%s', '%s', '%s');"%(id,Lname,Lphone,Lemail,Lrelationship)
                cur.execute(sql)
                QMessageBox.information(self,'Message','客户信息与联系人已增加', QMessageBox.Close, QMessageBox.Close)
            cur.close()
            self.db.commit()
        except MySQLdb._exceptions.IntegrityError:
            QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
            self.db.rollback()
        except MySQLdb._exceptions.OperationalError:
            QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)
            self.db.rollback()


    def fun_KH_Deleteinfo(self):
        #pass
        print("fun_KH_Deleteinfo")
        id = self.ui.KH_ID.text()
        if id == '':
            QMessageBox.information(self,'Message','请输入身份证号', QMessageBox.Close, QMessageBox.Close)
            return
        try:
            cur = self.db.cursor()
            sql = "delete from 联系人 where 联系人.客户身份证号 = '%s';"%(id)
            cur.execute(sql)
            self.db.commit()
            sql = "delete from 客户 where 客户.客户身份证号 = '%s';"%(id)
            cur.execute(sql)
            self.db.commit()
            QMessageBox.information(self,'Message','客户信息已删除', QMessageBox.Close, QMessageBox.Close)
            cur.close()
        except MySQLdb._exceptions.IntegrityError:
            QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
            self.db.rollback()
        except MySQLdb._exceptions.OperationalError:
            QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)
            self.db.rollback()


    def fun_KH_Modifyinfo(self):
        #pass
        print("fun_KH_Modifyinfo")
        id = self.ui.KH_ID.text()
        name = self.ui.KH_Name.text()
        phone = self.ui.KH_Phone.text()
        addr = self.ui.KH_Addr.text()
        Lname = self.ui.KH_L_Name.text()
        Lphone =  self.ui.KH_L_Phone.text()
        Lrelationship = self.ui.KH_L_Relationship.text()
        Lemail = self.ui.KH_L_Eamil.text()

        NEWID = self.ui.KH_ModifyID.text()

        name = name.replace("\"","\\\"")
        #print(name)
        Lname = Lname.replace("\"","\\\"")

        if id == '':
            QMessageBox.information(self,'Message','请输入身份证号', QMessageBox.Close, QMessageBox.Close)
            return

        try:
            cur = self.db.cursor()
            if name != '':
                print("更新客户名称")
                sql = "update 客户 set 客户.姓名 = \"%s\" where 客户.客户身份证号 = '%s';"%(name,id)
                cur.execute(sql)
            if phone != '':
                print("更新客户联系电话")
                sql = "update 客户 set 客户.联系电话 = '%s' where 客户.客户身份证号 = '%s';"%(phone,id)
                cur.execute(sql)
            if addr != '':
                print("更新客户地址")
                sql = "update 客户 set 客户.家庭住址 = '%s' where 客户.客户身份证号 = '%s';"%(addr,id)
                cur.execute(sql)
            if Lname != '':
                print("更新联系人名称")
                sql = "update 联系人 set 联系人.姓名 = "'%s'" where 联系人.客户身份证号 = '%s';"%(Lname,id)
                cur.execute(sql)
            if Lphone != '':
                print("更新联系人电话")
                sql = "update 联系人 set 联系人.手机号 = '%s' where 联系人.客户身份证号 = '%s';"%(Lphone,id)
                cur.execute(sql)
            if Lemail != '':
                print("更新联系人邮箱")
                sql = "update 联系人 set 联系人.邮箱地址 = '%s' where 联系人.客户身份证号 = '%s';"%(Lemail,id)
                cur.execute(sql)
            if Lrelationship != '':
                print("更新联系人关系")
                sql = "update 联系人 set 联系人.与客户关系 = '%s' where 联系人.客户身份证号 = '%s';"%(Lrelationship,id)
                cur.execute(sql)
            if NEWID != '':
                print("更新客户ID")
                sql = "update 客户 set 客户.客户身份证号 = '%s' where 客户.客户身份证号 = '%s';"%(NEWID,id)
                cur.execute(sql)
            cur.close()
            QMessageBox.information(self,'Message','修改成功', QMessageBox.Close, QMessageBox.Close)
            self.db.commit()
        except MySQLdb._exceptions.IntegrityError:
            QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
            self.db.rollback()


    def fun_KH_FindZH(self):
        #pass
        print("fun_KH_FindZH")
        self.ui.KH_Table.setRowCount(0)
        self.ui.KH_Table.setColumnCount(9) # 不设置不显示这些列
        self.ui.KH_Table.setHorizontalHeaderLabels(['客户身份证号', '客户姓名','客户联系电话','客户地址','账户号','开户支行','最近访问日期','开户日期','账户余额'])
        self.ui.KH_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.KH_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        cur = self.db.cursor()
        sql = "(select 客户身份证号,姓名,联系电话,家庭住址,账户号,支行名,最近访问日期,开户日期,账户余额\
                from 客户 left join (储蓄账户访问时间 left join 储蓄账户 Using(账户号))Using(客户身份证号))\
               union\
                (select 客户身份证号,姓名,联系电话,家庭住址,账户号,支行名,最近访问日期,开户日期,账户余额\
                 from 客户 left join (支票账户访问时间 left join 支票账户 Using(账户号))Using(客户身份证号))"
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()


        currentRowCount = self.ui.KH_Table.rowCount()
        for i in data:
            self.ui.KH_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item4 = QTableWidgetItem(str(i[4]))
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            item5 = QTableWidgetItem(str(i[5]))
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            item6 = QTableWidgetItem(str(i[6]))
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            item7 = QTableWidgetItem(str(i[7]))
            item7.setTextAlignment(QtCore.Qt.AlignCenter)
            item8 = QTableWidgetItem(str(i[8]))
            item8.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.KH_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.KH_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.KH_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.KH_Table.setItem(currentRowCount, 3, item3) #列4
            self.ui.KH_Table.setItem(currentRowCount, 4, item4) #列5
            self.ui.KH_Table.setItem(currentRowCount, 5, item5) #列6
            self.ui.KH_Table.setItem(currentRowCount, 6, item6) #列7
            self.ui.KH_Table.setItem(currentRowCount, 7, item7) #列8
            self.ui.KH_Table.setItem(currentRowCount, 8, item8) #列8

            currentRowCount += 1


    def fun_KH_FindDK(self):
        #pass
        self.ui.KH_Table.setRowCount(0)
        print("fun_KH_FindDK")
        self.ui.KH_Table.setColumnCount(10) # 不设置不显示这些列
        self.ui.KH_Table.setHorizontalHeaderLabels(['客户身份证号', '客户姓名','客户联系电话','客户地址','贷款号','发款支行','贷款总额','未发款数','贷款状态','最近发款日期'])
        self.ui.KH_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.KH_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        cur = self.db.cursor()
        sql = "select 客户身份证号,姓名,联系电话,家庭住址,贷款号,支行名,贷款总金额,未发款数,贷款状态,最近发款日期\
                from (客户 left join 客户_贷款 Using(客户身份证号)) left join 贷款 Using(贷款号)"
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()


        currentRowCount = self.ui.KH_Table.rowCount()
        for i in data:
            self.ui.KH_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item4 = QTableWidgetItem(str(i[4]))
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            item5 = QTableWidgetItem(str(i[5]))
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            item6 = QTableWidgetItem(str(i[6]))
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            item7 = QTableWidgetItem(str(i[7]))
            item7.setTextAlignment(QtCore.Qt.AlignCenter)
            item8 = QTableWidgetItem(str(i[8]))
            item8.setTextAlignment(QtCore.Qt.AlignCenter)
            item9 = QTableWidgetItem(str(i[9]))
            item9.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.KH_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.KH_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.KH_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.KH_Table.setItem(currentRowCount, 3, item3) #列4
            self.ui.KH_Table.setItem(currentRowCount, 4, item4) #列5
            self.ui.KH_Table.setItem(currentRowCount, 5, item5) #列6
            self.ui.KH_Table.setItem(currentRowCount, 6, item6) #列7
            self.ui.KH_Table.setItem(currentRowCount, 7, item7) #列8
            self.ui.KH_Table.setItem(currentRowCount, 8, item8) #列9
            self.ui.KH_Table.setItem(currentRowCount, 9, item9) #列10

            currentRowCount += 1


    def fun_ZH_showallinfo(self):
        self.ui.ZH_CX_Table.setRowCount(0)
        self.ui.ZH_ZP_Table.setRowCount(0)

        print("fun_ZH_showallinfo")
        cur = self.db.cursor()
        if self.ui.ZH_tabWidget.currentIndex() == 0:#储蓄账户
            sql = "select distinct * from 储蓄账户 left join 储蓄账户访问时间 USING(账户号)"
            cur.execute(sql)
            data = cur.fetchall()
            print(data)
            cur.close()

            currentRowCount = self.ui.ZH_CX_Table.rowCount()
            for i in data:
                self.ui.ZH_CX_Table.insertRow(currentRowCount)

                item0 = QTableWidgetItem(str(i[0]))
                item0.setTextAlignment(QtCore.Qt.AlignCenter)
                item1 = QTableWidgetItem(str(i[1]))
                item1.setTextAlignment(QtCore.Qt.AlignCenter)
                item2 = QTableWidgetItem(str(i[2]))
                item2.setTextAlignment(QtCore.Qt.AlignCenter)
                item3 = QTableWidgetItem(str(i[3]))
                item3.setTextAlignment(QtCore.Qt.AlignCenter)
                item4 = QTableWidgetItem(str(i[4]))
                item4.setTextAlignment(QtCore.Qt.AlignCenter)
                item5 = QTableWidgetItem(str(i[5]))
                item5.setTextAlignment(QtCore.Qt.AlignCenter)
                item6 = QTableWidgetItem(str(i[6]))
                item6.setTextAlignment(QtCore.Qt.AlignCenter)
                item7 = QTableWidgetItem(str(i[7]))
                item7.setTextAlignment(QtCore.Qt.AlignCenter)
                # item8 = QTableWidgetItem(str(i[8]))
                # item8.setTextAlignment(QtCore.Qt.AlignCenter)

                self.ui.ZH_CX_Table.setItem(currentRowCount, 0, item0) #列1
                self.ui.ZH_CX_Table.setItem(currentRowCount, 1, item1) #列2
                self.ui.ZH_CX_Table.setItem(currentRowCount, 2, item2) #列3
                self.ui.ZH_CX_Table.setItem(currentRowCount, 3, item3) #列4
                self.ui.ZH_CX_Table.setItem(currentRowCount, 4, item4) #列5
                self.ui.ZH_CX_Table.setItem(currentRowCount, 5, item5) #列6
                self.ui.ZH_CX_Table.setItem(currentRowCount, 6, item6) #列7
                self.ui.ZH_CX_Table.setItem(currentRowCount, 7, item7) #列8
                # self.ui.ZH_CX_Table.setItem(currentRowCount, 8, item7) #列8
                currentRowCount += 1
        else:
            sql = "select distinct * from 支票账户 left join 支票账户访问时间 USING(账户号);"
            cur.execute(sql)
            data = cur.fetchall()
            print(data)
            cur.close()

            currentRowCount = self.ui.ZH_ZP_Table.rowCount()
            for i in data:
                self.ui.ZH_ZP_Table.insertRow(currentRowCount)

                item0 = QTableWidgetItem(str(i[0]))
                item0.setTextAlignment(QtCore.Qt.AlignCenter)
                item1 = QTableWidgetItem(str(i[1]))
                item1.setTextAlignment(QtCore.Qt.AlignCenter)
                item2 = QTableWidgetItem(str(i[2]))
                item2.setTextAlignment(QtCore.Qt.AlignCenter)
                item3 = QTableWidgetItem(str(i[3]))
                item3.setTextAlignment(QtCore.Qt.AlignCenter)
                item4 = QTableWidgetItem(str(i[4]))
                item4.setTextAlignment(QtCore.Qt.AlignCenter)
                item5 = QTableWidgetItem(str(i[5]))
                item5.setTextAlignment(QtCore.Qt.AlignCenter)
                item6 = QTableWidgetItem(str(i[6]))
                item6.setTextAlignment(QtCore.Qt.AlignCenter)
                #item7 = QTableWidgetItem(str(i[7]))
                #item7.setTextAlignment(QtCore.Qt.AlignCenter)
                # item8 = QTableWidgetItem(str(i[8]))
                # item8.setTextAlignment(QtCore.Qt.AlignCenter)

                self.ui.ZH_ZP_Table.setItem(currentRowCount, 0, item0) #列1
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 1, item1) #列2
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 2, item2) #列3
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 3, item3) #列4
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 4, item4) #列5
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 5, item5) #列6
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 6, item6) #列7
                #self.ui.ZH_ZP_Table.setItem(currentRowCount, 7, item7) #列8
                # self.ui.ZH_ZP_Table.setItem(currentRowCount, 8, item7) #列8
                currentRowCount += 1


    def fun_ZH_FindInfo(self):
        self.ui.ZH_CX_Table.setRowCount(0)
        self.ui.ZH_ZP_Table.setRowCount(0)
        print("fun_ZH_FindInfo")


        cur = self.db.cursor()
        if self.ui.ZH_tabWidget.currentIndex() == 0:#储蓄账户
            accountID = self.ui.ZH_CX_ID.text()
            ownerID = self.ui.ZH_CX_KHID.text()
            openBank = self.ui.ZH_CX_Bank.text()
            openDate = self.ui.ZH_CX_Date.text()
            rate = self.ui.ZH_CX_Rate.text()
            type = self.ui.ZH_CX_Type.text()
            balance = self.ui.ZH_CX_Balance.text()

            #name = name.replace("\'","\\\'")
            #Lname = Lname.replace("\'","\\\'")

            condition = ''
            if accountID != '':
                condition = condition + " and 账户号 like '%s'"%('%'+accountID+'%')
            if ownerID != '':
                condition = condition + " and 客户身份证号 like '%s'"%('%'+ownerID+'%')
            if openBank != '':
                condition = condition + " and 支行名 like '%s'"%('%'+openBank+'%')
            if openDate != '':
                condition = condition + " and 开户日期 like '%s'"%('%'+openDate+'%')
            if rate != '':
                condition = condition + " and 利率 like '%s'"%('%'+rate+'%')
            if type != '':
                condition = condition + " and 货币类型 like '%s'"%('%'+type+'%')
            if balance != '':
                condition = condition + " and 账户余额 like '%s'"%('%'+balance+'%')


            cur = self.db.cursor()
            sql = "select distinct * from 储蓄账户 left join 储蓄账户访问时间 USING(账户号) where 1 = 1" + condition
            print(sql)
            cur.execute(sql)
            data = cur.fetchall()
            print(data)
            cur.close()

            currentRowCount = self.ui.ZH_CX_Table.rowCount()
            for i in data:
                self.ui.ZH_CX_Table.insertRow(currentRowCount)

                item0 = QTableWidgetItem(str(i[0]))
                item0.setTextAlignment(QtCore.Qt.AlignCenter)
                item1 = QTableWidgetItem(str(i[1]))
                item1.setTextAlignment(QtCore.Qt.AlignCenter)
                item2 = QTableWidgetItem(str(i[2]))
                item2.setTextAlignment(QtCore.Qt.AlignCenter)
                item3 = QTableWidgetItem(str(i[3]))
                item3.setTextAlignment(QtCore.Qt.AlignCenter)
                item4 = QTableWidgetItem(str(i[4]))
                item4.setTextAlignment(QtCore.Qt.AlignCenter)
                item5 = QTableWidgetItem(str(i[5]))
                item5.setTextAlignment(QtCore.Qt.AlignCenter)
                item6 = QTableWidgetItem(str(i[6]))
                item6.setTextAlignment(QtCore.Qt.AlignCenter)
                item7 = QTableWidgetItem(str(i[7]))
                item7.setTextAlignment(QtCore.Qt.AlignCenter)

                self.ui.ZH_CX_Table.setItem(currentRowCount, 0, item0) #列1
                self.ui.ZH_CX_Table.setItem(currentRowCount, 1, item1) #列2
                self.ui.ZH_CX_Table.setItem(currentRowCount, 2, item2) #列3
                self.ui.ZH_CX_Table.setItem(currentRowCount, 3, item3) #列4
                self.ui.ZH_CX_Table.setItem(currentRowCount, 4, item4) #列5
                self.ui.ZH_CX_Table.setItem(currentRowCount, 5, item5) #列6
                self.ui.ZH_CX_Table.setItem(currentRowCount, 6, item6) #列7
                self.ui.ZH_CX_Table.setItem(currentRowCount, 7, item7) #列8

                currentRowCount += 1
        else:
            accountID = self.ui.ZH_ZP_ID.text()
            ownerID = self.ui.ZH_ZP_KHID.text()
            openBank = self.ui.ZH_ZP_Bank.text()
            openDate = self.ui.ZH_ZP_Date.text()
            overdraft = self.ui.ZH_ZP_Overdraft.text()
            balance = self.ui.ZH_ZP_Balance.text()

            #name = name.replace("\'","\\\'")
            #Lname = Lname.replace("\'","\\\'")

            condition = ''
            if accountID != '':
                condition = condition + " and 账户号 like '%s'"%('%'+accountID+'%')
            if ownerID != '':
                condition = condition + " and 客户身份证号 like '%s'"%('%'+ownerID+'%')
            if openBank != '':
                condition = condition + " and 支行名 like '%s'"%('%'+openBank+'%')
            if openDate != '':
                condition = condition + " and 开户日期 like '%s'"%('%'+openDate+'%')
            if overdraft != '':
                condition = condition + " and 透支额 like '%s'"%('%'+overdraft+'%')
            if balance != '':
                condition = condition + " and 账户余额 like '%s'"%('%'+balance+'%')


            cur = self.db.cursor()
            sql = "select distinct * from 支票账户 left join 支票账户访问时间 USING(账户号) where 1 = 1" + condition
            print(sql)
            cur.execute(sql)
            data = cur.fetchall()
            print(data)
            cur.close()

            currentRowCount = self.ui.ZH_ZP_Table.rowCount()
            for i in data:
                self.ui.ZH_ZP_Table.insertRow(currentRowCount)

                item0 = QTableWidgetItem(str(i[0]))
                item0.setTextAlignment(QtCore.Qt.AlignCenter)
                item1 = QTableWidgetItem(str(i[1]))
                item1.setTextAlignment(QtCore.Qt.AlignCenter)
                item2 = QTableWidgetItem(str(i[2]))
                item2.setTextAlignment(QtCore.Qt.AlignCenter)
                item3 = QTableWidgetItem(str(i[3]))
                item3.setTextAlignment(QtCore.Qt.AlignCenter)
                item4 = QTableWidgetItem(str(i[4]))
                item4.setTextAlignment(QtCore.Qt.AlignCenter)
                item5 = QTableWidgetItem(str(i[5]))
                item5.setTextAlignment(QtCore.Qt.AlignCenter)
                item6 = QTableWidgetItem(str(i[6]))
                item6.setTextAlignment(QtCore.Qt.AlignCenter)
                item7 = QTableWidgetItem(str(i[7]))
                item7.setTextAlignment(QtCore.Qt.AlignCenter)

                self.ui.ZH_ZP_Table.setItem(currentRowCount, 0, item0) #列1
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 1, item1) #列2
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 2, item2) #列3
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 3, item3) #列4
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 4, item4) #列5
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 5, item5) #列6
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 6, item6) #列7
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 7, item7) #列8

                currentRowCount += 1


    def fun_ZH_ExactFindInfo(self):
        self.ui.ZH_CX_Table.setRowCount(0)
        self.ui.ZH_ZP_Table.setRowCount(0)
        print("fun_ZH_FindInfo")


        cur = self.db.cursor()
        if self.ui.ZH_tabWidget.currentIndex() == 0:#储蓄账户
            accountID = self.ui.ZH_CX_ID.text()
            ownerID = self.ui.ZH_CX_KHID.text()
            openBank = self.ui.ZH_CX_Bank.text()
            openDate = self.ui.ZH_CX_Date.text()
            rate = self.ui.ZH_CX_Rate.text()
            type = self.ui.ZH_CX_Type.text()
            balance = self.ui.ZH_CX_Balance.text()

            #name = name.replace("\'","\\\'")
            #Lname = Lname.replace("\'","\\\'")

            condition = ''
            if accountID != '':
                condition = condition + " and 账户号 = '%s'"%(accountID)
            if ownerID != '':
                condition = condition + " and 客户身份证号 = '%s'"%(ownerID)
            if openBank != '':
                condition = condition + " and 支行名 = '%s'"%(openBank)
            if openDate != '':
                condition = condition + " and 开户日期 = '%s'"%(openDate)
            if rate != '':
                condition = condition + " and 利率 = '%s'"%(rate)
            if type != '':
                condition = condition + " and 货币类型 = '%s'"%(type)
            if balance != '':
                condition = condition + " and 账户余额 = '%s'"%(balance)


            cur = self.db.cursor()
            sql = "select distinct * from 储蓄账户 left join 储蓄账户访问时间 USING(账户号) where 1 = 1" + condition
            print(sql)
            cur.execute(sql)
            data = cur.fetchall()
            print(data)
            cur.close()

            currentRowCount = self.ui.ZH_CX_Table.rowCount()
            for i in data:
                self.ui.ZH_CX_Table.insertRow(currentRowCount)

                item0 = QTableWidgetItem(str(i[0]))
                item0.setTextAlignment(QtCore.Qt.AlignCenter)
                item1 = QTableWidgetItem(str(i[1]))
                item1.setTextAlignment(QtCore.Qt.AlignCenter)
                item2 = QTableWidgetItem(str(i[2]))
                item2.setTextAlignment(QtCore.Qt.AlignCenter)
                item3 = QTableWidgetItem(str(i[3]))
                item3.setTextAlignment(QtCore.Qt.AlignCenter)
                item4 = QTableWidgetItem(str(i[4]))
                item4.setTextAlignment(QtCore.Qt.AlignCenter)
                item5 = QTableWidgetItem(str(i[5]))
                item5.setTextAlignment(QtCore.Qt.AlignCenter)
                item6 = QTableWidgetItem(str(i[6]))
                item6.setTextAlignment(QtCore.Qt.AlignCenter)
                item7 = QTableWidgetItem(str(i[7]))
                item7.setTextAlignment(QtCore.Qt.AlignCenter)

                self.ui.ZH_CX_Table.setItem(currentRowCount, 0, item0) #列1
                self.ui.ZH_CX_Table.setItem(currentRowCount, 1, item1) #列2
                self.ui.ZH_CX_Table.setItem(currentRowCount, 2, item2) #列3
                self.ui.ZH_CX_Table.setItem(currentRowCount, 3, item3) #列4
                self.ui.ZH_CX_Table.setItem(currentRowCount, 4, item4) #列5
                self.ui.ZH_CX_Table.setItem(currentRowCount, 5, item5) #列6
                self.ui.ZH_CX_Table.setItem(currentRowCount, 6, item6) #列7
                self.ui.ZH_CX_Table.setItem(currentRowCount, 7, item7) #列8

                currentRowCount += 1
        else:
            accountID = self.ui.ZH_ZP_ID.text()
            ownerID = self.ui.ZH_ZP_KHID.text()
            openBank = self.ui.ZH_ZP_Bank.text()
            openDate = self.ui.ZH_ZP_Date.text()
            overdraft = self.ui.ZH_ZP_Overdraft.text()
            balance = self.ui.ZH_ZP_Balance.text()

            #name = name.replace("\'","\\\'")
            #Lname = Lname.replace("\'","\\\'")

            condition = ''
            if accountID != '':
                condition = condition + " and 账户号 = '%s'"%(accountID)
            if ownerID != '':
                condition = condition + " and 客户身份证号 = '%s'"%(ownerID)
            if openBank != '':
                condition = condition + " and 支行名 = '%s'"%(openBank)
            if openDate != '':
                condition = condition + " and 开户日期 = '%s'"%(openDate)
            if overdraft != '':
                condition = condition + " and 透支额 = '%s'"%(overdraft)
            if balance != '':
                condition = condition + " and 账户余额 = '%s'"%(balance)


            cur = self.db.cursor()
            sql = "select distinct * from 支票账户 left join 支票账户访问时间 USING(账户号) where 1 = 1" + condition
            print(sql)
            cur.execute(sql)
            data = cur.fetchall()
            print(data)
            cur.close()

            currentRowCount = self.ui.ZH_ZP_Table.rowCount()
            for i in data:
                self.ui.ZH_ZP_Table.insertRow(currentRowCount)

                item0 = QTableWidgetItem(str(i[0]))
                item0.setTextAlignment(QtCore.Qt.AlignCenter)
                item1 = QTableWidgetItem(str(i[1]))
                item1.setTextAlignment(QtCore.Qt.AlignCenter)
                item2 = QTableWidgetItem(str(i[2]))
                item2.setTextAlignment(QtCore.Qt.AlignCenter)
                item3 = QTableWidgetItem(str(i[3]))
                item3.setTextAlignment(QtCore.Qt.AlignCenter)
                item4 = QTableWidgetItem(str(i[4]))
                item4.setTextAlignment(QtCore.Qt.AlignCenter)
                item5 = QTableWidgetItem(str(i[5]))
                item5.setTextAlignment(QtCore.Qt.AlignCenter)
                item6 = QTableWidgetItem(str(i[6]))
                item6.setTextAlignment(QtCore.Qt.AlignCenter)
                item7 = QTableWidgetItem(str(i[7]))
                item7.setTextAlignment(QtCore.Qt.AlignCenter)

                self.ui.ZH_ZP_Table.setItem(currentRowCount, 0, item0) #列1
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 1, item1) #列2
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 2, item2) #列3
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 3, item3) #列4
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 4, item4) #列5
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 5, item5) #列6
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 6, item6) #列7
                self.ui.ZH_ZP_Table.setItem(currentRowCount, 7, item7) #列8

                currentRowCount += 1


    def fun_ZH_Addinfo(self):
        #pass
        if self.ui.ZH_tabWidget.currentIndex() == 0:#储蓄账户
            accountID = self.ui.ZH_CX_ID.text()
            ownerID = self.ui.ZH_CX_KHID.text()
            openBank = self.ui.ZH_CX_Bank.text()
            openDate = self.ui.ZH_CX_Date.text()
            rate = self.ui.ZH_CX_Rate.text()
            type = self.ui.ZH_CX_Type.text()
            balance = self.ui.ZH_CX_Balance.text()

            newOwnerID = self.ui.ZH_CX_NEWKHID.text()
            if accountID == '':
                QMessageBox.information(self,'Message','请输入账户号', QMessageBox.Close, QMessageBox.Close)
                return
            try:
                if newOwnerID == '':
                    print("添加账户")
                    cur = self.db.cursor()
                    #print(balance)
                    sql = "insert into 储蓄账户 value('%s', '%s', '%s', '%s','%s');"%(accountID,rate,type,balance,openDate)
                    cur.execute(sql)
                    #print(currentDate.year,currentDate.month,currentDate.day)
                    sql = "insert into 储蓄账户访问时间 value('%s','%s', '%s','%s-%s-%s');"%(openBank,ownerID,accountID,currentDate.year,currentDate.month,currentDate.day)
                    cur.execute(sql)
                    self.db.commit()
                    QMessageBox.information(self,'Message','储蓄账户信息已增加', QMessageBox.Close, QMessageBox.Close)
                    cur.close()
                else:
                    print("添加账户所有者")
                    cur = self.db.cursor()
                    sql = "select distinct 支行名 from 储蓄账户访问时间 where 账户号 = '%s';"%(accountID)
                    cur.execute(sql)
                    data = cur.fetchall()
                    #print(data[0][0])
                    sql = "insert into 储蓄账户访问时间 value('%s', '%s' , '%s','%s-%s-%s');"%(data[0][0],newOwnerID,accountID,currentDate.year,currentDate.month,currentDate.day)
                    cur.execute(sql)
                    self.db.commit()
                    QMessageBox.information(self,'Message','新的账户所有者已增加！', QMessageBox.Close, QMessageBox.Close)
                    cur.close()
            except MySQLdb._exceptions.IntegrityError:
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
            except MySQLdb._exceptions.OperationalError:
                QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
            except Exception as res:
                print(res)
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
        else:   #支票账户
            accountID = self.ui.ZH_ZP_ID.text()
            ownerID = self.ui.ZH_ZP_KHID.text()
            openBank = self.ui.ZH_ZP_Bank.text()
            openDate = self.ui.ZH_ZP_Date.text()
            overdraft = self.ui.ZH_ZP_Overdraft.text()
            balance = self.ui.ZH_ZP_Balance.text()

            newOwnerID = self.ui.ZH_ZP_NEWKHID.text()
            try:
                if newOwnerID == '':
                    print("添加支票账户")
                    cur = self.db.cursor()
                    sql = "insert into 支票账户 value('%s', '%s', '%s','%s');"%(accountID,overdraft,balance,openDate)
                    cur.execute(sql)
                    #print(currentDate.year,currentDate.month,currentDate.day)
                    sql = "insert into 支票账户访问时间 value('%s','%s','%s','%s-%s-%s');"%(openBank,ownerID,accountID,currentDate.year,currentDate.month,currentDate.day)
                    cur.execute(sql)
                    QMessageBox.information(self,'Message','支票账户信息已增加', QMessageBox.Close, QMessageBox.Close)
                    cur.close()
                    self.db.commit()
                else:
                    print("添加账户所有者")
                    cur = self.db.cursor()
                    sql = "select distinct 支行名 from 支票账户访问时间 where 账户号 = '%s';"%(accountID)
                    cur.execute(sql)
                    data = cur.fetchall()
                    #print(data[0][0])
                    sql = "insert into 支票账户访问时间 value('%s', '%s' , '%s','%s-%s-%s');"%(data[0][0],newOwnerID,accountID,currentDate.year,currentDate.month,currentDate.day)
                    cur.execute(sql)
                    self.db.commit()
                    QMessageBox.information(self,'Message','新的账户所有者已增加！', QMessageBox.Close, QMessageBox.Close)
                    cur.close()
            except MySQLdb._exceptions.IntegrityError:
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
            except MySQLdb._exceptions.OperationalError:
                QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
            except Exception as res:
                print(res)
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()


    def fun_ZH_Deleteinfo(self):
        #pass
        print("fun_ZH_Deleteinfo")
        if self.ui.ZH_tabWidget.currentIndex() == 0:#储蓄账户
            id = self.ui.ZH_CX_ID.text()
            if id == '':
                QMessageBox.information(self,'Message','请输入账户号', QMessageBox.Close, QMessageBox.Close)
                return
            try:
                cur = self.db.cursor()
                sql = "delete from 储蓄账户访问时间 where 储蓄账户访问时间.账户号 = '%s';"%(id)
                cur.execute(sql)
                sql = "delete from 储蓄账户 where 储蓄账户.账户号 = '%s';"%(id)
                cur.execute(sql)
                self.db.commit()
                QMessageBox.information(self,'Message','储蓄账户信息已删除', QMessageBox.Close, QMessageBox.Close)
                cur.close()
            except MySQLdb._exceptions.IntegrityError:
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
            except MySQLdb._exceptions.OperationalError:
                QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)
        else:#支票账户删除
            id = self.ui.ZH_ZP_ID.text()
            if id == '':
                QMessageBox.information(self,'Message','请输入账户号', QMessageBox.Close, QMessageBox.Close)
                return
            try:
                cur = self.db.cursor()
                sql = "delete from 支票账户访问时间 where 支票账户访问时间.账户号 = '%s';"%(id)
                cur.execute(sql)
                sql = "delete from 支票账户 where 支票账户.账户号 = '%s';"%(id)
                cur.execute(sql)
                self.db.commit()
                QMessageBox.information(self,'Message','支票账户信息已删除', QMessageBox.Close, QMessageBox.Close)
                cur.close()
            except MySQLdb._exceptions.IntegrityError:
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
            except MySQLdb._exceptions.OperationalError:
                QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)


    def fun_ZH_DeleteOwner(self):
        #pass
        print("fun_ZH_DeleteOwner")


        if self.ui.ZH_tabWidget.currentIndex() == 0:#储蓄账户
            id = self.ui.ZH_CX_ID.text()
            ownerCX = self.ui.ZH_CX_NEWKHID.text()
            if id == '':
                QMessageBox.information(self,'Message','请输入账户号', QMessageBox.Close, QMessageBox.Close)
                return
            if ownerCX == '':
                QMessageBox.information(self,'Message','请输入要删除的所有者ID', QMessageBox.Close, QMessageBox.Close)
                return
            try:
                cur = self.db.cursor()
                sql = "delete from 储蓄账户访问时间 where 账户号 = '%s' and 客户身份证号 = '%s';"%(id,ownerCX)
                cur.execute(sql)

                QMessageBox.information(self,'Message','储蓄账户所有者信息已删除', QMessageBox.Close, QMessageBox.Close)
                cur.close()
                self.db.commit()
            except MySQLdb._exceptions.IntegrityError:
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
            except MySQLdb._exceptions.OperationalError:
                QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
        else:#支票账户删除
            id = self.ui.ZH_ZP_ID.text()
            ownerZP = self.ui.ZH_ZP_NEWKHID.text()
            if id == '':
                QMessageBox.information(self,'Message','请输入账户号', QMessageBox.Close, QMessageBox.Close)
                return
            if ownerZP == '':
                QMessageBox.information(self,'Message','请输入要删除的所有者ID', QMessageBox.Close, QMessageBox.Close)
                return
            try:
                cur = self.db.cursor()
                sql = "delete from 支票账户访问时间 where 账户号 = '%s' and 客户身份证号 = '%s';"%(id,ownerZP)
                cur.execute(sql)

                QMessageBox.information(self,'Message','支票账户所有者信息已删除', QMessageBox.Close, QMessageBox.Close)
                cur.close()
                self.db.commit()
            except MySQLdb._exceptions.IntegrityError:
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
            except MySQLdb._exceptions.OperationalError:
                QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()


    def fun_ZH_Modifyinfo(self):
        #pass
        print("fun_ZH_Modifyinfo")
        if self.ui.ZH_tabWidget.currentIndex() == 0:#储蓄账户
            accountID = self.ui.ZH_CX_ID.text()
            ownerID = self.ui.ZH_CX_KHID.text()
            openBank = self.ui.ZH_CX_Bank.text()
            openDate = self.ui.ZH_CX_Date.text()
            rate = self.ui.ZH_CX_Rate.text()
            type = self.ui.ZH_CX_Type.text()
            balance = self.ui.ZH_CX_Balance.text()

            newOwnerID = self.ui.ZH_CX_NEWKHID.text()

            if accountID == '':
                QMessageBox.information(self,'Message','请输入账户号', QMessageBox.Close, QMessageBox.Close)
                return
            try:
                cur = self.db.cursor()
                if newOwnerID != '' and ownerID != '':
                    print("变更账户所有者")
                    sql = "update 储蓄账户访问时间 set 储蓄账户访问时间.客户身份证号 = '%s' where 储蓄账户访问时间.账户号 = '%s' and 储蓄账户访问时间.客户身份证号 = '%s';"%(newOwnerID,accountID,ownerID)
                    cur.execute(sql)
                # if newOwnerID == '' and ownerID != '':
                #     print("新增账户所有者")
                #     sql =
                #     sql = "insert into 储蓄账户访问时间 value('Bank1', 'C1' , 'CX01','2020-01-02');" \
                #            "update 储蓄账户访问时间 set 储蓄账户访问时间.客户身份证号 = '%s' where 储蓄账户访问时间.账户号 = '%s';"%(ownerID,accountID)
                #     cur.execute(sql)
                if openBank != '':
                    print("更新开户支行")
                    sql = "update 储蓄账户访问时间 set 储蓄账户访问时间.支行名 = '%s' where 储蓄账户访问时间.账户号 = '%s';"%(openBank,accountID)
                    cur.execute(sql)
                if openDate != '':
                    print("更新开户日期")
                    sql = "update 储蓄账户 set 储蓄账户.开户日期 = '%s' where 储蓄账户.账户号 = '%s';"%(openDate,accountID)
                    cur.execute(sql)
                if rate != '':
                    print("更新利率")
                    sql = "update 储蓄账户 set 储蓄账户.利率 = '%s' where 储蓄账户.账户号 = '%s';"%(rate,accountID)
                    cur.execute(sql)
                if type != '':
                    print("更新货币类型")
                    sql = "update 储蓄账户 set 储蓄账户.货币类型 = '%s' where 储蓄账户.账户号 = '%s';"%(type,accountID)
                    cur.execute(sql)
                if balance != '':
                    print("更新账户余额")
                    sql = "update 储蓄账户 set 储蓄账户.账户余额 = '%s' where 储蓄账户.账户号 = '%s';"%(balance,accountID)
                    cur.execute(sql)
                #最后commit一次
                self.db.commit()
                cur.close()
                QMessageBox.information(self,'Message','修改成功', QMessageBox.Close, QMessageBox.Close)
            except MySQLdb._exceptions.IntegrityError:
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
            except Exception as res:
                print(res)

        else:   #支票账户修改
            accountID = self.ui.ZH_ZP_ID.text()
            ownerID = self.ui.ZH_ZP_KHID.text()
            openBank = self.ui.ZH_ZP_Bank.text()
            openDate = self.ui.ZH_ZP_Date.text()
            overdraft = self.ui.ZH_ZP_Overdraft.text()
            balance = self.ui.ZH_ZP_Balance.text()

            newOwnerID = self.ui.ZH_ZP_NEWKHID.text()

            if accountID == '':
                QMessageBox.information(self,'Message','请输入账户号', QMessageBox.Close, QMessageBox.Close)
                return
            try:
                cur = self.db.cursor()
                if newOwnerID != '' and ownerID != '':
                    print("变更账户所有者")
                    sql = "update 支票账户访问时间 set 客户身份证号 = '%s' where 账户号 = '%s' and 客户身份证号 = '%s';"%(newOwnerID,accountID,ownerID)
                    cur.execute(sql)
                # if ownerID != '':
                #     print("更新账户所有者")
                #     sql = "update 支票账户访问时间 set 支票账户访问时间.客户身份证号 = '%s' where 支票账户访问时间.账户号 = '%s';"%(ownerID,accountID)
                #     cur.execute(sql)
                if openBank != '':
                    print("更新开户支行")
                    sql = "update 支票账户访问时间 set 支票账户访问时间.支行名 = '%s' where 支票账户访问时间.账户号 = '%s';"%(openBank,accountID)
                    cur.execute(sql)
                if openDate != '':
                    print("更新开户日期")
                    sql = "update 支票账户 set 支票账户.开户日期 = '%s' where 支票账户.账户号 = '%s';"%(openDate,accountID)
                    cur.execute(sql)
                if overdraft != '':
                    print("更新透支额度")
                    sql = "update 支票账户 set 支票账户.利率 = '%s' where 支票账户.账户号 = '%s';"%(overdraft,accountID)
                    cur.execute(sql)
                if balance != '':
                    print("更新账户余额")
                    sql = "update 支票账户 set 支票账户.账户余额 = '%s' where 支票账户.账户号 = '%s';"%(balance,accountID)
                    cur.execute(sql)
                #最后commit一次
                self.db.commit()
                cur.close()
                QMessageBox.information(self,'Message','修改成功', QMessageBox.Close, QMessageBox.Close)
            except MySQLdb._exceptions.IntegrityError:
                QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
            except Exception as res:
                print(res)


    def fun_DK_showallinfo(self):
        self.ui.DK_Table.setRowCount(0)
        print("fun_DK_showallinfo")
        cur = self.db.cursor()
        sql = "select 贷款号,支行名,贷款总金额,客户身份证号,发款日期,发款金额,发款.未发款数,贷款状态 from (贷款 left join 客户_贷款 USING(贷款号))left join 发款 USING(贷款号);"
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()

        currentRowCount = self.ui.DK_Table.rowCount()
        for i in data:
            self.ui.DK_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item4 = QTableWidgetItem(str(i[4]))
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            item5 = QTableWidgetItem(str(i[5]))
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            item6 = QTableWidgetItem(str(i[6]))
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            item7 = QTableWidgetItem(str(i[7]))
            item7.setTextAlignment(QtCore.Qt.AlignCenter)


            self.ui.DK_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.DK_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.DK_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.DK_Table.setItem(currentRowCount, 3, item3) #列4
            self.ui.DK_Table.setItem(currentRowCount, 4, item4) #列5
            self.ui.DK_Table.setItem(currentRowCount, 5, item5) #列6
            self.ui.DK_Table.setItem(currentRowCount, 6, item6) #列7
            self.ui.DK_Table.setItem(currentRowCount, 7, item7) #列8

            currentRowCount += 1


    def fun_DK_FindInfo(self):
        self.ui.DK_Table.setRowCount(0)
        print("fun_DK_FindInfo")
        cur = self.db.cursor()

        dkid = self.ui.DK_ID.text()
        total_amount = self.ui.DK_TotalAmount.text()
        bank = self.ui.DK_Bank.text()
        khid = self.ui.DK_KHID.text()
        fk_amount = self.ui.DK_ProvideAmount.text()
        fk_date = self.ui.DK_ProvideDate.text()

        condition = ''
        if dkid != '':
            condition = condition + " and 贷款号 like '%s'"%('%'+dkid+'%')
        if total_amount != '':
            condition = condition + " and 贷款总金额 like '%s'"%('%'+total_amount+'%')
        if bank != '':
            condition = condition + " and 支行名 like '%s'"%('%'+bank+'%')
        if khid != '':
            condition = condition + " and 客户身份证号 like '%s'"%('%'+khid+'%')
        if fk_amount != '':
            condition = condition + " and 发款金额 like '%s'"%('%'+fk_amount+'%')
        if fk_date != '':
            condition = condition + " and 发款日期 like '%s'"%('%'+fk_date+'%')


        sql = "select 贷款号,支行名,贷款总金额,客户身份证号,发款日期,发款金额,发款.未发款数,贷款状态 " \
              "from (贷款 left join 客户_贷款 USING(贷款号))left join 发款 USING(贷款号)" \
              "where 1 = 1" + condition
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()

        currentRowCount = self.ui.DK_Table.rowCount()
        for i in data:
            self.ui.DK_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item4 = QTableWidgetItem(str(i[4]))
            item4.setTextAlignment(QtCore.Qt.AlignCenter)
            item5 = QTableWidgetItem(str(i[5]))
            item5.setTextAlignment(QtCore.Qt.AlignCenter)
            item6 = QTableWidgetItem(str(i[6]))
            item6.setTextAlignment(QtCore.Qt.AlignCenter)
            item7 = QTableWidgetItem(str(i[7]))
            item7.setTextAlignment(QtCore.Qt.AlignCenter)


            self.ui.DK_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.DK_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.DK_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.DK_Table.setItem(currentRowCount, 3, item3) #列4
            self.ui.DK_Table.setItem(currentRowCount, 4, item4) #列5
            self.ui.DK_Table.setItem(currentRowCount, 5, item5) #列6
            self.ui.DK_Table.setItem(currentRowCount, 6, item6) #列7
            self.ui.DK_Table.setItem(currentRowCount, 7, item7) #列8

            currentRowCount += 1


    def fun_DK_AddLoaninfo(self):
        #pass
        print("fun_DK_AddLoaninfo")
        dkid = self.ui.DK_ID.text()
        total_amount = self.ui.DK_TotalAmount.text()
        bank = self.ui.DK_Bank.text()
        khid = self.ui.DK_KHID.text()
        if dkid == '' or khid == '':
            QMessageBox.information(self,'Message','添加操作请输入贷款号和客户号~', QMessageBox.Close, QMessageBox.Close)
            return
        try:
            cur = self.db.cursor()
            sql = "select * from 贷款 where 贷款号 = '%s'"%(dkid)
            cur.execute(sql)
            data = cur.fetchall()
            print(data)
            if len(data) == 0:
                print("添加新的贷款信息")
                sql = "insert into 贷款 value('%s', '%s', '%s', '%s', '%s', '%s');"%(dkid,bank,total_amount,total_amount,"未发放",'1000-01-01')
                cur.execute(sql)
                sql = "insert into 客户_贷款 value('%s', '%s');"%(khid,dkid)
                cur.execute(sql)
                QMessageBox.information(self,'Message','新的贷款信息已添加！', QMessageBox.Close, QMessageBox.Close)
                cur.close()
                self.db.commit()
            else:
                print("现有贷款添加所有者")
                sql = "insert into 客户_贷款 value('%s', '%s');"%(khid,dkid)
                cur.execute(sql)
                QMessageBox.information(self,'Message','现有贷款已添加新的所有者！', QMessageBox.Close, QMessageBox.Close)
                cur.close()
                self.db.commit()
        except MySQLdb._exceptions.IntegrityError:
            QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
            self.db.rollback()
        except MySQLdb._exceptions.OperationalError:
            QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)
            self.db.rollback()


    def fun_DK_AddProvideinfo(self):
        #pass
        print("fun_DK_AddProvideinfo")
        dkid = self.ui.DK_ID.text()
        provide_amount = self.ui.DK_ProvideAmount.text()
        provide_date = self.ui.DK_ProvideDate.text()

        try:
            cur = self.db.cursor()

            sql = "insert into 发款 (贷款号,发款日期,发款金额)value('%s','%s','%s');"%(dkid,provide_date,provide_amount)
            cur.execute(sql)
            QMessageBox.information(self,'Message','新的放款信息已添加！', QMessageBox.Close, QMessageBox.Close)
            self.db.commit()

            cur.close()
        except MySQLdb._exceptions.IntegrityError:
            QMessageBox.information(self,'Message','无效操作(完整性约束不满足)', QMessageBox.Close, QMessageBox.Close)
            self.db.rollback()
        # except MySQLdb._exceptions.OperationalError:
        #     QMessageBox.information(self,'Message','无效操作', QMessageBox.Close, QMessageBox.Close)
        except Exception as res:
            #print(res.args[0])
            if(res.args[0] == 1054):
                QMessageBox.information(self,'Message','发款金额超过未发总额，请检查发款金额', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()
            elif(res.args[0] == 1136):
                QMessageBox.information(self,'Message','发款日期早于上一次发款日期，请检查发款日期', QMessageBox.Close, QMessageBox.Close)
                self.db.rollback()


    def fun_DK_LoanDeleteinfo(self):
        #pass
        print("fun_DK_LoanDeleteinfo")
        dkid = self.ui.DK_ID.text()
        if dkid == '':
            QMessageBox.information(self,'Message','请输入待删除的贷款号', QMessageBox.Close, QMessageBox.Close)
            return

        cur = self.db.cursor()

        sql = "call delete_LoanInfo('%s',@TEST);"%(dkid)
        cur.execute(sql)
        sql = "SELECT @TEST;"
        cur.execute(sql)
        data = cur.fetchone()
        state = data[0]
        #print(state)

        if state == 0:
            QMessageBox.information(self,'Message','贷款信息已删除', QMessageBox.Close, QMessageBox.Close)
            self.db.commit()
        elif state == 1:
            QMessageBox.information(self,'Message','贷款号未找到', QMessageBox.Close, QMessageBox.Close)
        else:
            QMessageBox.information(self,'Message','发放中的贷款不允许删除！', QMessageBox.Close, QMessageBox.Close)

        cur.close()



    def fun_TJ_FK_Month(self):
        self.ui.TJ_Table.setRowCount(0)
        self.ui.TJ_Table.setColumnCount(4) # 不设置不显示这些列
        self.ui.TJ_Table.setHorizontalHeaderLabels(['支行名', '月份','发款次数','发款总额'])
        self.ui.TJ_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.TJ_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        cur = self.db.cursor()
        sql = "select 支行名,DATE_FORMAT(发款日期,'%Y-%m') 月份,count(发款日期) 发款次数 ,SUM(发款金额) 发款总额 from (select 支行名,贷款号,发款日期,发款金额 from (支行 left join 贷款 Using(支行名)) left join 发款 Using(贷款号)) C1 group by 支行名,月份;"
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()

        currentRowCount = self.ui.TJ_Table.rowCount()
        for i in data:
            self.ui.TJ_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.TJ_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.TJ_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.TJ_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.TJ_Table.setItem(currentRowCount, 3, item3) #列4

            currentRowCount += 1


    def fun_TJ_FK_Quarter(self):
        self.ui.TJ_Table.setRowCount(0)
        self.ui.TJ_Table.setColumnCount(5) # 不设置不显示这些列
        self.ui.TJ_Table.setHorizontalHeaderLabels(['支行名', '年度','季度','发款次数','发款总额'])
        self.ui.TJ_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.TJ_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        cur = self.db.cursor()
        sql = "select 支行名, DATE_FORMAT(发款日期,'%Y')年度, QUARTER(发款日期)季度, count(发款日期) 发款次数 ,SUM(发款金额) 发款总额\
                from (select 支行名,贷款号,发款日期,发款金额 from (支行 left join 贷款 Using(支行名)) left join 发款 Using(贷款号)) C1\
                group by 支行名,年度,季度;"
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()

        currentRowCount = self.ui.TJ_Table.rowCount()
        for i in data:
            self.ui.TJ_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item4 = QTableWidgetItem(str(i[4]))
            item4.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.TJ_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.TJ_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.TJ_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.TJ_Table.setItem(currentRowCount, 3, item3) #列4
            self.ui.TJ_Table.setItem(currentRowCount, 4, item4) #列5

            currentRowCount += 1


    def fun_TJ_FK_Year(self):
        self.ui.TJ_Table.setRowCount(0)
        self.ui.TJ_Table.setColumnCount(4) # 不设置不显示这些列
        self.ui.TJ_Table.setHorizontalHeaderLabels(['支行名', '月份','发款次数','发款总额'])
        self.ui.TJ_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.TJ_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        cur = self.db.cursor()
        sql = "select 支行名,DATE_FORMAT(发款日期,'%Y')年度,count(发款日期) 发款次数 ,SUM(发款金额) 发款总额\
                from (select 支行名,贷款号,发款日期,发款金额 from (支行 left join 贷款 Using(支行名)) left join 发款 Using(贷款号)) C1\
                group by 支行名,年度;"
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()

        currentRowCount = self.ui.TJ_Table.rowCount()
        for i in data:
            self.ui.TJ_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.TJ_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.TJ_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.TJ_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.TJ_Table.setItem(currentRowCount, 3, item3) #列4

            currentRowCount += 1


    def fun_TJ_CX_Month(self):
        self.ui.TJ_Table.setRowCount(0)
        self.ui.TJ_Table.setColumnCount(4) # 不设置不显示这些列
        self.ui.TJ_Table.setHorizontalHeaderLabels(['支行名', '月份','新增客户人数','新增存储'])
        self.ui.TJ_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.TJ_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        cur = self.db.cursor()
        sql = "select S1.支行名, S1.月份, 新增客户人数, 存储总额\
                from\
                    (select 支行名, DATE_FORMAT(开户日期,'%Y-%m') 月份, SUM(账户余额) 存储总额\
	                from (\
                    (select distinct 支行名,账户号,账户余额,开户日期\
			        from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))\
			        Union\
			        (select distinct 支行名,账户号,账户余额,开户日期\
			        from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1\
	                group by 支行名,月份) S1,\
                    (\
	                select 支行名,DATE_FORMAT(开户日期,'%Y-%m') 月份, count(distinct 客户身份证号) 新增客户人数 \
	                from (\
                    (select 支行名,账户号,账户余额,开户日期,客户身份证号\
			        from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))\
			        Union\
			        (select 支行名,账户号,账户余额,开户日期,客户身份证号\
			        from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1\
	                group by 支行名,月份) S2\
                where S1.支行名 = S2.支行名 and S1.月份 = S2.月份;"
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()

        currentRowCount = self.ui.TJ_Table.rowCount()
        for i in data:
            self.ui.TJ_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.TJ_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.TJ_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.TJ_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.TJ_Table.setItem(currentRowCount, 3, item3) #列4

            currentRowCount += 1


    def fun_TJ_CX_Quarter(self):
        self.ui.TJ_Table.setRowCount(0)
        self.ui.TJ_Table.setColumnCount(5) # 不设置不显示这些列
        self.ui.TJ_Table.setHorizontalHeaderLabels(['支行名', '年度','季度','新增客户人数','发款总额'])
        self.ui.TJ_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.TJ_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        cur = self.db.cursor()
        sql = "select S1.支行名, S1.年度, S1.季度, 新增客户人数, 存储总额\
                from\
                (select 支行名, DATE_FORMAT(开户日期,'%Y') 年度, QUARTER(开户日期)季度, SUM(账户余额) 存储总额\
	            from ((select distinct 支行名,账户号,账户余额,开户日期\
			    from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))\
			    Union\
			    (select distinct 支行名,账户号,账户余额,开户日期\
			    from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1\
	            group by 支行名,年度,季度) S1,\
                (\
	            select 支行名,DATE_FORMAT(开户日期,'%Y') 年度, QUARTER(开户日期)季度, count(distinct 客户身份证号) 新增客户人数 \
	            from ((select 支行名,账户号,账户余额,开户日期,客户身份证号\
			    from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))\
			    Union\
			    (select 支行名,账户号,账户余额,开户日期,客户身份证号\
			    from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1\
	            group by 支行名,年度,季度) S2\
                where S1.支行名 = S2.支行名 and S1.年度 = S2.年度 and S1.季度 = S2.季度;"
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()

        currentRowCount = self.ui.TJ_Table.rowCount()
        for i in data:
            self.ui.TJ_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)
            item4 = QTableWidgetItem(str(i[4]))
            item4.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.TJ_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.TJ_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.TJ_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.TJ_Table.setItem(currentRowCount, 3, item3) #列4
            self.ui.TJ_Table.setItem(currentRowCount, 4, item4) #列5

            currentRowCount += 1


    def fun_TJ_CX_Year(self):
        self.ui.TJ_Table.setRowCount(0)
        self.ui.TJ_Table.setColumnCount(4) # 不设置不显示这些列
        self.ui.TJ_Table.setHorizontalHeaderLabels(['支行名', '月份','新增客户人数','新增存储'])
        self.ui.TJ_Table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #设置表格等宽
        self.ui.TJ_Table.horizontalHeader().setStyleSheet("QHeaderView::section{background:gray;}")

        cur = self.db.cursor()
        sql = """#按月统计银行储蓄总额以及客户人数
                select S1.支行名, S1.年度, 新增客户人数, 存储总额
                from
                (select 支行名, DATE_FORMAT(开户日期,'%Y') 年度, SUM(账户余额) 存储总额
	            from ((select distinct 支行名,账户号,账户余额,开户日期
			    from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))
			    Union
			    (select distinct 支行名,账户号,账户余额,开户日期
			    from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1
	            group by 支行名,年度) S1,
                (
	            select 支行名,DATE_FORMAT(开户日期,'%Y') 年度, count(distinct 客户身份证号) 新增客户人数 
	            from ((select 支行名,账户号,账户余额,开户日期,客户身份证号
			    from 支行 left join ((储蓄账户 left join 储蓄账户访问时间 Using(账户号))) Using(支行名))
			    Union
			    (select 支行名,账户号,账户余额,开户日期,客户身份证号
			    from 支行 left join ((支票账户 left join 支票账户访问时间 Using(账户号))) Using(支行名))) C1
	            group by 支行名,年度) S2
                where S1.支行名 = S2.支行名 and S1.年度 = S2.年度;"""
        cur.execute(sql)
        data = cur.fetchall()
        #print(data)
        cur.close()

        currentRowCount = self.ui.TJ_Table.rowCount()
        for i in data:
            self.ui.TJ_Table.insertRow(currentRowCount)

            item0 = QTableWidgetItem(str(i[0]))
            item0.setTextAlignment(QtCore.Qt.AlignCenter)
            item1 = QTableWidgetItem(str(i[1]))
            item1.setTextAlignment(QtCore.Qt.AlignCenter)
            item2 = QTableWidgetItem(str(i[2]))
            item2.setTextAlignment(QtCore.Qt.AlignCenter)
            item3 = QTableWidgetItem(str(i[3]))
            item3.setTextAlignment(QtCore.Qt.AlignCenter)

            self.ui.TJ_Table.setItem(currentRowCount, 0, item0) #列1
            self.ui.TJ_Table.setItem(currentRowCount, 1, item1) #列2
            self.ui.TJ_Table.setItem(currentRowCount, 2, item2) #列3
            self.ui.TJ_Table.setItem(currentRowCount, 3, item3) #列4

            currentRowCount += 1


