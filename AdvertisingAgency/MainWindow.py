import sys
from PyQt5 import QtSql

from PyQt5.QtCore import QSize
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import *

from BillboardsWidget import BillboardsWidget
from CompaniesWidget import CompaniesWidget
from OrdersWidget import OrdersWidget


# Класс главного окна приложения
class MainWindow(QMainWindow):
    # Инициализация
    def __init__(self):
        super().__init__()

        # Добавление подключения к базе данных
        self.connection = QSqlDatabase.addDatabase('QSQLITE')

        # Инициализация подключения к БД
        self.initialize_data_base_connection()

        # Инициализация элементов управления
        self.initialize_user_interface()

        # Инициализация меню
        self.initialize_menu_bar()

    def initialize_menu_bar(self):
        menu_bar = self.menuBar()
        report_action = menu_bar.addAction('&Сформировать отчет')
        report_action.triggered.connect(self.make_report)

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
        # Подключение к базе данных
        self.connection.setDatabaseName('advertising_agency.db')
        self.connection.open()
        self.connection.exec('PRAGMA foreign_keys = ON')

        # Создание необходимых таблиц
        self.connection.exec('CREATE TABLE IF NOT EXISTS billboards( '
                             'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                             'address TEXT NOT NULL UNIQUE,'
                             'surface_count INTEGER DEFAULT 1)'
                             )
        self.connection.exec('CREATE TABLE IF NOT EXISTS companies('
                             'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                             'name TEXT NOT NULL UNIQUE)')

        self.connection.exec('CREATE TABLE IF NOT EXISTS orders('
                             'id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,'
                             'billboard_id INTEGER NOT NULL,'
                             'company_id INTEGER NOT NULL,'
                             'order_date TEXT NOT NULL,'
                             'ad_start TEXT NOT NULL,'
                             'ad_end TEXT NOT NULL,'
                             'ad_making_price REAL NOT NULL,'
                             'ad_placing_price REAL NOT NULL,'
                             'FOREIGN KEY(billboard_id) REFERENCES billboards(id)'
                             ' ON DELETE CASCADE ON UPDATE NO ACTION,'
                             'FOREIGN KEY(company_id) REFERENCES companies(id)'
                             ' ON DELETE CASCADE ON UPDATE NO ACTION)')

    def closeEvent(self, *args, **kwargs):
        # Закрыть подключение к базе при завершении работы
        self.connection.close()
        QMainWindow.closeEvent(self, *args, **kwargs)

    def make_report(self):
        with open('report.txt', 'w') as file:
            file.write('id|\tОрганизация|\tРекламный щит|\tДата заказа|\tДата начала размещения|'
                       '\tДата конца размещения|\tЦена изготовления рекламы|\tЦена размещения рекламы\n')

            query_str = 'SELECT orders.id, billboard_id, company_id, address, name, ' \
                        'order_date, ad_start, ad_end, ad_making_price, ad_placing_price ' \
                        'FROM orders ' \
                        'INNER JOIN billboards ON billboards.id = billboard_id ' \
                        'INNER JOIN companies ON  companies.id = company_id ' \
                        'ORDER BY ad_start DESC '

            query = QtSql.QSqlQuery()
            query.exec(query_str)

            if query.isActive():
                query.first()
                while query.isValid():
                    file.write("{id}\t{name}\t{address}\t{order_date}\t"
                               "{ad_start}\t{ad_end}\t{ad_making_price}\t{ad_placing_price}\n".format(
                        id=query.value("id"),
                        name=query.value("name"),
                        address=query.value("address"),
                        order_date=query.value("order_date"),
                        ad_start=query.value("ad_start"),
                        ad_end=query.value("ad_end"),
                        ad_making_price=query.value("ad_making_price"),
                        ad_placing_price=query.value("ad_placing_price")
                    ))
                    query.next()

        message_box = QMessageBox()
        message_box.setText("Отчет успешно сформирован. Файл с отчетом находится "
                            "в каталоге с приложением.")
        message_box.setWindowTitle("Отчет")
        message_box.exec()


if __name__ == "__main__":
    application = QApplication(sys.argv)
    executable = MainWindow()
    sys.exit(application.exec_())
