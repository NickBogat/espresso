import sys

import sqlite3
from PyQt5 import QtSql, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QDialog
import UI.addEditCoffeeForm, UI.addPost, UI.editPost, UI.main


class MyWidget(QMainWindow, UI.main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Кофе')
        self.pushButton.clicked.connect(self.run)
        self.choiceButton.hide()
        self.updateButton.hide()
        self.choiceButton.clicked.connect(self.choice)
        self.db_name = None
        self.new_window = None
        self.updateButton.clicked.connect(self.load_data)

    def run(self):
        try:
            fname = QFileDialog.getOpenFileName(self, 'Выбрать базу данных', '',
                                                'Файл (*.sqlite);;Файл (*.sqlite3);;Все файлы (*)')[0]
            self.db_name = fname
            self.load_data()
            self.choiceButton.show()
            self.updateButton.show()
        except Exception as er:
            print(er)

    def load_data(self):
        con = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        con.setDatabaseName(self.db_name)
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

    def choice(self):
        try:
            if self.new_window is None:
                self.new_window = ChoiceWindow(self.db_name)
            self.new_window.show()
        except Exception as er:
            print(er)


class ChoiceWindow(QMainWindow, UI.addEditCoffeeForm.Ui_MainWindow):
    def __init__(self, db_name):
        super().__init__()
        self.db_name = db_name
        self.setupUi(self)
        self.setWindowTitle('Изменение/добавление записей')
        self.con = sqlite3.connect(self.db_name)
        self.selectButton.clicked.connect(self.change)
        self.addPostButton.clicked.connect(self.add_post)
        self.tableWidget.cellClicked.connect(self.sel)
        self.selected_row = None
        self.show_data()
        self.updateButton.clicked.connect(self.show_data)

    def sel(self):
        self.selected_row = self.tableWidget.currentRow() + 1
        self.show_data()

    def item_changed(self, item):
        self.modified[self.titles[item.column()]] = item.text()

    def change(self):
        try:
            if self.selected_row:
                post_id = self.tableWidget.item(self.selected_row - 1, 0).text()
                print(post_id)
                post_id = int(post_id)
                edit_form = ChangePost(post_id, self.db_name)
                edit_form.exec_()
        except Exception as er:
            print(er)

    def add_post(self):
        add_form = AddPost(self.db_name)
        add_form.exec_()

    def show_data(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM data").fetchall()
        self.tableWidget.setRowCount(len(result))
        if not result:
            self.statusBar().showMessage('Ничего не нашлось')
            return
        else:
            self.statusBar().showMessage(f"Данные есть")
        self.tableWidget.setColumnCount(len(result[0]))
        self.titles = [description[0] for description in cur.description]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


class ChangePost(QDialog, UI.editPost.Ui_Dialog):
    def __init__(self, post_id, db_name):
        super().__init__()
        self.post_id = post_id
        self.setupUi(self)
        self.con = sqlite3.connect(db_name)
        self.pushButton.clicked.connect(self.save)
        cur = self.con.cursor()
        row_data = [str(i) for i in list(cur.execute("""SELECT * FROM data WHERE id = ?""", (self.post_id,)))[0][1:]]
        print(row_data)
        self.sortEdit.setText(row_data[0])
        self.fryEdit.setText(row_data[1])
        self.formEdit.setText(row_data[2])
        self.tasteEdit.setText(row_data[3])
        self.priceEdit.setText(row_data[4])
        self.weightEdit.setText(row_data[5])

    def save(self):
        try:
            cur = self.con.cursor()
            query = """UPDATE data SET name = ?, degree = ?, form = ?, taste = ?, price = ?, volume = ? WHERE id = ?"""
            cur.execute(query, (self.sortEdit.text(), self.fryEdit.text(), self.formEdit.text(),
                                self.tasteEdit.text(), self.priceEdit.text(),
                                self.weightEdit.text(), self.post_id))
            self.con.commit()
            self.accept()
        except Exception as er:
            print(er)


class AddPost(QDialog, UI.addPost.Ui_Dialog):
    def __init__(self, db_name):
        super().__init__()
        self.con = sqlite3.connect(db_name)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.save)

    def save(self):
        try:
            cur = self.con.cursor()
            query = """INSERT INTO data (name, degree, form, taste, price, volume) VALUES (?, ?, ?, ?, ?, ?)"""
            cur.execute(query, (self.sortEdit.text(), self.fryEdit.text(), self.formEdit.text(),
                                self.tasteEdit.text(), self.priceEdit.text(),
                                self.weightEdit.text()))
            self.con.commit()
            self.accept()
        except Exception as er:
            print(er)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
