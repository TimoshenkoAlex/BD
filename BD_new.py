from sys import stderr
from PyQt5 import QtCore, QtGui, QtWidgets
import psycopg2
from psycopg2 import Error

try:
    # Подключение к существующей базе данных
    conn = psycopg2.connect(dbname = 'db_214',
                        user = 'postgres',
                        password = '12345',
                        host = 'localhost')
    cursor = conn.cursor()
    
    class Window_fam(QtWidgets.QWidget):
        def __init__(self):
            super(Window_fam, self).__init__()
            self.setWindowTitle('Фамилия')
            self.resize(400, 400)
            
             # Таблица выводв
            self.tableWidget = QtWidgets.QTableWidget(self)
            self.tableWidget.setGeometry(QtCore.QRect(10, 150, 581, 211))
            self.tableWidget.setObjectName("tableWidget")
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Фамилия"])
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            
            # Ввод новой фамилии
            self.fam_text = QtWidgets.QLineEdit(self)
            self.fam_text.setGeometry(QtCore.QRect(10, 10, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.fam_text.setFont(font)
            self.fam_text.setObjectName("fam_text")
            self.fam_text.setPlaceholderText("Введите фамилию")
            
            self.btn = QtWidgets.QPushButton(self)
            self.btn.setGeometry(QtCore.QRect(250, 10, 30, 30))
            font = QtGui.QFont()
            self.btn.setObjectName("btn")
            self.btn.clicked.connect(self.print_table)
            
             # Кнопка удаления
            self.remove_btn = QtWidgets.QPushButton(self)
            self.remove_btn.setGeometry(QtCore.QRect(10, 50, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.remove_btn.setFont(font)
            self.remove_btn.setObjectName("remove_btn")
            self.remove_btn.setText("Удалить")
            self.remove_btn.clicked.connect(self.def_remove)
            
            # Кнопка обновить
            self.update_btn = QtWidgets.QPushButton(self)
            self.update_btn.setGeometry(QtCore.QRect(170, 50, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.update_btn.setFont(font)
            self.update_btn.setObjectName("update_btn")
            self.update_btn.setText("Изменить")
            self.update_btn.clicked.connect(self.def_update)
            
            # Кнопка добавить
            self.add_btn = QtWidgets.QPushButton(self)
            self.add_btn.setGeometry(QtCore.QRect(10, 90, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.add_btn.setFont(font)
            self.add_btn.setObjectName("add_btn")
            self.add_btn.setText("Добавить")
            self.add_btn.clicked.connect(self.def_add)
            
            # Кнопка искать
            self.search_btn = QtWidgets.QPushButton(self)
            self.search_btn.setGeometry(QtCore.QRect(170, 90, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.search_btn.setFont(font)
            self.search_btn.setObjectName("search_btn")
            self.search_btn.setText("Искать")
            self.search_btn.clicked.connect(self.def_search)
            
        # функция вывода
        def print_table(self):
            cursor.execute("select * from fam")
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
                    
        def def_add(self):
            f = self.fam_text.text()
            
            if f != '':
                cursor.execute("INSERT INTO fam(f_id, f_val) values (default, '" + f + "')")
                conn.commit()
                self.print_table()
                
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите фамилию, чтобы ее добавить")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
                    
        def def_search(self):
            request = "select * from fam where "
            f = self.fam_text.text()
            if f != '':
                request = request + "f_val = '" + f + "'"
            if request.endswith('where '):
                request = request[:len(request)-6]
            
            cursor.execute(request)
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
            
        def def_remove(self):
            cur = self.tableWidget.currentRow()
            n = self.tableWidget.item(cur,0).text()
            s = "Вы уверены, что хотите удалить " + str(cur + 1) + " строку?"
            otvet = QtWidgets.QMessageBox.question(self, 'Внимание!', s, QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
            if otvet == QtWidgets.QMessageBox.StandardButton.Yes:
                request = "delete from fam where f_id = "+str(n)
                cursor.execute(request)
                self.print_table()
                
        def def_update(self):
            cur = self.tableWidget.currentRow()
            id = self.tableWidget.item(cur,0).text()
            request = "update fam set "
            
            f = self.fam_text.text()
            if f != '':
                request = request + "f_val = '" + f + "'"
            if request.endswith('set '):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите новую фамилию")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
            else:
                request = request + " where f_id = "+str(id)
                cursor.execute(request)
                conn.commit()
                self.print_table()
                
        
            
    class Window_nam(QtWidgets.QWidget):
        def __init__(self):
            super(Window_nam, self).__init__()
            self.setWindowTitle('Имя')
            self.resize(400, 400)
            
             # Таблица выводв
            self.tableWidget = QtWidgets.QTableWidget(self)
            self.tableWidget.setGeometry(QtCore.QRect(10, 150, 581, 211))
            self.tableWidget.setObjectName("tableWidget")
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Имя"])
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            
            # Ввод новой фамилии
            self.fam_text = QtWidgets.QLineEdit(self)
            self.fam_text.setGeometry(QtCore.QRect(10, 10, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.fam_text.setFont(font)
            self.fam_text.setObjectName("fam_text")
            self.fam_text.setPlaceholderText("Введите имя")
            
            self.btn = QtWidgets.QPushButton(self)
            self.btn.setGeometry(QtCore.QRect(250, 10, 30, 30))
            font = QtGui.QFont()
            self.btn.setObjectName("btn")
            self.btn.clicked.connect(self.print_table)
            
             # Кнопка удаления
            self.remove_btn = QtWidgets.QPushButton(self)
            self.remove_btn.setGeometry(QtCore.QRect(10, 50, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.remove_btn.setFont(font)
            self.remove_btn.setObjectName("remove_btn")
            self.remove_btn.setText("Удалить")
            self.remove_btn.clicked.connect(self.def_remove)
            
            # Кнопка обновить
            self.update_btn = QtWidgets.QPushButton(self)
            self.update_btn.setGeometry(QtCore.QRect(170, 50, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.update_btn.setFont(font)
            self.update_btn.setObjectName("update_btn")
            self.update_btn.setText("Изменить")
            self.update_btn.clicked.connect(self.def_update)
            
            # Кнопка добавить
            self.add_btn = QtWidgets.QPushButton(self)
            self.add_btn.setGeometry(QtCore.QRect(10, 90, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.add_btn.setFont(font)
            self.add_btn.setObjectName("add_btn")
            self.add_btn.setText("Добавить")
            self.add_btn.clicked.connect(self.def_add)
            
            # Кнопка искать
            self.search_btn = QtWidgets.QPushButton(self)
            self.search_btn.setGeometry(QtCore.QRect(170, 90, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.search_btn.setFont(font)
            self.search_btn.setObjectName("search_btn")
            self.search_btn.setText("Искать")
            self.search_btn.clicked.connect(self.def_search)
            
        # функция вывода
        def print_table(self):
            cursor.execute("select * from nam")
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
                    
        def def_add(self):
            f = self.fam_text.text()
            
            if f != '':
                cursor.execute("INSERT INTO nam(n_id, n_val) values (default, '" + f + "')")
                conn.commit()
                self.print_table()
                
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите фамилию, чтобы ее добавить")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
                    
        def def_search(self):
            request = "select * from nam where "
            f = self.fam_text.text()
            if f != '':
                request = request + "n_val = '" + f + "'"
            if request.endswith('where '):
                request = request[:len(request)-6]
            
            cursor.execute(request)
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
            
        def def_remove(self):
            cur = self.tableWidget.currentRow()
            n = self.tableWidget.item(cur,0).text()
            s = "Вы уверены, что хотите удалить " + str(cur + 1) + " строку?"
            otvet = QtWidgets.QMessageBox.question(self, 'Внимание!', s, QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
            if otvet == QtWidgets.QMessageBox.StandardButton.Yes:
                request = "delete from nam where n_id = "+str(n)
                cursor.execute(request)
                self.print_table()
                
        def def_update(self):
            cur = self.tableWidget.currentRow()
            id = self.tableWidget.item(cur,0).text()
            request = "update nam set "
            
            f = self.fam_text.text()
            if f != '':
                request = request + "n_val = '" + f + "'"
            if request.endswith('set '):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите новое имя")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
            else:
                request = request + " where n_id = "+str(id)
                cursor.execute(request)
                conn.commit()
                self.print_table()
    
    class Window_otc(QtWidgets.QWidget):
        def __init__(self):
            super(Window_otc, self).__init__()
            self.setWindowTitle('Отчество')
            self.resize(400, 400)
            
             # Таблица выводв
            self.tableWidget = QtWidgets.QTableWidget(self)
            self.tableWidget.setGeometry(QtCore.QRect(10, 150, 581, 211))
            self.tableWidget.setObjectName("tableWidget")
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Отчество"])
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            
            # Ввод новой фамилии
            self.fam_text = QtWidgets.QLineEdit(self)
            self.fam_text.setGeometry(QtCore.QRect(10, 10, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.fam_text.setFont(font)
            self.fam_text.setObjectName("otc_text")
            self.fam_text.setPlaceholderText("Введите отчество")
            
            self.btn = QtWidgets.QPushButton(self)
            self.btn.setGeometry(QtCore.QRect(250, 10, 30, 30))
            font = QtGui.QFont()
            self.btn.setObjectName("btn")
            self.btn.clicked.connect(self.print_table)
            
             # Кнопка удаления
            self.remove_btn = QtWidgets.QPushButton(self)
            self.remove_btn.setGeometry(QtCore.QRect(10, 50, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.remove_btn.setFont(font)
            self.remove_btn.setObjectName("remove_btn")
            self.remove_btn.setText("Удалить")
            self.remove_btn.clicked.connect(self.def_remove)
            
            # Кнопка обновить
            self.update_btn = QtWidgets.QPushButton(self)
            self.update_btn.setGeometry(QtCore.QRect(170, 50, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.update_btn.setFont(font)
            self.update_btn.setObjectName("update_btn")
            self.update_btn.setText("Изменить")
            self.update_btn.clicked.connect(self.def_update)
            
            # Кнопка добавить
            self.add_btn = QtWidgets.QPushButton(self)
            self.add_btn.setGeometry(QtCore.QRect(10, 90, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.add_btn.setFont(font)
            self.add_btn.setObjectName("add_btn")
            self.add_btn.setText("Добавить")
            self.add_btn.clicked.connect(self.def_add)
            
            # Кнопка искать
            self.search_btn = QtWidgets.QPushButton(self)
            self.search_btn.setGeometry(QtCore.QRect(170, 90, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.search_btn.setFont(font)
            self.search_btn.setObjectName("search_btn")
            self.search_btn.setText("Искать")
            self.search_btn.clicked.connect(self.def_search)
            
        # функция вывода
        def print_table(self):
            cursor.execute("select * from otc")
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
                    
        def def_add(self):
            f = self.fam_text.text()
            
            if f != '':
                cursor.execute("INSERT INTO otc(otc_id, otc_val) values (default, '" + f + "')")
                conn.commit()
                self.print_table()
                
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите отчество, чтобы его добавить")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
                    
        def def_search(self):
            request = "select * from otc where "
            f = self.fam_text.text()
            if f != '':
                request = request + "otc_val = '" + f + "'"
            if request.endswith('where '):
                request = request[:len(request)-6]
            
            cursor.execute(request)
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
            
        def def_remove(self):
            cur = self.tableWidget.currentRow()
            n = self.tableWidget.item(cur,0).text()
            s = "Вы уверены, что хотите удалить " + str(cur + 1) + " строку?"
            otvet = QtWidgets.QMessageBox.question(self, 'Внимание!', s, QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
            if otvet == QtWidgets.QMessageBox.StandardButton.Yes:
                request = "delete from otc where otc_id = "+str(n)
                cursor.execute(request)
                self.print_table()
                
        def def_update(self):
            cur = self.tableWidget.currentRow()
            id = self.tableWidget.item(cur,0).text()
            request = "update otc set "
            
            f = self.fam_text.text()
            if f != '':
                request = request + "otc_val = '" + f + "'"
            if request.endswith('set '):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите новое имя")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
            else:
                request = request + " where otc_id = "+str(id)
                cursor.execute(request)
                conn.commit()
                self.print_table()
            
    class Window_str(QtWidgets.QWidget):
        def __init__(self):
            super(Window_str, self).__init__()
            self.setWindowTitle('Улица')
            self.resize(400, 400)
            
             # Таблица выводв
            self.tableWidget = QtWidgets.QTableWidget(self)
            self.tableWidget.setGeometry(QtCore.QRect(10, 150, 581, 211))
            self.tableWidget.setObjectName("tableWidget")
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Улица"])
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            
            # Ввод новой фамилии
            self.fam_text = QtWidgets.QLineEdit(self)
            self.fam_text.setGeometry(QtCore.QRect(10, 10, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.fam_text.setFont(font)
            self.fam_text.setObjectName("str_text")
            self.fam_text.setPlaceholderText("Введите улицу")
            
            self.btn = QtWidgets.QPushButton(self)
            self.btn.setGeometry(QtCore.QRect(250, 10, 30, 30))
            font = QtGui.QFont()
            self.btn.setObjectName("btn")
            self.btn.clicked.connect(self.print_table)
            
             # Кнопка удаления
            self.remove_btn = QtWidgets.QPushButton(self)
            self.remove_btn.setGeometry(QtCore.QRect(10, 50, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.remove_btn.setFont(font)
            self.remove_btn.setObjectName("remove_btn")
            self.remove_btn.setText("Удалить")
            self.remove_btn.clicked.connect(self.def_remove)
            
            # Кнопка обновить
            self.update_btn = QtWidgets.QPushButton(self)
            self.update_btn.setGeometry(QtCore.QRect(170, 50, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.update_btn.setFont(font)
            self.update_btn.setObjectName("update_btn")
            self.update_btn.setText("Изменить")
            self.update_btn.clicked.connect(self.def_update)
            
            # Кнопка добавить
            self.add_btn = QtWidgets.QPushButton(self)
            self.add_btn.setGeometry(QtCore.QRect(10, 90, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.add_btn.setFont(font)
            self.add_btn.setObjectName("add_btn")
            self.add_btn.setText("Добавить")
            self.add_btn.clicked.connect(self.def_add)
            
            # Кнопка искать
            self.search_btn = QtWidgets.QPushButton(self)
            self.search_btn.setGeometry(QtCore.QRect(170, 90, 150, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.search_btn.setFont(font)
            self.search_btn.setObjectName("search_btn")
            self.search_btn.setText("Искать")
            self.search_btn.clicked.connect(self.def_search)
            
        # функция вывода
        def print_table(self):
            cursor.execute("select * from str")
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
                    
        def def_add(self):
            f = self.fam_text.text()
            
            if f != '':
                cursor.execute("INSERT INTO str(str_id, str_val) values (default, '" + f + "')")
                conn.commit()
                self.print_table()
                
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите улицу, чтобы ее добавить")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
                    
        def def_search(self):
            request = "select * from str where "
            f = self.fam_text.text()
            if f != '':
                request = request + "str_val = '" + f + "'"
            if request.endswith('where '):
                request = request[:len(request)-6]
            
            cursor.execute(request)
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(2):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
            
        def def_remove(self):
            cur = self.tableWidget.currentRow()
            n = self.tableWidget.item(cur,0).text()
            s = "Вы уверены, что хотите удалить " + str(cur + 1) + " строку?"
            otvet = QtWidgets.QMessageBox.question(self, 'Внимание!', s, QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
            if otvet == QtWidgets.QMessageBox.StandardButton.Yes:
                request = "delete from str where str_id = "+str(n)
                cursor.execute(request)
                self.print_table()
                
        def def_update(self):
            cur = self.tableWidget.currentRow()
            id = self.tableWidget.item(cur,0).text()
            request = "update str set "
            
            f = self.fam_text.text()
            if f != '':
                request = request + "str_val = '" + f + "'"
            if request.endswith('set '):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите новую улицу")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
            else:
                request = request + " where str_id = "+str(id)
                cursor.execute(request)
                conn.commit()
                self.print_table()
            
    # Класс для визуализации
    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            self.mainwindow = MainWindow
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(600, 600)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            
            # Таблица выводв
            self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
            self.tableWidget.setGeometry(QtCore.QRect(10, 350, 581, 211))
            self.tableWidget.setObjectName("tableWidget")
            self.tableWidget.setColumnCount(9)
            self.tableWidget.setRowCount(0)
            self.tableWidget.setHorizontalHeaderLabels(["ID", "Фамилия", "Имя", "Отчество", "Улица", "Дом", "Корпус", "Номер квартиры", "Номер телефона"])
            self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
            self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            
            # Кнопка добавления фамилии
            self.fam_add = QtWidgets.QPushButton(self.centralwidget)
            self.fam_add.setGeometry(QtCore.QRect(330, 10, 31, 31))
            self.fam_add.setObjectName("fam_add")
            self.fam_add.clicked.connect(self.def_fam_add)
            
            # Кнопка добавления имени
            self.nam_add = QtWidgets.QPushButton(self.centralwidget)
            self.nam_add.setGeometry(QtCore.QRect(330, 50, 31, 31))
            self.nam_add.setObjectName("nam_add")
            self.nam_add.clicked.connect(self.def_nam_add)
            
            # Кнопка добавления отчества
            self.otc_add = QtWidgets.QPushButton(self.centralwidget)
            self.otc_add.setGeometry(QtCore.QRect(330, 90, 31, 31))
            self.otc_add.setObjectName("otc_add")
            self.otc_add.clicked.connect(self.def_otc_add)
            
            # Кнопка добавления улицы
            self.str_add = QtWidgets.QPushButton(self.centralwidget)
            self.str_add.setGeometry(QtCore.QRect(330, 130, 31, 31))
            self.str_add.setObjectName("str_add")
            self.str_add.clicked.connect(self.def_str_add)
            
            # Выпадающий список фамилий
            self.fam = QtWidgets.QComboBox(self.centralwidget)
            self.fam.setGeometry(QtCore.QRect(30, 10, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.fam.setFont(font)
            self.fam.setEditable(True)
            self.fam.setMaxVisibleItems(30)
            self.fam.setObjectName("fam")
            cursor.execute("select f_val from fam")
            fam_list = cursor.fetchall()
            self.fam.addItem('')
            for i in range(len(fam_list)):
                self.fam.addItem(str(fam_list[i][0]))
            
            # Выпадающий список имен
            self.nam = QtWidgets.QComboBox(self.centralwidget)
            self.nam.setGeometry(QtCore.QRect(30, 50, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.nam.setFont(font)
            self.nam.setEditable(True)
            self.nam.setMaxVisibleItems(30)
            self.nam.setObjectName("nam")
            cursor.execute("select n_val from nam")
            nam_list = cursor.fetchall()
            self.nam.addItem('')
            for i in range(len(nam_list)):
                self.nam.addItem(str(nam_list[i][0]))
            
            # Выпадающий список отчеств
            self.otc = QtWidgets.QComboBox(self.centralwidget)
            self.otc.setGeometry(QtCore.QRect(30, 90, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.otc.setFont(font)
            self.otc.setEditable(True)
            self.otc.setMaxVisibleItems(30)
            self.otc.setObjectName("otc")
            cursor.execute("select otc_val from otc")
            otc_list = cursor.fetchall()
            self.otc.addItem('')
            for i in range(len(otc_list)):
                self.otc.addItem(str(otc_list[i][0]))
            
            # Выпадающий список улиц
            self.str = QtWidgets.QComboBox(self.centralwidget)
            self.str.setGeometry(QtCore.QRect(30, 130, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.str.setFont(font)
            self.str.setEditable(True)
            self.str.setMaxVisibleItems(30)
            self.str.setObjectName("str")
            cursor.execute("select str_val from str")
            str_list = cursor.fetchall()
            self.str.addItem('')
            for i in range(len(str_list)):
                self.str.addItem(str(str_list[i][0]))
            
            
            self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
            self.layoutWidget.setGeometry(QtCore.QRect(280, 210, 291, 101))
            self.layoutWidget.setObjectName("layoutWidget")
            self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
            self.gridLayout.setContentsMargins(0, 0, 0, 0)
            self.gridLayout.setObjectName("gridLayout")
            
            # Кнопка удаления
            self.remove_btn = QtWidgets.QPushButton(self.layoutWidget)
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.remove_btn.setFont(font)
            self.remove_btn.setObjectName("remove_btn")
            self.gridLayout.addWidget(self.remove_btn, 1, 0, 1, 1)
            self.remove_btn.clicked.connect(self.def_remove)
            
            # Кнопка обновить
            self.update_btn = QtWidgets.QPushButton(self.layoutWidget)
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.update_btn.setFont(font)
            self.update_btn.setObjectName("update_btn")
            self.gridLayout.addWidget(self.update_btn, 0, 1, 1, 1)
            self.update_btn.clicked.connect(self.def_update)
            
            # Кнопка добавить
            self.add_btn = QtWidgets.QPushButton(self.layoutWidget)
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setItalic(False)
            font.setWeight(75)
            self.add_btn.setFont(font)
            self.add_btn.setObjectName("add_btn")
            self.gridLayout.addWidget(self.add_btn, 1, 1, 1, 1)
            self.add_btn.clicked.connect(self.def_add)
            
            # Кнопка искать
            self.search_btn = QtWidgets.QPushButton(self.layoutWidget)
            font = QtGui.QFont()
            font.setPointSize(10)
            font.setBold(True)
            font.setWeight(75)
            self.search_btn.setFont(font)
            self.search_btn.setObjectName("search_btn")
            self.gridLayout.addWidget(self.search_btn, 0, 0, 1, 1)
            self.search_btn.clicked.connect(self.def_search)
            
            # Ввод номера дома
            self.bldn_text = QtWidgets.QLineEdit(self.centralwidget)
            self.bldn_text.setGeometry(QtCore.QRect(30, 170, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.bldn_text.setFont(font)
            self.bldn_text.setObjectName("bldn_text")
            
            # Ввод номера корпуса
            self.bldn_k_text = QtWidgets.QLineEdit(self.centralwidget)
            self.bldn_k_text.setGeometry(QtCore.QRect(30, 210, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.bldn_k_text.setFont(font)
            self.bldn_k_text.setObjectName("bldn_k_text")
            
            # Ввод номера квартиры
            self.flat_text = QtWidgets.QLineEdit(self.centralwidget)
            self.flat_text.setGeometry(QtCore.QRect(30, 250, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.flat_text.setFont(font)
            self.flat_text.setObjectName("flat_text")
            
            # Ввод номера телефона
            self.number_text = QtWidgets.QLineEdit(self.centralwidget)
            self.number_text.setGeometry(QtCore.QRect(30, 290, 231, 31))
            font = QtGui.QFont()
            font.setPointSize(10)
            self.number_text.setFont(font)
            self.number_text.setObjectName("number_text")
            
            
            MainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(MainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 18))
            self.menubar.setObjectName("menubar")
            MainWindow.setMenuBar(self.menubar)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)

            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)

        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "База данных"))
            self.fam_add.setText(_translate("MainWindow", "..."))
            self.nam_add.setText(_translate("MainWindow", "..."))
            self.otc_add.setText(_translate("MainWindow", "..."))
            self.str_add.setText(_translate("MainWindow", "..."))
            self.remove_btn.setText(_translate("MainWindow", "Удалить"))
            self.update_btn.setText(_translate("MainWindow", "Изменить"))
            self.add_btn.setText(_translate("MainWindow", "Добавить"))
            self.search_btn.setText(_translate("MainWindow", "Найти"))
            self.bldn_text.setPlaceholderText(_translate("MainWindow", "Введите номер дома"))
            self.bldn_k_text.setPlaceholderText(_translate("MainWindow", "Введите номер корпуса"))
            self.flat_text.setPlaceholderText(_translate("MainWindow", "Введите номер квартиры"))
            self.number_text.setPlaceholderText(_translate("MainWindow", "Введите номер телефона"))
        
        # функция вывода
        def print_table(self):
            cursor.execute("select main_id, f_val, n_val, otc_val, str_val, bldn, bldn_k, app, telef from main join fam on fam.f_id = main.fam_ join nam on nam.n_id = main.nam_ join otc on otc.otc_id = main.otc_ join str on str.str_id = main.str_")
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(9):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
                    
        # Функция обновления
        def def_update(self):
            cur = self.tableWidget.currentRow()
            id = self.tableWidget.item(cur,0).text()
            request = "update main set "
            
            f = self.fam.currentText()
            if f != '':
                cursor.execute("SELECT f_id from fam where f_val = '" + f + "'" )
                f_table = cursor.fetchall()
                f_n = str(f_table[0][0])
                request = request + "fam_ = " +f_n + ","
            
            n = self.nam.currentText()
            if n != '':
                cursor.execute("SELECT n_id from nam where n_val = '" + n + "'" )
                n_table = cursor.fetchall()
                n_n = str(n_table[0][0])
                request = request + "nam_ = " +n_n + ","
            
            o = self.otc.currentText()
            if o != '':
                cursor.execute("SELECT otc_id from otc where otc_val = '" + o + "'" )
                o_table = cursor.fetchall()
                o_n = str(o_table[0][0])
                request = request + "otc_ = " +o_n + ","
            
            s = self.str.currentText()
            if s != '':
                cursor.execute("SELECT str_id from str where str_val = '" + s + "'" )
                s_table = cursor.fetchall()
                s_n = str(s_table[0][0])
                request = request + "str_ = " +s_n + ","
            
            b = self.bldn_text.text()
            if b != '':
                request = request + "bldn = '" +b+"'" + ","
            b_k = self.bldn_k_text.text()
            if b != '':
                request = request + "bldn_k = '" +b_k+"'" + ","
            a = self.flat_text.text()
            if a != '':
                request = request + "app = " +b + ","
            num = self.number_text.text()
            if num != '':
                request = request + "telef = '" +b+"'" + ","
            if request.endswith(','):
                request = request[:len(request)-1]
            
            if request.endswith('set '):
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите какую-нибудь новую информацию")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
            else:
                request = request + " where main_id = "+str(id)
                cursor.execute(request)
                conn.commit()
                self.print_table()
        
        # Функция удаления
        def def_remove(self):
            cur = self.tableWidget.currentRow()
            n = self.tableWidget.item(cur,0).text()
            s = "Вы уверены, что хотите удалить " + str(cur + 1) + " строку?"
            otvet = QtWidgets.QMessageBox.question(self.mainwindow, 'Внимание!', s, QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No, QtWidgets.QMessageBox.StandardButton.No)
            if otvet == QtWidgets.QMessageBox.StandardButton.Yes:
                request = "delete from main where main_id = "+str(n)
                cursor.execute(request)
                self.print_table()
            
            
        # Функция поиска
        def def_search(self):
            request = "select main_id, f_val, n_val, otc_val, str_val, bldn, bldn_k, app, telef from main join fam on fam.f_id = main.fam_ join nam on nam.n_id = main.nam_ join otc on otc.otc_id = main.otc_ join str on str.str_id = main.str_ where "
            f = self.fam.currentText()
            if f != '':
                cursor.execute("SELECT f_id from fam where f_val = '" + f + "'" )
                f_table = cursor.fetchall()
                f_n = str(f_table[0][0])
                request = request + "fam_ = " +f_n + " and "
            
            n = self.nam.currentText()
            if n != '':
                cursor.execute("SELECT n_id from nam where n_val = '" + n + "'" )
                n_table = cursor.fetchall()
                n_n = str(n_table[0][0])
                request = request + "nam_ = " +n_n + " and "
            
            o = self.otc.currentText()
            if o != '':
                cursor.execute("SELECT otc_id from otc where otc_val = '" + o + "'" )
                o_table = cursor.fetchall()
                o_n = str(o_table[0][0])
                request = request + "otc_ = " +o_n + " and "
            
            s = self.str.currentText()
            if s != '':
                cursor.execute("SELECT str_id from str where str_val = '" + s + "'" )
                s_table = cursor.fetchall()
                s_n = str(s_table[0][0])
                request = request + "str_ = " +s_n + " and "
            
            b = self.bldn_text.text()
            if b != '':
                request = request + "bldn = '" +b+"'" + " and "
            b_k = self.bldn_k_text.text()
            if b != '':
                request = request + "bldn_k = '" +b_k+"'" + " and "
            a = self.flat_text.text()
            if a != '':
                request = request + "app = " +b + " and "
            num = self.number_text.text()
            if num != '':
                request = request + "telef = '" +b+"'" + " and "
            if request.endswith('and '):
                request = request[:len(request)-4]
            
            if request.endswith('where '):
                request = request[:len(request)-6]
            
            cursor.execute(request)
            table_updated = cursor.fetchall()
            self.tableWidget.setRowCount(len(table_updated))
            for i in range(len(table_updated)):
                for j in range(9):
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(table_updated[i][j])))
            
            
            
        # Функция добавления
        def def_add(self):
            f = self.fam.currentText()
            n = self.nam.currentText()
            o = self.otc.currentText()
            s = self.str.currentText()
            b = self.bldn_text.text()
            b_k = self.bldn_k_text.text()
            a = self.flat_text.text()
            num = self.number_text.text()
            
            if f and n and o and s and b and b_k and a and num:
                cursor.execute("SELECT f_id from fam where f_val = '" + f + "'" )
                f_table = cursor.fetchall()
                f_n = str(f_table[0][0])
                
                cursor.execute("SELECT n_id from nam where n_val = '" + n + "'" )
                n_table = cursor.fetchall()
                n_n = str(n_table[0][0])
                
                cursor.execute("SELECT otc_id from otc where otc_val = '" + o + "'" )
                o_table = cursor.fetchall()
                o_n = str(o_table[0][0])
                
                cursor.execute("SELECT str_id from str where str_val = '" + s + "'" )
                s_table = cursor.fetchall()
                s_n = str(s_table[0][0])
                
                cursor.execute("INSERT INTO main(main_id, fam_, nam_, otc_, str_, bldn, bldn_k, app, telef) values (default, " + f_n + ","+n_n+","+o_n+","+s_n+", '"+ b + "', '"+b_k+"', "+a+", '"+num+"')")
                conn.commit()
                self.print_table()
                
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText("Введите все поля, чтобы добавить нового человека")
                msg.setWindowTitle("Внимание!")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                msg.exec_()
        
        # Функция добавления новой фамилии
        def def_fam_add(self):
            self.w1 = Window_fam()
            self.w1.show()
                    
        # Функция добавления нового имени
        def def_nam_add(self):
            self.w1 = Window_nam()
            self.w1.show()
                    
        # Функция добавления нового отчества
        def def_otc_add(self):
            self.w1 = Window_otc()
            self.w1.show()
                    
         # Функция добавления новой улицы
        def def_str_add(self):
            self.w1 = Window_str()
            self.w1.show()
                
                
        

    if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        ui.print_table()
        MainWindow.show()
        sys.exit(app.exec_())

except (Exception, Error) as error:
    print("Ошибки при работе с PostgreSQL", error)
finally:
    if conn:
        cursor.close()
        conn.close()
        print("Соединение с PostgreSQL закрыто")