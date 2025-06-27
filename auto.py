import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox
import json
from interface2 import MainWindow
class AuthorizationWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Окно авторизации")
        self.setGeometry(100, 100, 300, 200)

        self.login_label = QLabel("Логин:", self)
        self.login_label.move(50, 50)

        self.login_input = QLineEdit(self)
        #self.login_input.move()
        self.login_input.setGeometry(100, 50, 120, 20)

        self.password_label = QLabel("Пароль:", self)
        self.password_label.move(50, 80)

        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        #self.password_input.move()
        self.password_input.setGeometry(100, 80,120, 20)

        self.login_button = QPushButton("Войти", self)
        self.login_button.move(100, 120)
        self.login_button.clicked.connect(self.save_login_password)

    def save_login_password(self):
        with open('auto.json', 'r') as file:
            data = json.load(file)
        log = data['login']
        pw = data['password']

        login = self.login_input.text()
        password = self.password_input.text()
        print("Логин:", login)
        print("Пароль:", password)
        if log == login and pw == password:
            self.main_window = MainWindow()  # Сохраняем ссылку на объект MainWindow
            self.main_window.show()
            self.close()
        else:
            QMessageBox.about(self, "Ошибка", "Неверный логин или пароль. Повторите попытку")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    auth_window = AuthorizationWindow()
    auth_window.show()
    sys.exit(app.exec_())