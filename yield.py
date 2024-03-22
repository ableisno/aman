from PySide2.QtWidgets import QApplication, QWidget,QTableView,QHeaderView,QTableWidgetItem
from PySide2.QtGui import QStandardItemModel, QStandardItem
from PySide2.QtUiTools import QUiLoader
import pymysql



class earn(QWidget):
    def __init__(self,parent=None):
        super(earn, self).__init__(parent)
        self.ui = QUiLoader().load('earnings.ui')  # 加载记账界面
        self.ui.setWindowTitle('记账管理界面')
        self.ui.action_3.triggered.connect(self.add_pro) #添加商品
        self.account ='root'
        self.coded = '123456'
        self.table_name= 'product'
        self.ui.pushButton.clicked.connect(self.duct)    #加载按钮
        self.ui.pushButton_2.clicked.connect(self.mess)  #显示商品按钮
        self.ui.pushButton_3.clicked.connect(self.sell)  #出售按钮
        
    def duct(self):
        print(self.ui.calendarWidget.selectedDate())

    def add_pro(self):
        self.add = QUiLoader().load('product.ui')  # 加载商品界面
        self.ui.setWindowTitle('商品界面')
        stats.add.show()
        self.add.buttonBox.accepted.connect(self.pro)  #确认信号
        
    def pro(self):
        print(self.add.lineEdit.text())
        print(self.add.lineEdit_2.text())
        connection = pymysql.connect(
            host='localhost',
            user=self.account,
            password=self.coded,
            database='management'
        )
        # #  创建游标对象
        # cursor = connection.cursor()
        # # 执行查询语句
        # query = f"SELECT * FROM {self.table_name}"
        # cursor.execute(query)
        # # 获取查询结果
        # result = cursor.fetchall()
        
        
    def mess(self):
        connection = pymysql.connect(
            host='localhost',
            user=self.account,
            password=self.coded,
            database='management'
        )
        
        cursor = connection.cursor()                             # 创建游标对象
        cursor.execute("SHOW COLUMNS FROM "+ self.table_name)    # 获取表结构
        columns = cursor.fetchall()                              # 获取查询结果

        header_labels = [column[0] for column in columns]  # 提取列标题
        self.ui.tableWidget.setColumnCount(len(header_labels))  # 设置表格的列数
        self.ui.tableWidget.setHorizontalHeaderLabels(header_labels)  # 设置表格的列标题
        tableHeader = self.ui.tableWidget.horizontalHeader()
        tableHeader.setStretchLastSection(True)  # 设置表格控件的宽度

        cursor.execute("SELECT * FROM "+ self.table_name) # 获取表数据
        data = cursor.fetchall()
        self.ui.tableWidget.setRowCount(len(data))  # 设置表格的行数
        for row, row_data in enumerate(data):
            for column, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                self.ui.tableWidget.setItem(row, column, item)  # 填充表格数据
        # 关闭游标和连接
        cursor.close()
        connection.close()
    def sell(self):
        
        print(self.ui.calendarWidget.selectedDate())

if __name__ == '__main__':
    app = QApplication([])
    stats = earn()
    stats.ui.show()
    app.exec_()