from PySide2.QtWidgets import QApplication, QMessageBox,QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import Signal

import pymysql


class Ascend(QWidget):
    param_signal = Signal(str, str, int)

    def __init__(self,parent=None):
        super(Ascend, self).__init__(parent)
        self.ui = QUiLoader().load('register.ui')  # 加载UI文件
        self.ui.setWindowTitle('登录界面')
        self.ui.pushButton.clicked.connect(self.enter)      
        self.ui.pushButton_2.clicked.connect(self.enroll)   
        

    def enter(self):
        text = self.ui.lineEdit.text()        # 获取登录账号信息
        text_2 = self.ui.lineEdit_2.text()    # 获取登录密码信息
        try:
            connection = pymysql.connect(
                host='localhost',
                user=text,
                password=text_2,
                database='management'
            )
            cur = connection.cursor()
            cur.close()
            connection.close()

            self.param_signal.emit(text, text_2,1)  # 发射自定义信号，传递参数
            self.ui.close()  # 关闭登录界面
        except pymysql.err.OperationalError as e:
            QMessageBox.critical(
                self.ui,
                '登录',
                '登录失败，请重新输入！')

    def enroll(self):
        print("注册")


if __name__ == '__main__':
    app = QApplication([])
    stats = Ascend()
    stats.ui.show()
    app.exec_()