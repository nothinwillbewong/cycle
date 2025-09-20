from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import matplotlib  
matplotlib.use('Qt5Agg') # Configure the backend to use Qt5  from matplotlib.backends.backend_qt5agg 
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,  NavigationToolbar2QT 
from matplotlib.figure import Figure

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



class model_graph(QObject):

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
    

class CreateCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, nrow =1, ncol=2):
        figure = Figure(figsize=(6,5), dpi=100)
        super(CreateCanvas, self).__init__(figure)
    

class Left(QWidget):
    def __init__(self):
        super().__init__()

        self.scatter_canvas = CreateCanvas(self)

        self.charts_hlayout = QHBoxLayout(self)

        self.export_params_vlayout = QVBoxLayout(self)
        self.dpi_hlayout = QHBoxLayout(self)
        self.param_hlayout = QHBoxLayout(self)
        self.export_hlayout = QHBoxLayout(self)

        self.dpi_label = QLabel('dpi')
        self.dpi_label.setObjectName('dpi_label')

        self.param_label = QLabel('param1')
        self.param_label.setObjectName('param_label')

        self.export_label = QLabel('export as...')
        self.export_label.setObjectName('export_as_label')


        self.dpi_lineedit = QLineEdit()
        self.dpi_lineedit.setObjectName('dpi_lineedit')

        self.param_lineedit = QLineEdit()
        self.param_lineedit.setObjectName('param_lineedit')

        self.export_pdf_pb = QPushButton('pdf')
        self.export_pdf_pb.setObjectName('export_pdf_pb')

        self.export_img_pb = QPushButton('img')
        self.export_img_pb.setObjectName('export_img_pb')



        self.dpi_hlayout.addWidget(self.dpi_label)
        self.dpi_hlayout.addWidget(self.dpi_lineedit)

        self.param_hlayout.addWidget(self.param_label)
        self.param_hlayout.addWidget(self.param_lineedit)

        self.export_hlayout.addWidget(self.export_label)
        self.export_hlayout.addWidget(self.export_pdf_pb)
        self.export_hlayout.addWidget(self.export_img_pb)

        self.export_params_vlayout.addLayout(self.dpi_hlayout)
        self.export_params_vlayout.addSpacing(5)
        self.export_params_vlayout.addLayout(self.param_hlayout)
        self.export_params_vlayout.addSpacing(5)
        self.export_params_vlayout.addLayout(self.export_hlayout)
        self.export_params_vlayout.addSpacing(5)
        self.export_params_vlayout.setAlignment(Qt.AlignCenter)

        self.charts_hlayout.addWidget(self.scatter_canvas)
        self.charts_hlayout.addLayout(self.export_params_vlayout)
        

        self.setLayout(self.charts_hlayout)
        

class Right(QVBoxLayout):

    def __init__(self):
        super().__init__()

        self.type_hlayout = QHBoxLayout()
        self.setObjectName('types_hlayout')

        self.graphtype_label = QLabel('Graphtype')
        self.graphtype_label.setObjectName('graphtype_label')

        self.graphtype_combo = QComboBox()
        self.graphtype_combo.setObjectName('graphtype_combo')

        self.type_hlayout.addWidget(self.graphtype_label)
        self.type_hlayout.addWidget(self.graphtype_combo)

        self.themes_hlayout = QHBoxLayout()

        self.themes_label = QLabel('Themes')
        self.themes_label.setObjectName('themes_label')

        self.themes_combo = QComboBox()
        self.themes_combo.setObjectName('themes_combo')

        self.type_hlayout.addWidget(self.themes_label)
        self.type_hlayout.addWidget(self.themes_combo)

        
        self.legend_label = QLabel('Legend')
        self.legend_label.setObjectName('legend_label')

        self.legend_vlayout = QVBoxLayout()

        self.legend_pos_hlayout = QHBoxLayout()

        self.legend_pos_label = QLabel('Position')
        self.legend_pos_label.setObjectName('legend_pos_label')

        self.legend_pos_combo = QComboBox()
        self.legend_pos_combo.setObjectName('legend_pos_combo')

        self.legend_pos_hlayout.addWidget(self.legend_pos_label)
        self.legend_pos_hlayout.addWidget(self.legend_pos_combo)

        self.legend_size_hlayout = QHBoxLayout()

        self.legend_size_label = QLabel('Size')
        self.legend_size_label.setObjectName('legend_size_label')

        self.legend_size_lineedit = QLineEdit()
        self.legend_size_lineedit.setObjectName('legend_size_lineedit')

        self.legend_size_hlayout.addWidget(self.legend_size_label)
        self.legend_size_hlayout.addWidget(self.legend_size_lineedit)

        self.legend_vlayout.addLayout(self.legend_pos_hlayout)
        self.legend_vlayout.addLayout(self.legend_size_hlayout)

        self.grid_label = QLabel('Grid')
        self.grid_label.setObjectName('grid_label')

        self.grid_vlayout = QVBoxLayout()

        self.grid_status_cb = QCheckBox('On')
        self.grid_status_cb.setObjectName('grid_status_cb')

        self.grid_xdensity_hbox = QHBoxLayout()

        self.grid_xdensity_label = QLabel('x-density')
        self.grid_xdensity_label.setObjectName('x_density_label')

        self.grid_xdensity_lineedit = QLineEdit()
        self.grid_xdensity_lineedit.setObjectName('self.grid_xdensity_lineedit')

        self.grid_xdensity_hbox.addWidget(self.grid_xdensity_label)
        self.grid_xdensity_hbox.addWidget(self.grid_xdensity_lineedit)

        self.grid_ydensity_hbox = QHBoxLayout()

        self.grid_ydensity_label = QLabel('y-density')
        self.grid_ydensity_label.setObjectName('y_density_label')

        self.grid_ydensity_lineedit = QLineEdit()
        self.grid_ydensity_lineedit.setObjectName('self.grid_ydensity_lineedit')

        self.grid_ydensity_hbox.addWidget(self.grid_ydensity_label)
        self.grid_ydensity_hbox.addWidget(self.grid_ydensity_lineedit)

        self.grid_vlayout.addWidget(self.grid_status_cb)
        self.grid_vlayout.addLayout(self.grid_xdensity_hbox)
        self.grid_vlayout.addLayout(self.grid_ydensity_hbox)

        self.title_label = QLabel('Title')
        self.title_label.setObjectName('title_label')

        self.title_vlayout = QVBoxLayout()

        self.title_header_hlayout = QHBoxLayout()

        self.title_header_label = QLabel('Header')
        self.title_header_label.setObjectName('title_header_label')

        self.title_header_lineedit = QLineEdit()
        self.title_header_lineedit.setObjectName('title_header_lineedit')

        self.title_header_hlayout.addWidget(self.title_header_label)
        self.title_header_hlayout.addWidget(self.title_header_lineedit)

        self.title_xaxis_hlayout = QHBoxLayout()

        self.title_xaxis_label = QLabel('x-axis')
        self.title_xaxis_label.setObjectName('title_xaxis_label')

        self.title_xaxis_lineedit = QLineEdit()
        self.title_xaxis_lineedit.setObjectName('title_xaxis_lineedit')

        self.title_xaxis_hlayout.addWidget(self.title_xaxis_label)
        self.title_xaxis_hlayout.addWidget(self.title_xaxis_lineedit)

        self.title_yaxis_hlayout = QHBoxLayout()

        self.title_yaxis_label = QLabel('title_yaxis')
        self.title_yaxis_label.setObjectName('title_yaxis_label')

        self.title_yaxis_lineedit = QLineEdit()
        self.title_yaxis_lineedit.setObjectName('title_header_lineedit')

        self.title_yaxis_hlayout.addWidget(self.title_yaxis_label)
        self.title_yaxis_hlayout.addWidget(self.title_yaxis_lineedit)

        self.title_vlayout.addLayout(self.title_header_hlayout)
        self.title_vlayout.addLayout(self.title_xaxis_hlayout)
        self.title_vlayout.addLayout(self.title_yaxis_hlayout)

        self.normaliztion_label = QLabel('Normalization')
        self.normaliztion_label.setObjectName('normalization_label')

        self.normaliztion_vlayout = QVBoxLayout()

        self.normalization_xaxis_hlayout = QHBoxLayout()

        self.normalization_xaxis_label = QLabel('x-axis')
        self.normalization_xaxis_label.setObjectName('normalization_xaxis_label')

        self.normalization_xaxis_lineedit = QLineEdit()
        self.normalization_xaxis_lineedit.setObjectName("normalization_xaxis_lineedit")

        self.normalization_xaxis_hlayout.addWidget(self.normalization_xaxis_label)
        self.normalization_xaxis_hlayout.addWidget(self.normalization_xaxis_lineedit)


        self.normalization_yaxis_hlayout = QHBoxLayout()

        self.normalization_yaxis_label = QLabel('y-axis')
        self.normalization_yaxis_label.setObjectName('normalization_yaxis_label')

        self.normalization_yaxis_lineedit = QLineEdit()
        self.normalization_yaxis_lineedit.setObjectName("normalization_yaxis_lineedit")

        self.normalization_yaxis_hlayout.addWidget(self.normalization_yaxis_label)
        self.normalization_yaxis_hlayout.addWidget(self.normalization_yaxis_lineedit)

        self.normaliztion_vlayout.addLayout(self.normalization_xaxis_hlayout)
        self.normaliztion_vlayout.addLayout(self.normalization_yaxis_hlayout)



        self.addLayout(self.type_hlayout)
        self.addSpacing(100)
        self.addLayout(self.themes_hlayout)
        self.addSpacing(100)
        self.addWidget(self.legend_label)
        self.addSpacing(5)
        self.addLayout(self.legend_vlayout)
        self.addSpacing(100)
        self.addWidget(self.grid_label)
        self.addSpacing(5)
        self.addLayout(self.grid_vlayout)
        self.addSpacing(100)
        self.addWidget(self.title_label)
        self.addSpacing(5)
        self.addLayout(self.title_vlayout)
        self.addSpacing(100)
        self.addWidget(self.normaliztion_label)
        self.addSpacing(5)
        self.addLayout(self.normaliztion_vlayout)
        self.setAlignment(Qt.AlignTop)












