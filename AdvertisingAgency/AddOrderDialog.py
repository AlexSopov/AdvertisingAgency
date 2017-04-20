from PyQt5 import QtSql
from datetime import datetime

from PyQt5.QtWidgets import *


class AddOrderDialog(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        form_layout = QFormLayout()

        self.list_billboards = QComboBox()
        self.list_companies = QComboBox()

        self.date_ad_start = QDateEdit()
        self.date_ad_end = QDateEdit()

        self.making_price = QSpinBox()
        self.posting_price = QSpinBox()

        button_ok = QPushButton('&Сохранить')
        button_ok.clicked.connect(self.accept)

        button_cancel = QPushButton('&Отмена')
        button_cancel.clicked.connect(self.reject)

        horizontal_layout_buttons = QHBoxLayout()
        horizontal_layout_buttons.addWidget(button_cancel)
        horizontal_layout_buttons.addWidget(button_ok)

        form_layout.addRow('Рекламный щит:', self.list_billboards)
        form_layout.addRow('Организация:', self.list_companies)
        form_layout.addRow('Дата размещения:', self.date_ad_start)
        form_layout.addRow('Конец размещения:', self.date_ad_end)
        form_layout.addRow('Цена изготовления:', self.making_price)
        form_layout.addRow('Цена размещения:', self.posting_price)
        form_layout.addItem(horizontal_layout_buttons)

        self.query_model_billboards = QtSql.QSqlQueryModel()
        self.query_model_companies = QtSql.QSqlQueryModel()
        self.initialize_lists()

        self.initialize_date_selector()
        self.initialize_price_selector()

        self.setWindowTitle('Новый заказ')
        self.setMinimumWidth(300)
        self.setMaximumWidth(500)
        self.setMaximumHeight(self.height())
        self.setLayout(form_layout)

    def initialize_lists(self):
        self.query_model_billboards.setQuery('SELECT * FROM billboards '
                                             'ORDER BY address')
        self.list_billboards.setModel(self.query_model_billboards)
        self.list_billboards.setModelColumn(1)

        self.query_model_companies.setQuery('SELECT id, name FROM companies '
                                            'ORDER BY name')

        self.list_companies.setModel(self.query_model_companies)
        self.list_companies.setModelColumn(1)

    def initialize_date_selector(self):
        self.date_ad_start.setCalendarPopup(True)
        self.date_ad_start.setDate(datetime.today())

        self.date_ad_end.setCalendarPopup(True)
        self.date_ad_end.setDate(datetime.today())

    def initialize_price_selector(self):
        self.making_price.setRange(100, 10e6)
        self.making_price.setValue(100)
        self.making_price.setSingleStep(100)
        self.making_price.setSuffix(' руб.')

        self.posting_price.setRange(100, 10e6)
        self.posting_price.setValue(100)
        self.posting_price.setSingleStep(100)
        self.posting_price.setSuffix(' руб.')

    def validate_data(self, record_billboard):
        ad_start = self.date_ad_start.date()
        ad_end = self.date_ad_end.date()
        if ad_start > ad_end:
            message_box = QMessageBox()
            message_box.setText("Начальная дата не может быть меньше конечной.")
            message_box.setWindowTitle("Ошибка")
            message_box.exec()
            return False

        get_count_orders_query = QtSql.QSqlQuery()
        get_count_orders_query.exec("SELECT COUNT(*) FROM orders "
                                    "WHERE ad_start <= '{start_date}' AND ad_end >= '{start_date}' "
                                    "AND billboard_id = {billboard_id}".
                                    format(start_date=ad_start.toPyDate(), billboard_id=record_billboard.value("id")))
        count = -1
        if get_count_orders_query.isActive():
            get_count_orders_query.first()
            count = get_count_orders_query.value(0)

        if count >= record_billboard.value("surface_count"):
            message_box = QMessageBox()
            message_box.setText("Выбранный рекламный щит не имеет свободный поверхностей "
                                "для указанного периода времени.")
            message_box.setWindowTitle("Ошибка")
            message_box.exec()
            return False

        return True

    def accept(self):
        list_index_billboard = self.list_billboards.currentIndex()
        if list_index_billboard < 0:
            return

        record_billboard = self.query_model_billboards.record(list_index_billboard)
        billboard_id = record_billboard.value("id")

        list_index_company = self.list_companies.currentIndex()
        if list_index_company < 0:
            return

        record_company = self.query_model_companies.record(list_index_company)
        company_id = record_company.value("id")

        if not self.validate_data(record_billboard):
            return

        insert_query = QtSql.QSqlQuery()
        insert_query.prepare("INSERT INTO orders VALUES(NULL, ?, ?, ?, ?, ?, ?, ?)")
        insert_query.addBindValue(billboard_id)
        insert_query.addBindValue(company_id)
        insert_query.addBindValue(str(datetime.today().date()))
        insert_query.addBindValue(str(self.date_ad_start.date().toPyDate()))
        insert_query.addBindValue(str(self.date_ad_end.date().toPyDate()))
        insert_query.addBindValue(self.making_price.value())
        insert_query.addBindValue(self.posting_price.value())
        insert_query.exec_()

        super().accept()