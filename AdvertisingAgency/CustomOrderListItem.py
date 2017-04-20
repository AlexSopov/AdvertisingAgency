from datetime import datetime

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget


class CustomOrderListItem(QWidget):
    def __init__(self, _id, company_name, billboard_name, order_date, order_start, order_end, creating_price,
                 posting_price):
        super().__init__()
        self.id = _id

        main_horizontal_layout = QHBoxLayout()

        self.label_icon = QLabel()
        self.label_status = QLabel()
        self.label_title = QLabel()
        self.label_order_date = QLabel()
        self.label_period = QLabel()
        self.label_creating_price = QLabel()
        self.label_posting_price = QLabel()

        icon_vertical_layout = QVBoxLayout()
        icon_vertical_layout.addWidget(self.label_icon, alignment=QtCore.Qt.AlignCenter)
        icon_vertical_layout.addWidget(self.label_status)
        icon_vertical_layout.setSpacing(0)

        description_vertical_layout = QVBoxLayout()
        description_vertical_layout.addWidget(self.label_title)
        description_vertical_layout.addWidget(self.label_order_date)
        description_vertical_layout.addWidget(self.label_period)
        description_vertical_layout.setSpacing(0)

        price_vertical_layout = QVBoxLayout()
        price_vertical_layout.addWidget(self.label_creating_price, alignment=QtCore.Qt.AlignRight)
        price_vertical_layout.addWidget(self.label_posting_price, alignment=QtCore.Qt.AlignRight)
        price_vertical_layout.setSpacing(0)

        main_horizontal_layout.addLayout(icon_vertical_layout, 0)
        main_horizontal_layout.addLayout(description_vertical_layout, 1)
        main_horizontal_layout.addLayout(price_vertical_layout)

        self.set_icon_status(order_start, order_end)
        self.set_title(company_name, billboard_name)
        self.set_date(order_date, order_start, order_end)
        self.set_price(creating_price, posting_price)

        self.setLayout(main_horizontal_layout)

    def set_icon_status(self, order_start, order_end):
        current_date = datetime.today()
        order_start_date = datetime.strptime(order_start, '%Y-%m-%d')
        order_order_end = datetime.strptime(order_end, '%Y-%m-%d')

        pix_map = None
        if current_date.day < order_start_date.day:
            pix_map = QtGui.QPixmap('images/waiting_icon.png')
            self.label_status.setText("В ожидании")
        elif current_date.day > order_order_end.day:
            pix_map = QtGui.QPixmap('images/ready_icon.png')
            self.label_status.setText("Выполнено")
        else:
            pix_map = QtGui.QPixmap('images/in_process_icon.png')
            self.label_status.setText("Исполняется")

        self.label_icon.setFixedSize(QSize(40, 40))
        self.label_icon.setPixmap(pix_map.scaled(40, 40, transformMode=QtCore.Qt.SmoothTransformation))

    def set_title(self, company_name, billboard_name):
        self.label_title.setText('Заказ на рекламный щит: "{billboard}" организации "{company}"'.
                                 format(billboard=billboard_name, company=company_name))

    def set_date(self, order_date, order_start, order_end):
        self.label_order_date.setText('Дата заказа: {date}'.format(date=order_date))
        self.label_period.setText('Период размещения рекламы: {from_date} - {till_date}'.
                                  format(from_date=order_start, till_date=order_end))

    def set_price(self, creating_price, posting_price):
        self.label_creating_price.setText('Цена изготовления: {price} руб.'.format(price=creating_price))
        self.label_posting_price.setText('Цена размещения: {price} руб.'.format(price=posting_price))

    def get_id(self):
        return self.id