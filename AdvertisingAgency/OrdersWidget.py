from datetime import datetime

from PyQt5 import QtSql

from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from AddOrderDialog import AddOrderDialog
from CustomOrderListItem import CustomOrderListItem


class OrdersWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.list_widget = QListWidget()
        self.empty_text_widget = QLabel("<center>"
                                        "Не найдено данных для отображения<br>"
                                        "Нажмите <b>'Добавить заказ'</b> для добавления нового заказа"
                                        "</center>")

        self.initialize_user_interface()
        self.initialize_list()

    def initialize_user_interface(self):
        main_vertical_layout = QVBoxLayout()

        self.empty_text_widget.setVisible(False)
        self.empty_text_widget.setStyleSheet("background-color: white;"
                                             "border: 1px solid gray;")

        label_title = QLabel("<center>Заказы</center>")
        label_title.setStyleSheet("font-size: 17pt")

        button_add_new_order = QPushButton(QIcon('images/add_icon.png'), "Добавить заказ")
        button_add_new_order.setIconSize(QSize(24, 24))
        button_add_new_order.setStyleSheet("padding: 5px 20px")
        button_add_new_order.clicked.connect(self.add_new_order)

        button_del_order = QPushButton(QIcon('images/add_icon.png'), "Удалить заказ")
        button_del_order.setIconSize(QSize(24, 24))
        button_del_order.setStyleSheet("padding: 5px 20px")
        button_del_order.clicked.connect(self.del_order)

        horizontal_button_layout = QHBoxLayout()
        horizontal_button_layout.addWidget(button_del_order, alignment=QtCore.Qt.AlignRight)
        horizontal_button_layout.addWidget(button_add_new_order, alignment=QtCore.Qt.AlignRight)
        horizontal_button_layout.setStretch(0, 1)
        horizontal_button_layout.setStretch(1, 0)

        main_vertical_layout.addWidget(label_title)
        main_vertical_layout.addWidget(self.initialize_filter_view())
        main_vertical_layout.addWidget(self.list_widget)
        main_vertical_layout.addWidget(self.empty_text_widget, 1)
        main_vertical_layout.addLayout(horizontal_button_layout)

        self.setLayout(main_vertical_layout)

    def initialize_filter_view(self):
        group_box_filter = QGroupBox('Фильтр')
        layout_filter = QHBoxLayout()

        left_form = QFormLayout()
        right_form = QFormLayout()

        # Billboard
        self.check_box_billboard = QCheckBox('Рекламный щит: ')
        self.check_box_billboard.stateChanged.connect(lambda:
                                                      (
                                                          self.list_billboards.setEnabled(
                                                              not self.list_billboards.isEnabled()),
                                                          self.initialize_list())
                                                      )

        self.list_billboards = QComboBox()
        self.query_model_billboards = QtSql.QSqlQueryModel()
        self.query_model_billboards.setQuery('SELECT * FROM billboards '
                                        'ORDER BY address')
        self.list_billboards.setModel(self.query_model_billboards)
        self.list_billboards.setModelColumn(1)
        self.list_billboards.setEnabled(False)
        self.list_billboards.currentIndexChanged.connect(lambda: self.initialize_list())

        # Company
        self.check_box_company = QCheckBox('Организация-орендатор: ')
        self.check_box_company.stateChanged.connect(lambda:
                                                    (
                                                        self.list_companies.setEnabled(
                                                            not self.list_companies.isEnabled()),
                                                        self.initialize_list())
                                                    )

        self.list_companies = QComboBox()
        self.query_model_companies = QtSql.QSqlQueryModel()
        self.query_model_companies.setQuery('SELECT * FROM companies '
                                       'ORDER BY name')
        self.list_companies.setModel(self.query_model_companies)
        self.list_companies.setModelColumn(1)
        self.list_companies.setEnabled(False)
        self.list_companies.currentIndexChanged.connect(lambda: self.initialize_list())

        # Order date
        self.check_box_order_date = QCheckBox('Дата заказа: ')
        self.check_box_order_date.stateChanged.connect(lambda:
                                                       (
                                                           self.date_edit_order_date.setEnabled(
                                                               not self.date_edit_order_date.isEnabled()),
                                                           self.initialize_list())
                                                       )
        self.date_edit_order_date = QDateEdit()
        self.date_edit_order_date.setCalendarPopup(True)
        self.date_edit_order_date.setDate(datetime.today())
        self.date_edit_order_date.setEnabled(False)
        self.date_edit_order_date.dateChanged.connect(lambda: self.initialize_list())

        # Order date
        self.check_box_order_pub = QCheckBox('Дата размещения: ')
        self.check_box_order_pub.stateChanged.connect(lambda:
                                                      (
                                                          self.date_edit_order_pub.setEnabled(
                                                              not self.date_edit_order_pub.isEnabled()),
                                                          self.initialize_list())
                                                      )
        self.date_edit_order_pub = QDateEdit()
        self.date_edit_order_pub.setCalendarPopup(True)
        self.date_edit_order_pub.setDate(datetime.today())
        self.date_edit_order_pub.setEnabled(False)
        self.date_edit_order_pub.dateChanged.connect(lambda: self.initialize_list())

        left_form.addRow(self.check_box_billboard, self.list_billboards)
        left_form.addRow(self.check_box_company, self.list_companies)
        right_form.addRow(self.check_box_order_date, self.date_edit_order_date)
        right_form.addRow(self.check_box_order_pub, self.date_edit_order_pub)

        layout_filter.addLayout(left_form)
        layout_filter.addLayout(right_form)
        group_box_filter.setLayout(layout_filter)

        return group_box_filter

    def initialize_list(self):
        items_count = 0

        self.list_widget.clear()

        query_str = 'SELECT orders.id, billboard_id, company_id, address, name, ' \
                    'order_date, ad_start, ad_end, ad_making_price, ad_placing_price ' \
                    'FROM orders ' \
                    'INNER JOIN billboards ON billboards.id = billboard_id ' \
                    'INNER JOIN companies ON  companies.id = company_id '

        if self.check_box_company.isChecked() or self.check_box_billboard.isChecked() \
                or self.check_box_order_date.isChecked() or self.check_box_order_pub.isChecked():

            query_str += ' WHERE '

            if self.check_box_company.isChecked():
                query_str += ' name = "{name}" AND'.format(name=self.list_companies.currentText())
            if self.check_box_billboard.isChecked():
                query_str += ' address = "{address}" AND'.format(address=self.list_billboards.currentText())
            if self.check_box_order_date.isChecked():
                query_str += ' order_date = "{order_date}" AND'.format(order_date=self.date_edit_order_date.date().toPyDate())
            if self.check_box_order_pub.isChecked():
                query_str += ' ad_start = "{ad_start}" AND'.format(ad_start=self.date_edit_order_pub.date().toPyDate())

            query_str = query_str[0: len(query_str) - 3]

        query_str += ' ORDER BY ad_start DESC '

        query = QtSql.QSqlQuery()
        query.exec(query_str)

        if query.isActive():
            query.first()
            while query.isValid():
                widget = CustomOrderListItem(
                    query.value("id"),
                    query.value("name"),
                    query.value("address"),
                    query.value("order_date"),
                    query.value("ad_start"),
                    query.value("ad_end"),
                    query.value("ad_making_price"),
                    query.value("ad_placing_price"))

                widget_item = QListWidgetItem(self.list_widget)
                widget_item.setSizeHint(widget.sizeHint())

                self.list_widget.addItem(widget_item)
                self.list_widget.setItemWidget(widget_item, widget)

                items_count += 1
                query.next()

        if items_count == 0:
            self.list_widget.setVisible(False)
            self.empty_text_widget.setVisible(True)
        else:
            self.list_widget.setVisible(True)
            self.empty_text_widget.setVisible(False)

    def update_filter_data(self):
        self.query_model_billboards.setQuery(self.query_model_billboards.query().lastQuery())
        self.query_model_companies.setQuery(self.query_model_companies.query().lastQuery())

    def add_new_order(self):
        dialog = AddOrderDialog(self)
        result = dialog.exec()

        if result == QDialog.Accepted:
            self.list_widget.clear()
            self.initialize_list()

    def del_order(self):
        current_item = self.list_widget.currentItem()
        if current_item is None:
            return

        current_id = self.list_widget.itemWidget(current_item).get_id()
        query = QtSql.QSqlQuery()
        query.exec("DELETE FROM orders WHERE id = {id}".format(id=current_id))
        self.initialize_list()
