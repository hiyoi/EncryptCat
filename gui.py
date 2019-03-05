import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QLineEdit, QPushButton, QMessageBox
from crypto import encrypt_file, decrypt_file


class myLabel(QLabel):

    def __init__(self, parent=None):
        super(myLabel, self).__init__(parent)
        self.setText('将 待加密文件 或 待解密文件 拖进来')

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        self.path = e.mimeData().urls()[0].toLocalFile()
        self.setText(self.path)


class MyWindow(QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.resize(300, 300)
        self.mainlayout = QVBoxLayout(self)
        self.label = myLabel(self)
        self.label.setAcceptDrops(True)
        self.textbox = QLineEdit(self)
        self.textbox.setEchoMode(QLineEdit.Password)
        self.textbox.setPlaceholderText("输入密钥")
        self.enc_btn = QPushButton('加密')
        self.enc_btn.clicked.connect(self.on_enc_cilck)
        self.dec_btn = QPushButton('解密')
        self.dec_btn.clicked.connect(self.on_dec_click)
        self.mainlayout.addWidget(self.label)
        self.mainlayout.addWidget(self.textbox)
        self.mainlayout.addWidget(self.enc_btn)
        self.mainlayout.addWidget(self.dec_btn)
        self.show()

    @pyqtSlot()
    def on_enc_cilck(self):
        output = encrypt_file(self.textbox.text(), self.label.text())
        QMessageBox.information(self,
                                "加密成功",
                                "加密成功! 加密文件路径: " + output,
                                QMessageBox.Close)

    @pyqtSlot()
    def on_dec_click(self):
        try:
            output = decrypt_file(self.textbox.text(), self.label.text())
            QMessageBox.information(self, "解密完毕", "解密完毕! 解密文件路径: " + output,
                                    QMessageBox.Close)
        except ValueError:
            QMessageBox.warning(self, "解密失败", "解密失败! 待解密文件解析出错",
                                QMessageBox.Close)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('加密喵')
    sys.exit(app.exec_())
