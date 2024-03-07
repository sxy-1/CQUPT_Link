import sys
import socket
import psutil
import requests
import webbrowser
from PyQt6.QtCore import Qt, QTranslator, QLocale, QObject, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QApplication
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar, MessageBox
from LoginWindow import Ui_Form
from ConnectDb import ConnectDb
import images  # 不要删，导入qrc文件


class Mysignals(QObject):
    text_print = pyqtSignal(str)


class LoginWindow(AcrylicWindow, Ui_Form):
    # my_signals = Mysignals()
    # ms = my_signals.text_print
    db = ConnectDb()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')

        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.label.setScaledContents(False)
        self.setWindowTitle('重邮校园网登录')
        self.setWindowIcon(QIcon(":/resource/images/logo.png"))
        self.resize(1000, 650)

        self.windowEffect.setMicaEffect(self.winId(), isDarkMode=False)
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: white
            }
        """)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
        self.pushButton.clicked.connect(self.login)
        self.PushButton.clicked.connect(self.refresh)
        self.pushButton_2.clicked.connect(lambda: webbrowser.open("https://202.202.32.120:8443/Self/login/"))
        self.isp_mapping = {"0": "cmcc", "1": "unicom", "2": "telecom"}

        exists, account = self.db.get_first_user()
        if exists:
            # self.id = account[0]
            self.user_account = account[1]
            self.user_password = account[2]

            self.isp = self.isp_mapping[account[3]]
            print( self.user_account,self.user_password,self.isp)
            self.method = account[4]
            self.lineEdit_3.setText(self.user_account)
            self.lineEdit_4.setText(self.user_password)
            if self.isp == "cmcc":
                self.RadioButton_1.setChecked(True)
            elif self.isp == "unicom":
                self.RadioButton_2.setChecked(True)
            elif self.isp == "telecom":
                self.RadioButton_3.setChecked(True)

            if self.method == "0":
                self.RadioButton_5.setChecked(True)
            elif self.method == "1":
                self.RadioButton_6.setChecked(True)

    def login(self):

        if self.RadioButton_1.isChecked():
            self.isp = "0"
        elif self.RadioButton_2.isChecked():
            self.isp = "1"
        elif self.RadioButton_3.isChecked():
            self.isp = "2"
        else:
            MessageBox("信息缺少", "未选择运营商", self).exec()
            return
        if self.RadioButton_5.isChecked():
            self.method = "0"
        elif self.RadioButton_6.isChecked():
            self.method = "1"
        else:
            MessageBox("信息缺少", "未选择设备类型", self).exec()
            return
        print("正在login")
        if self.checkBox.isChecked():
            self.db.insert_user(self.lineEdit_3.text(), self.lineEdit_4.text(), self.isp, self.method)
        print(self.lineEdit.text())
        print(self.method)
        print(self.lineEdit_3.text())
        print(self.lineEdit_4.text())
        print(self.LineEdit.text())
        url = "http://" + self.lineEdit.text() + ":801/" + "eportal/?c=Portal&a=login&callback=dr1003&login_method=1&user_account=%2C" + self.method + "%2C" + self.lineEdit_3.text() + "%40" + \
              self.isp_mapping[
                  self.isp] + "&user_password=" + self.lineEdit_4.text() + "&wlan_user_ip=" + self.LineEdit.text() + "&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=3.3.3&v=6305"
        print(url)
        response = requests.get(url)
        print(response)
        print(response.content)
        content = ''
        if response.status_code == 200 and (
                b'dr1003({"result":"0","msg":"","ret_code":2})' in response.content or b'\u8ba4\u8bc1\u6210\u529f' in response.content):
            title = '登录成功'

            if b'dr1003({"result":"0","msg":"","ret_code":2})' in response.content:
                method_mapping = {"0": "电脑端", "1": "移动端"}
                content = "重复登录，如果您想更改/伪装新的登录端，请现在自服务注销"
                # 也可能已达到 + method_mapping[self.method]  + 数量限制
        else:
            print("登录失败")
            title = '登录失败'
            print(response.content)
            print(b'dr1003({"result":"0","msg":"dXNlcmlkIGVycm9yMQ==","ret_code":1})' == response.content)
            print("cao")
            if b'bGRhcCBhdXRoIGVycm9y' in response.content:
                content = "密码错误或运营商错误，请仔细检查后重试"
            elif b'aW51c2UsIGxvZ2luI' in response.content:
                content = "请再试一次"
            elif b'dr1003({"result":"0","msg":"","ret_code":1})' in response.content:
                content = "请仔细检查ip地址等后重试！"
            elif b'dr1003({"result":"0","msg":"dXNlcmlkIGVycm9yMQ==","ret_code":1})' in response.content:
                content = "请仔细检查运营商等后重试"
            elif b'dr1003({"result":"0","msg":"\\u5bc6\\u7801\\u4e0d\\u80fd\\u4e3a\\u7a7a"})' in response.content:
                content = "密码不能为空，请重新填写密码"
            content += f"\n{response.status_code}\n {response.content}\n"
            print(content)
            content += f"{url}"
            print(content)
        w = MessageBox(title, content, self)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def refresh(self):
        ipv4_address = "error"
        try:
            interfaces = psutil.net_if_addrs()
            interface_name = "WLAN"
            # 选择指定名称的接口
            interface = interfaces.get(interface_name)

            # 遍历接口的地址信息
            for address in interface:
                if address.family == socket.AF_INET:
                    ipv4_address = address.address  # 获取IPv4地址
                    ipv4_netmask = address.netmask  # 获取IPv4网络掩码

                    # print(ipv4_address)

        except Exception as e:
            print(f"错误：{e}")
            return None, None
        self.LineEdit.setText(ipv4_address)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/resource/images/gd3u3ibyyp.jpg").scaled(
            # pixmap = QPixmap("./resource/images/middle.jpg").scaled(
            self.label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Internationalization
    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)

    w = LoginWindow()
    w.show()
    app.exec()
