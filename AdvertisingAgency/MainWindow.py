import sys
from PyQt5 import QtSql

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import *

from BillboardsWidget import BillboardsWidget
from CompaniesWidget import CompaniesWidget
from OrdersWidget import OrdersWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.stacked_layout = QStackedLayout()
        self.connection = QSqlDatabase.addDatabase('QSQLITE')

        self.initialize_data_base_connection()
        self.initialize_user_interface()
        self.initialize_menu_bar()

    def initialize_menu_bar(self):
        menu_bar = self.menuBar()
        orders_action = menu_bar.addAction('&Заказы')
        orders_action.triggered.connect(lambda: self.stacked_layout.setCurrentIndex(0))

        orders_action = menu_bar.addAction('&Рекламные щиты')
        orders_action.triggered.connect(lambda: self.stacked_layout.setCurrentIndex(1))

        orders_action = menu_bar.addAction('&Организации')
        orders_action.triggered.connect(lambda: self.stacked_layout.setCurrentIndex(2))

        update_data = menu_bar.addAction('&Обновить данные')
        update_data.triggered.connect(lambda: (self.orders_widget.update_filter_data(),
                                               self.orders_widget.initialize_list()))

        exit_action = menu_bar.addAction('&Выход')
        exit_action.triggered.connect(self.close)

    def initialize_user_interface(self):
        central_widget = QWidget(self)

        box_layout = QHBoxLayout(self)

        self.orders_widget = OrdersWidget()

        tables_splitter = QSplitter(Qt.Vertical)
        tables_splitter.addWidget(BillboardsWidget())
        tables_splitter.addWidget(CompaniesWidget())

        main_splitter = QSplitter(Qt.Horizontal)
        main_splitter.addWidget(self.orders_widget)
        main_splitter.addWidget(tables_splitter)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 0)

        box_layout.addWidget(main_splitter)
        central_widget.setLayout(box_layout)

        self.setCentralWidget(central_widget)

        self.setWindowTitle('Рекламное агентство')
        self.setMinimumSize(QSize(1000, 600))
        self.show()

    def initialize_data_base_connection(self):
        self.connection.setDatabaseName('advertising_agency.db')
        self.connection.open()
        self.connection.exec('PRAGMA foreign_keys = ON')

    def closeEvent(self, *args, **kwargs):
        self.connection.close()
        QMainWindow.closeEvent(self, *args, **kwargs)


if __name__ == "__main__":
    application = QApplication(sys.argv)
    executable = MainWindow()
    sys.exit(application.exec_())
