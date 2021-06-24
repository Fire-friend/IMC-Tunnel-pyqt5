from demo import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QIcon
import requests
import base64
import re
import time
import configparser
import os

from autorun_util import AutoRun

class Login:

    def __init__(self, usr, pwd):
        self.every = 5
        self.usr = usr
        self.pwd = pwd

    def login(self):
        # print(self.getCurrentTime(), u"connecting...")
        account = self.usr
        pwd = str(base64.b64encode(self.pwd.encode('utf-8')), 'utf-8')
        url = 'http://10.10.10.146:8080/portal/pws?t=li'
        head = {
            'Host': '10.10.10.146:8080',
            'Origin': 'http://10.10.10.146:8080',
            'Pragma': 'no-cache',
            'Referer': 'http://10.10.10.146:8080/portal/index_default.jsp',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': 'hello1={}; hello2=false; i_p_pl=JTdCJTIyZXJyb3JOdW1iZXIlMjIlM0ElMjIxJTIyJTJDJTIybmV4dFVybCUyMiUzQSUyMmh0dHAlM0ElMkYlMkYxMC4xMC4xMC4xNDYlM0E4MDgwJTJGcG9ydGFsJTJGaW5kZXhfZGVmYXVsdC5qc3AlMjIlMkMlMjJxdWlja0F1dGglMjIlM0FmYWxzZSUyQyUyMmNsaWVudExhbmd1YWdlJTIyJTNBJTIyQ2hpbmVzZSUyMiUyQyUyMmFzc2lnbklwVHlwZSUyMiUzQTAlMkMlMjJpTm9kZVB3ZE5lZWRFbmNyeXB0JTIyJTNBMSUyQyUyMndsYW5uYXNpZCUyMiUzQSUyMiUyMiUyQyUyMndsYW5zc2lkJTIyJTNBJTIyJTIyJTJDJTIybmFzSXAlMjIlM0ElMjIlMjIlMkMlMjJieW9kU2VydmVySXAlMjIlM0ElMjIxMC4xMC4xMC4xNDYlMjIlMkMlMjJieW9kU2VydmVySXB2NiUyMiUzQSUyMjAwMDAlM0EwMDAwJTNBMDAwMCUzQTAwMDAlM0EwMDAwJTNBMDAwMCUzQTAwMDAlM0EwMDAwJTIyJTJDJTIyYnlvZFNlcnZlckh0dHBQb3J0JTIyJTNBJTIyODA4MCUyMiUyQyUyMmlmVHJ5VXNlUG9wdXBXaW5kb3clMjIlM0FmYWxzZSUyQyUyMnVhbUluaXRDdXN0b20lMjIlM0ElMjIxJTIyJTJDJTIyY3VzdG9tQ2ZnJTIyJTNBJTIyTFRFJTIyJTJDJTIycmVnQ29kZVR5cGUlMjIlM0ElMjJNQSUyMiU3RA'.format(
                account),
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '414',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        data = {
            'userName': '{}'.format(account),
            'userPwd': '{}'.format(pwd),
            'userDynamicPwd': '',
            'userDynamicPwdd': '',
            'serviceType': '',
            'userurl': '',
            'userip': '',
            'basip': '',
            'language': 'Chinese',
            'usermac': 'null',
            'wlannasid': '',
            'wlanssid': '',
            'entrance': 'null',
            'loginVerifyCode': '',
            'userDynamicPwddd': '',
            'customPageId': '0',
            'pwdMode': '0',
            'portalProxyIP': '10.10.10.146',
            'portalProxyPort': '50200',
            'dcPwdNeedEncrypt': '1',
            'assignIpType': '0',
            'appRootUrl': 'http://10.10.10.146:8080/portal/',
            'manualUrl': '',
            'manualUrlEncryptKey': ''
        }

        try:
            requests.post(url, params=data, headers=head)
            print(self.getCurrentTime(), 'connection over')
        except:
            print("connection over")

    def canConnect(self):
        try:
            q = requests.get("http://www.baidu.com", timeout=10)
            m = re.search(r'STATUS OK', q.text)
            if m:
                return True
            else:
                return False
        except:
            # print('error')

            return False

    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def main(self):
        can_connect = self.canConnect()
        if not can_connect:
            # print(self.getCurrentTime(), " internet interruption")
            ui.btn_online.setText('正在连接')
            self.login()
        else:
            # print(self.getCurrentTime(), " internet normal")
            ui.btn_online.setText('已上线')
            # self.login()
            # while True:
            #     can_connect = self.canConnect()
            #     if not can_connect:
            #         print(self.getCurrentTime(), " internet interruption")
            #         self.login()
            #     else:
            #         print(self.getCurrentTime(), " internet normal")
            #     time.sleep(self.every)
            # time.sleep(self.every)


class MyThread(QThread):
    _signal = pyqtSignal(str)  # 信号类型：int

    def __init__(self, sec=500, parent=None):
        super().__init__(parent)
        self.sec = sec  # 默认1000秒

    def run(self):
        while True:
            self._signal.emit('detect')  # 发射信号
            usr = ui.txt_username.text()
            pwd = ui.txt_passward.text()
            do_login.usr = usr
            do_login.pwd = pwd
            do_login.main()
            self.msleep(self.sec)

class TimeThread(QThread):
    _signal = pyqtSignal(str)  # 信号类型：int

    def __init__(self, sec=3600, parent=None):
        super().__init__(parent)
        self.sec = sec  # 默认1000秒
        self.houre = 0

    def run(self):
        while True:
            ui.LCD_time.display(self.houre)
            self.houre += 1
            self.sleep(self.sec)

def login():
    # print("ss")
    ui.btn_online.setEnabled(False)


    my_thread.start()
    do_Time.start()


class CamShow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(CamShow, self).__init__(parent)
        self.setupUi(self)


def write_config():
    """
    共享变量写入配置文件
    """
    global usr
    global pwd
    global is_start

    usr = ui.txt_username.text()
    pwd = ui.txt_passward.text()
    if ui.CB_start.isChecked():
        is_start = 1
    else:
        is_start = 0

    cf.set('login', 'usr', usr)
    cf.set('login', 'pwd', pwd)
    cf.set('login', 'start_up', str(is_start))
    cf.write(open(os.path.join(root_path, 'config.ini'), "w"))


def read_config():
    """
    配置文件读入内存
    """
    global usr
    global pwd
    global is_start

    cf.read(os.path.join(root_path, "config.ini"))
    usr = cf.get('login', 'usr')
    pwd = cf.get('login', 'pwd')
    is_start = int(cf.get('login', 'start_up'))

    ui.txt_username.setText(usr)
    ui.txt_passward.setText(pwd)
    if is_start == 1:
        ui.CB_start.setChecked(True)
        AutoRun(switch='open', key_name='net_connect')
    else:
        ui.CB_start.setChecked(False)
        AutoRun(switch='close', key_name='net_connect')

    return cf

def change_start():
    if ui.CB_start.isChecked():
        AutoRun(switch='open', key_name='net_connect')
    else:
        AutoRun(switch='close', key_name='net_connect')
    write_config()

def change_usr():
    global usr
    usr = ui.txt_username.text()
    write_config()

def change_pwd():
    global pwd
    pwd = ui.txt_passward.text()
    write_config()

cf = configparser.ConfigParser()
root_path, _ = os.path.split(os.path.abspath(sys.argv[0]))
usr = "0"
pwd = "0"
is_start = 0
do_login = Login(pwd=pwd, usr=usr)

from PyQt5.QtNetwork import QLocalSocket, QLocalServer

if __name__ == '__main__':
    app = QApplication(sys.argv)
    serverName = 'CarServer'
    socket = QLocalSocket()
    socket.connectToServer(serverName)
    if socket.waitForConnected(500):
        QMessageBox().information(None, "提示", "软件已在托盘运行，右键托盘恢复。", QMessageBox.Yes)
        app.quit()
    else:

        ui = CamShow()
        my_thread = MyThread()
        do_Time = TimeThread()
        # my_thread._signal.connect(do)
        read_config()
        ui.btn_online.clicked.connect(login)
        ui.CB_start.clicked.connect(change_start)
        ui.txt_username.textChanged.connect(change_usr)
        ui.txt_passward.textChanged.connect(change_pwd)
        ui.setWindowTitle('IMC Tunnel v1.0beta')
        ui.setWindowIcon(QIcon(os.path.join(root_path, 'icon.ico')))
        app.setQuitOnLastWindowClosed(False)

        def showApp():
            ui.show()  # w.hide() #隐藏
        tp = QSystemTrayIcon(ui)
        tp.setIcon(QIcon(os.path.join(root_path, 'icon.ico')))
        a1 = QAction('&显示(Show)', triggered=showApp)


        def quitApp():
            tp.setVisible(False)
            # os.kill(car_zhou_video_process_thread.pid, 19)
            os._exit(0)


        a2 = QAction('&退出(Exit)', triggered=quitApp)  # 直接退出可以用qApp.quit
        tpMenu = QMenu()
        tpMenu.addAction(a1)
        tpMenu.addAction(a2)
        tp.setContextMenu(tpMenu)
        tp.show()

        ui.show()
        sys.exit(app.exec_())
