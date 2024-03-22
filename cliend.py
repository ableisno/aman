from PySide2.QtWidgets import QApplication,QWidget,QTableWidgetItem,QMessageBox
from PySide2.QtUiTools import QUiLoader
import pymysql

class ChilendClass(QWidget):

    def __init__(self,arg1,arg2,parent=None):
        super(ChilendClass, self).__init__(parent)
        self.ui = QUiLoader().load('clientside.ui')  # 加载UI文件
        self.ui.setWindowTitle('客户管理界面')
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.ui.pushButton_2.clicked.connect(self.check)    #加载所有信息
        self.ui.pushButton_3.clicked.connect(self.append)   #添加用户信息
        self.ui.pushButton_4.clicked.connect(self.lete)     #删除用户信息
        self.ui.pushButton.clicked.connect(self.search)     #搜索用户信息
        self.account = arg1  #存储账户
        self.coded = arg2    #存储账户密码
        self.table_name = 'client'
        
    def check(self):
        connection = pymysql.connect(
            host='localhost',
            user=self.account,
            password=self.coded,
            database='management'
        )
        #  创建游标对象
        cursor = connection.cursor()
        # 执行查询语句
        query = f"SELECT * FROM {self.table_name}"
        cursor.execute(query)
        # 获取查询结果
        result = cursor.fetchall()
        # 清空表格控件内容
        self.ui.tableWidget.clearContents()
        # 设置表格行数
        self.ui.tableWidget.setRowCount(len(result))
        # 插入数据到表格
        for row_index, row_data in enumerate(result):
            for column_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data)) #将单元格数据转换为字符串并设置为文本内容
                self.ui.tableWidget.setItem(row_index, column_index, item)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 关闭游标和连接
        cursor.close()
        connection.close()

    def lete(self):      #删除用户
        connection = pymysql.connect(
            host='localhost',
            user=self.account,
            password=self.coded,
            database='management'
        )

        cursor = connection.cursor()    #  创建游标对象
        currentrow = self.ui.tableWidget.currentRow()
        gain = self.ui.tableWidget.item(currentrow,0).text()
        gain_1 = self.ui.tableWidget.item(currentrow,1).text()
        sql = "DELETE FROM " + self.table_name + " WHERE ID = %s"

        choice = QMessageBox.question(
        self.ui,
        '确认',
        '确定要删除'+ gain_1 +'吗？')

        if choice == QMessageBox.Yes:
            try:
                cursor.execute(sql, (gain,))
                connection.commit()
                print("删除成功")
            except pymysql.Error as e:
                connection.rollback()
                print("删除失败:", e)
        if choice == QMessageBox.No:
            print('你选择了no')


        cursor.close()
        connection.close()
        self.check()   #更新表格

    def append(self):    #添加用户
        # self.pend = pend() 
        # self.pend.ui.show()
        self.pend = QUiLoader().load('usr.ui')  # 加载添加用户界面
        self.pend.setWindowTitle('添加用户界面')
        self.pend.show()
        self.pend.buttonBox.accepted.connect(self.append_usr)
        
    def append_usr(self):
        connection = pymysql.connect(
            host='localhost',
            user=self.account,
            password=self.coded,
            database='management'
        )
        cursor = connection.cursor()
        sql = "INSERT INTO " + self.table_name + " VALUES (NULL, %s, %s, %s ,0)"
        cursor.execute(sql, (self.pend.lineEdit.text(), self.pend.comboBox.currentText(),self.pend.lineEdit_2.text()))
        
        # 提交事务并关闭连接
        connection.commit()
        connection.close()
        self.check()

    def search(self):  #搜索用户
        connection = pymysql.connect(
            host='localhost',
            user=self.account,
            password=self.coded,
            database='management'
        )
        cursor = connection.cursor()
        phone = self.ui.lineEdit.text()
        sql = "SELECT * FROM " + self.table_name + " WHERE 电话 LIKE %s "
        phone = f"{phone}%"
        try:
            cursor.execute(sql, (phone))
            connection.commit()
            print("搜索成功")
        except pymysql.Error as e:
            connection.rollback()
            print("搜索失败:", e)
        results = cursor.fetchall()
        # 清空表格控件内容
        self.ui.tableWidget.clearContents()
        # 设置表格行数
        self.ui.tableWidget.setRowCount(len(results))
        # 插入数据到表格
        for row_index, row_data in enumerate(results):
            for column_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data)) #将单元格数据转换为字符串并设置为文本内容
                self.ui.tableWidget.setItem(row_index, column_index, item)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True)
        # 关闭游标和连接
        cursor.close()
        connection.close()

    
if __name__ == '__main__':
    
    app = QApplication([])
    stats = ChilendClass()
    stats.ui.show()
    app.exec_()