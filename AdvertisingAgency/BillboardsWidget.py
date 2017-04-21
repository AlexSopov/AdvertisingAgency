from PyQt5 import QtCore

from PyQt5 import QtSql

from PyQt5.QtWidgets import *

# Класс виджета, отображающего рекламные щиты в таблице
class BillboardsWidget(QFrame):
    # Инициализация
    def __init__(self):
        super().__init__()

        self.table_model = QtSql.QSqlTableModel()
        self.table_widget = QTableView()

        self.initialize_user_interface()

    # Инициализация представления
    def initialize_user_interface(self):
        vertical_layout = QVBoxLayout()

        self.table_model.setTable('billboards')
        self.table_model.setSort(1, QtCore.Qt.AscendingOrder)
        self.table_model.setHeaderData(1, QtCore.Qt.Horizontal, 'Адрес')
        self.table_model.setHeaderData(2, QtCore.Qt.Horizontal, 'Кол-во поверхностей')
        self.table_model.select()

        self.table_widget.setModel(self.table_model)
        self.table_widget.hideColumn(0)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        label_title = QLabel('<center><b>Рекламные щиты</b></center>')
        button_add_record = QPushButton('Добавить запись')
        button_add_record.clicked.connect(self.add_record)
        button_del_record = QPushButton('Удалить запись')
        button_del_record.clicked.connect(self.del_record)

        vertical_layout.addWidget(label_title)
        vertical_layout.addWidget(self.table_widget)
        vertical_layout.addWidget(button_add_record)
        vertical_layout.addWidget(button_del_record)

        self.setLayout(vertical_layout)
        self.setFrameShape(QFrame.StyledPanel)

    # Обработка нажатия кнопки "Добавить новую запись"
    def add_record(self):
        self.table_model.insertRow(self.table_model.rowCount())

    # Обработка нажатия кнопки "Удалить запись"
    def del_record(self):
        self.table_model.removeRow(self.table_widget.currentIndex().row())
        self.table_model.select()

