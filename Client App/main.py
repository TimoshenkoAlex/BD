from PyQt5 import QtWidgets
import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow

import sys

conn = psycopg2.connect(dbname = 'db_214',
                        user = 'postgres',
                        password = '12345',
                        host = 'localhost')
cursor = conn.cursor()

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        
        self.setWindowTitle("База данных")
        self.setGeometry(300, 100, 1300, 900)
        
        self.new_text = QtWidgets.QLabel(self)
        
        self.main_text = QtWidgets.QLabel(self)
        self.main_text.setText("Ты пидор")
        self.main_text.move(100, 100)                    #Расположение объекта
        self.main_text.adjustSize()                      #Подстраивается под размер данных
        
        self.btn = QtWidgets.QPushButton(self)
        self.btn.move(70, 150)
        self.btn.setText("Нажми на меня")
        self.btn.adjustSize()
        self.btn.clicked.connect(self.add_label)
        

    def add_label(self):                                #При нажатии на кнопку
        cursor.execute("SELECT * from main;")
        print(cursor.fetchall())
            
def application():
    app = QApplication(sys.argv)
    window = Window()
    
    window.show()
    sys.exit(app.exec_())
        
    cursor.close()
    conn.close()
        
    
    
if __name__ == "__main__":
    application()

