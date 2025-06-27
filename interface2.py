import json
import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QDateEdit, QPushButton, QMenu, QToolBar, QMenuBar, \
    QAction, QWidget, QTabWidget, QSpacerItem, QSizePolicy, QHBoxLayout, QVBoxLayout, QGroupBox, QRadioButton, \
    QCheckBox, QMdiArea, QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QLineEdit
from  generateDate import  calculate
import datetime
import newWindow as t
import pandas as pd
from PIL import Image

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.calculate = calculate()
        self._createMenuBar()
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.setWindowTitle('Оперативный анализ')

        # UI components (example, these should be properly initialized in your UI setup)
        self.radioButton = QRadioButton()
        self.radioButton_2 = QRadioButton()
        self.radioButton_3 = QRadioButton()
        self.radioButton_4 = QRadioButton()
        self.radioButton_5 = QRadioButton()
        self.radioButton_6 = QRadioButton()
        self.radioButton_7 = QRadioButton()
        self.radioButton_8 = QRadioButton()
        self.radioButton_9 = QRadioButton()
        self.radioButton_10 = QRadioButton()
        self.radioButton_13 = QRadioButton()
        self.radioButton_14 = QRadioButton()
        self.radioButton_15 = QRadioButton()
        self.checkBox_3 = QCheckBox()
        self.checkBox_6 = QCheckBox()
        self.date_edit1 = QDateEdit()
        self.date_edit2 = QDateEdit()

    def _createMenuBar(self):
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1095, 24))

        self.analysis_menu = QAction('Анализ', self)
        self.analysis_menu.triggered.connect(self.run_centralWidget)
        self.menuBar.addAction(self.analysis_menu)

        self.save_menu = QAction('Сохранённые решения', self)
        self.save_menu.triggered.connect(self.run_centralWidget)
        self.menuBar.addAction(self.save_menu)

        self.settings_menu = QAction('Настройки', self)
        self.settings_menu.triggered.connect(self.run_centralWidget)
        self.menuBar.addAction(self.settings_menu)

        self.setMenuBar(self.menuBar)

    def run_centralWidget(self):
        action = self.sender()
        if action.text() == 'Анализ':
            self.show_analysis()
        elif action.text() == 'Сохранённые решения':
            self.open_saved_solutions()
        elif action.text() == 'Настройки':
            self.show_settings()

    def show_analysis(self):
        self.centralWidget = QWidget(self)
        vbox = QVBoxLayout()

        layout = QHBoxLayout()
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        label1 = QLabel("Начало периода:")
        self.date_edit1 = QDateEdit()
        label2 = QLabel("Конец периода:")
        self.date_edit2 = QDateEdit()
        self.date_edit2.setDate(QDate.currentDate())
        layout.addItem(spacerItem)
        layout.addWidget(label1)
        layout.addWidget(self.date_edit1)
        layout.addWidget(label2)
        layout.addWidget(self.date_edit2)
        vbox.addLayout(layout)

        self.tabWidget = QTabWidget()
        self.tabWidget.setGeometry(QtCore.QRect(0, 60, 1101, 751))
        # ABC
        self.tab = QWidget()
        self.groupBox = QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 560, 140))
        self.radioButton = QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(10, 30, 371, 20))
        self.radioButton.setChecked(True)
        self.radioButton.setText("анализ по наименованию одежды ")
        self.radioButton_2 = QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 50, 361, 20))
        self.radioButton_2.setText("анализ по категории одежды ")
        self.radioButton_3 = QRadioButton(self.groupBox)
        self.radioButton_3.setGeometry(QtCore.QRect(10, 70, 321, 20))
        self.radioButton_3.setText("анализ по размеру одежды")
        self.radioButton_4 = QRadioButton(self.groupBox)
        self.radioButton_4.setGeometry(QtCore.QRect(10, 90, 321, 20))
        self.radioButton_4.setText("анализ по гендерной принадлежности обежды ")
        self.checkBox_2 = QCheckBox(self.tab)
        self.checkBox_2.setGeometry(QtCore.QRect(20, 170, 431, 20))
        self.checkBox_2.setText("Учитывать границы установленного периода")
        self.pushButton_2 = QPushButton(self.tab)
        self.pushButton_2.clicked.connect(self.ABC)
        self.pushButton_2.setGeometry(20, 200, 93, 30)
        self.pushButton_2.setText("Рассчитать")
        self.tabWidget.addTab(self.tab, "ABC")

        # XYZ
        self.tab_2 = QWidget()
        self.groupBox_2 = QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 20, 511, 80))
        self.radioButton_5 = QRadioButton(self.groupBox_2)
        self.radioButton_5.setGeometry(QtCore.QRect(10, 30, 131, 20))
        self.radioButton_5.setChecked(True)
        self.radioButton_5.setText("по сезонам")
        self.radioButton_6 = QRadioButton(self.groupBox_2)
        self.radioButton_6.setGeometry(QtCore.QRect(10, 50, 111, 20))
        self.radioButton_6.setText("по месяцам")
        self.groupBox_3 = QGroupBox(self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 110, 561, 81))
        self.radioButton_7 = QRadioButton(self.groupBox_3)
        self.radioButton_7.setGeometry(QtCore.QRect(10, 30, 371, 20))
        self.radioButton_7.setChecked(True)
        self.radioButton_7.setText("анализ по наименованию одежды ")
        self.radioButton_7.setObjectName("radioButton_7")
        self.radioButton_8 = QRadioButton(self.groupBox_3)
        self.radioButton_8.setGeometry(QtCore.QRect(10, 50, 361, 20))
        self.radioButton_8.setText("анализ по категории одежды")
        self.pushButton_4 = QPushButton(self.tab_2)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 230, 93, 30))
        self.pushButton_4.setText("Рассчитать")
        self.pushButton_4.clicked.connect(self.XYZ)
        self.tabWidget.addTab(self.tab_2, "XYZ")

        # общий
        self.tab_3 = QWidget()
        self.groupBox_5 = QGroupBox(self.tab_3)
        self.groupBox_5.setGeometry(QtCore.QRect(20, 20, 511, 100))
        self.radioButton_13 = QRadioButton(self.groupBox_5)
        self.radioButton_13.setGeometry(QtCore.QRect(10, 30, 111, 20))
        self.radioButton_13.setChecked(True)
        self.radioButton_13.setText("по сезонам")
        self.radioButton_14 = QRadioButton(self.groupBox_5)
        self.radioButton_14.setGeometry(QtCore.QRect(10, 50, 111, 20))
        self.radioButton_14.setText("по месяцам")
        self.radioButton_15 = QRadioButton(self.groupBox_5)
        self.radioButton_15.setGeometry(QtCore.QRect(10, 70, 111, 20))
        self.radioButton_15.setText("без сезона")

        self.groupBox4 = QGroupBox(self.tab_3)
        self.groupBox4.setGeometry(QtCore.QRect(20, 125, 561, 120))
        self.radioButton_9 = QRadioButton(self.groupBox4)
        self.radioButton_9.setGeometry(QtCore.QRect(10, 30, 371, 20))
        self.radioButton_9.setChecked(True)
        self.radioButton_9.setText("анализ по наименованию одежды ")
        self.radioButton_10 = QRadioButton(self.groupBox4)
        self.radioButton_10.setGeometry(QtCore.QRect(10, 50, 371, 20))
        self.radioButton_10.setText("анализ по категории одежды ")
        self.checkBox_6 = QCheckBox(self.tab_3)
        self.checkBox_6.setGeometry(QtCore.QRect(20, 250, 293, 30))
        self.checkBox_6.setText("Учитывать границы установленного периода")
        self.pushButton_6 = QPushButton(self.tab_3)
        self.pushButton_6.setGeometry(QtCore.QRect(20, 280, 93, 30))
        self.pushButton_6.clicked.connect(self.General)
        self.pushButton_6.setText("Рассчитать")
        self.tabWidget.addTab(self.tab_3, "Общий анализ")

        self.tab_4 = QWidget()
        self.pushButton_7 = QPushButton(self.tab_4)
        self.pushButton_7.setGeometry(QtCore.QRect(20, 280, 193, 30))
        self.pushButton_7.clicked.connect(self.Prognoz)
        self.pushButton_7.setText("Запустить прогноз продаж")
        self.tabWidget.addTab(self.tab_4, "Прогноз продаж")

        vbox.addWidget(self.tabWidget)

        self.centralWidget.setLayout(vbox)
        self.setCentralWidget(self.centralWidget)

    def open_saved_solutions(self):
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder_path = 'output'
        if not os.path.exists(folder_path):
            QMessageBox.warning(self, 'Ошибка', f'Папка {folder_path} не найдена!')



        folder_path2 = QFileDialog.getExistingDirectory(self, "Выберите папку", folder_path, QFileDialog.ShowDirsOnly)

        ex = t.NewWindow(folder_path2, False)
        ex.show()

    def show_settings(self):
        self.centralWidget = QWidget(self)
        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox1.setAlignment(Qt.AlignmentFlag.AlignRight)
        space = QSpacerItem(880,20)
        hbox1.addItem(space)

        self.login_label = QLabel("Логин:", self)
        hbox1.addWidget(self.login_label)
        self.login_input = QLineEdit(self)
        self.login_input.setFixedWidth(300)
        hbox1.addWidget(self.login_input)
        vbox.addLayout(hbox1)

        hbox2 = QHBoxLayout()
        hbox2.addItem(space)
        hbox2.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.password_label = QLabel("Пароль:", self)
        hbox2.addWidget(self.password_label)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedWidth(300)
        hbox2.addWidget(self.password_input)
        vbox.addLayout(hbox2)

        hbox3 = QHBoxLayout()
        hbox3.addItem(space)
        hbox3.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.password_label2 = QLabel("Пароль:", self)
        hbox3.addWidget(self.password_label2)
        self.password_input2 = QLineEdit(self)
        self.password_input2.setEchoMode(QLineEdit.Password)
        self.password_input2.setFixedWidth(300)
        hbox3.addWidget(self.password_input2)
        vbox.addLayout(hbox3)


        self.login_button = QPushButton("Изменить", self)
        self.login_button.setFixedWidth(100)
        self.login_button.clicked.connect(self.save_login_password)
        vbox.addWidget(self.login_button)

        self.centralWidget.setLayout(vbox)
        self.setCentralWidget(self.centralWidget)

    def save_login_password(self):
        login = self.login_input.text()
        password1 = self.password_input.text()
        password2 = self.password_input2.text()
        if password1!=password2:
            QMessageBox.about(self, "Ошибка", "Пароль и повтор пароля не соответствуют")
        else:
            with open('auto.json', 'r') as file:
                data = json.load(file)
            data['login'] = login
            data['password'] = password1
            with open('auto.json', 'w') as file:
                json.dump(data, file, indent=4)
            QMessageBox.about(self, "Сообщение", "Данные успешно обновлены")

    def open_file(self, file_path):
        # Проверяем расширение файла
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == '.xlsx':
            self.open_excel_file(file_path)
        elif file_extension == '.png':
            self.open_image_file(file_path)
        else:
            QMessageBox.warning(self, 'Неподдерживаемый формат', 'Выбранный файл имеет неподдерживаемый формат.')

    def open_excel_file(self, file_path):
        try:
            # Чтение данных из файла Excel
            df = pd.read_excel(file_path)
            # Создание QTableWidget и заполнение его данными из DataFrame
            table_widget = QTableWidget()
            table_widget.setRowCount(df.shape[0])
            table_widget.setColumnCount(df.shape[1])
            table_widget.setHorizontalHeaderLabels(df.columns)
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    table_widget.setItem(i, j, QTableWidgetItem(str(df.iat[i, j])))

            # Установка созданного виджета в качестве центрального виджета
            self.setCentralWidget(table_widget)
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось открыть файл Excel: {str(e)}')

    def open_image_file(self, file_path):
        try:
            image = Image.open(file_path)
            # Отображение изображения в окне PyQt
            label = QLabel(self)
            label.setPixmap(QtGui.QPixmap(file_path))
            self.setCentralWidget(label)
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось открыть изображение: {str(e)}')

    def process_dates(self, check_box, date_edit1, date_edit2):
        if check_box.isChecked():
            self.calculate.bool_date = True
            start_date = date_edit1.date()
            self.calculate.start_date = datetime(start_date.year(), start_date.month(), start_date.day())
            end_date = date_edit2.date()
            self.calculate.end_date = datetime(end_date.year(), end_date.month(), end_date.day())
        else:
            self.calculate.bool_date = False


    def process_category(self, *radio_buttons):
        for i, radio_button in enumerate(radio_buttons):
            if radio_button.isChecked():
                self.calculate.category = i
                return
        self.calculate.category = None


    def process_period(self, *radio_buttons):
        for i, radio_button in enumerate(radio_buttons):
            if radio_button.isChecked():
                self.calculate.period = i
                return
        self.calculate.period = None
    def ABC(self):
        if self.checkBox_2.isChecked():
            self.calculate.bool_date = True
            strt_date = self.date_edit1.date()
            date_time = datetime.datetime(strt_date.year(), strt_date.month(), strt_date.day())
            self.calculate.start_date = date_time

            end_date = self.date_edit2.date()
            date_time = datetime.datetime(end_date.year(), end_date.month(), end_date.day())
            self.calculate.end_date = date_time
        else:
            self.calculate.bool_date = False
        if self.radioButton.isChecked():
            self.calculate.category = None
        elif self.radioButton_2.isChecked():
            self.calculate.category = 1
        elif self.radioButton_3.isChecked():
            self.calculate.category = 2
        elif self.radioButton_4.isChecked():
            self.calculate.category = 3
        filename = self.calculate.ABC()
        ex = t.NewWindow(filename)
        ex.show()


    def XYZ(self):
        if self.checkBox_3.isChecked():
            self.calculate.bool_date = True
            strt_date = self.date_edit1.date()
            date_time = datetime.datetime(strt_date.year(), strt_date.month(), strt_date.day())
            self.calculate.start_date = date_time

            end_date = self.date_edit2.date()
            date_time = datetime.datetime(end_date.year(), end_date.month(), end_date.day())
            self.calculate.end_date = date_time
        else:
            self.calculate.bool_date = False
        if self.radioButton_5.isChecked():
            self.calculate.period = 2
        elif self.radioButton_6.isChecked():
            self.calculate.period = 1
        if self.radioButton_7.isChecked():
            self.calculate.category = None
        elif self.radioButton_8.isChecked():
            self.calculate.category = 1
        filename = self.calculate.XYZ()
        ex = t.NewWindow(filename)
        ex.show()

    def Prognoz(self):
        filename = self.calculate.Prognoz()
        ex = t.NewWindow(filename)
        ex.show()
    def General(self):
        if self.checkBox_6.isChecked():
            self.calculate.bool_date = True
            strt_date = self.date_edit1.date()
            date_time = datetime.datetime(strt_date.year(), strt_date.month(), strt_date.day())
            self.calculate.start_date = date_time

            end_date = self.date_edit2.date()
            date_time = datetime.datetime(end_date.year(), end_date.month(), end_date.day())
            self.calculate.end_date = date_time
        else:
            self.calculate.bool_date = False
        if self.radioButton_9.isChecked():
            self.calculate.category = None
        elif self.radioButton_10.isChecked():
            self.calculate.category = 1
        if self.radioButton_13.isChecked():
            self.calculate.period = 2
        elif self.radioButton_14.isChecked():
            self.calculate.period = 1
        elif self.radioButton_15.isChecked():
            self.calculate.period = None
        self.calculate.viruchka()
        self.calculate.viruchka_kat()
        ex = t.NewWindow('general')
        ex.show()


