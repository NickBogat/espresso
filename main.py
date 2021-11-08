import sys

from PyQt5 import uic, QtSql, QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPainter, QPolygon
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFileDialog
from random import randint


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.setWindowTitle('Кофе')
        self.pushButton.clicked.connect(self.run)

    def run(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать базу данных', '',
                                                'Файл (*.sqlite);;Файл (*.sqlite3);;Все файлы (*)')[0]
            con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
            con.setDatabaseName(fname)
            con.open()
            stm = QtSql.QSqlTableModel(parent=self.tableView)
            stm.setTable('Coffee')
            stm.select()
            model = QtSql.QSqlQueryModel()
            model.setQuery("""SELECT * FROM data""")
            model.setHeaderData(1, QtCore.Qt.Horizontal, 'Сорт')
            model.setHeaderData(2, QtCore.Qt.Horizontal, 'Обжарка')
            model.setHeaderData(3, QtCore.Qt.Horizontal, 'Форма')
            model.setHeaderData(4, QtCore.Qt.Horizontal, 'Вкус')
            model.setHeaderData(5, QtCore.Qt.Horizontal, 'Цена')
            model.setHeaderData(6, QtCore.Qt.Horizontal, 'Вес')

            self.tableView.setModel(model)
            self.tableView.setSelectionBehavior(1)
        except Exception as er:
            print(er)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
