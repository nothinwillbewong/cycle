from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# OTHERS____________________________________
from pathlib import Path
from PIL import Image
from enum import Enum
from math import *
import numpy as np
import sys
import os
import pandas as pd
import csv
#############


class model_results(QObject):

    # Initializer:
    def __init__(self):
        super().__init__()
        

        # ui_components:
        self.__left = Left()
        self.__right= Right()

    # Get instances Right & Left:
    def getLeftWidget(self):
        return self.__left

    def getRightLayout(self):
        return self.__right
    




class Left(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.results_vlayout = QVBoxLayout(self)

        self.result_label = QLabel('Results')
        self.result_label.setObjectName('result_label')
        self.result_label.setFixedSize(100,25)

        self.model = QStandardItemModel()
        self.model.setColumnCount(2)
        self.model.setHorizontalHeaderLabels(['Isotope','Concentration'])

        self.table_view = QTableView()
        self.table_view.setObjectName('result_table')
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.export_hlayout = QHBoxLayout(self)

        self.export_label = QLabel('Export as...')
        self.export_label.setObjectName('export_label')

        self.csv_pb = QPushButton('csv')
        self.csv_pb.setObjectName('result_csv_pb')

        self.txt_pb = QPushButton('txt')
        self.txt_pb.setObjectName('result_txt_pb')

        self.export_hlayout.addWidget(self.export_label)
        self.export_hlayout.addWidget(self.csv_pb)
        self.export_hlayout.addWidget(self.txt_pb)

        self.results_vlayout.addWidget(self.result_label)
        self.results_vlayout.addWidget(self.table_view)
        self.results_vlayout.addLayout(self.export_hlayout)


        

class Right(QVBoxLayout):
    
    def __init__(self):
        super().__init__()

        self.init_cond_label = QLabel('Initial Conditions')
        self.init_cond_label.setObjectName('init_cond_label')
        self.init_cond_label.setFixedSize(100,25)

        self.model = QStandardItemModel()
        self.model.setColumnCount(2)
        self.model.setHorizontalHeaderLabels(['Isotope','Concentration'])

        self.table_view = QTableView()
        self.table_view.setObjectName('init_cond_table')
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        method_hbox = QHBoxLayout()

        self.method_label = QLabel('Method')
        self.method_label.setObjectName('method_label')

        self.method_box = QComboBox()
        self.method_box.setObjectName('method_box')

        method_hbox.addWidget(self.method_label)
        method_hbox.addWidget(self.method_box)

        time_hbox = QHBoxLayout()

        self.time_label = QLabel('Time')
        self.time_label.setObjectName('time_label')

        self.time_lineedit = QLineEdit()
        self.time_lineedit.setObjectName('time_lineedit')

        self.time_unit_box = QComboBox()
        self.time_unit_box.setObjectName('time_unit_box')

        time_hbox.addWidget(self.time_label)
        time_hbox.addWidget(self.time_lineedit)
        time_hbox.addWidget(self.time_unit_box)


        self.calculate_pb = QPushButton('Calculate')
        self.calculate_pb.setObjectName('calculate_pb')
        self.calculate_pb.setFixedSize(150,50)

        self.calculation_vlayout = QVBoxLayout()

        self.heat_density_cb = QCheckBox('HeatDensity')
        self.heat_density_cb.setObjectName('heat_density_cb')


        self.product_cb = QCheckBox('\u03c3'+'N')
        self.product_cb.setObjectName('product_cb')

        self.concentration_cb = QCheckBox('Concentration')
        self.concentration_cb.setObjectName('concentration_cb')

        self.calculation_vlayout.addWidget(self.heat_density_cb)
        self.calculation_vlayout.addWidget(self.product_cb)
        self.calculation_vlayout.addWidget(self.concentration_cb)



        self.addWidget(self.init_cond_label)
        self.addWidget(self.table_view)
        self.addLayout(method_hbox)
        self.addLayout(time_hbox)
        self.addLayout(self.calculation_vlayout)
        self.addWidget(self.calculate_pb, alignment=Qt.AlignCenter)








