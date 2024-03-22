from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QDialog
from PySide2.QtCore import QObject
from seed import Ascend
from cliend import ChilendClass

class Stats(QMainWindow):
    def __init__(self):
        super(Stats, self).__init__()
        self.ui = QUiLoader().load('untitled.ui')
        self.ui.setWindowTitle('管理界面')
        self.ui.pushButton.clicked.connect(self.manuse) #用户按钮
        self.ui.pushButton_2.clicked.connect(self.earning) #收银按钮

        self.OurNewWindow = Ascend()       #登录页面
        self.OurNewWindow.ui.show()
        self.OurNewWindow.param_signal.connect(self.display_params)  # 连接信号和槽函数
        self.account = []  #存储账户
        self.coded = []    #存储账户密码

    def display_params(self, arg1, arg2, arg3): #登录信号
        # print("收到参数:", arg1, arg2, arg3)
        if(arg3 == 1):
            stats.ui.show()
        self.account = arg1
        self.coded = arg2
        
    def manuse(self):
        self.cli = ChilendClass(self.account,self.coded) 
        self.cli.ui.show()

    def earning(self):
        print("ksdmfls")
        
        
if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    stats.ui.hide()  # 隐藏窗口
    app.exec_()