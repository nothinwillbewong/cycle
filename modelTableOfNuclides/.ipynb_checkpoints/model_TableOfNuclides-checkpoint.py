# Qt________________________________________
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
###########################################
# ui-components files:

#from GUIcomp import *

class model_TableOfNuclides(QObject):

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

        self.setObjectName("TableOfNuclidesLeftWidg")
        self.setWindowTitle("Table of Nuclides")

        # Сделаем размеры адаптивными
        self.setMinimumSize(600, 600)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Основной Layout для таблицы Менделеева
        self.layout = QGridLayout(self)
        self.layout.setObjectName("TableOfIsotopesLayout")
        self.layout.setSpacing(0)  # Плотная компоновка
        self.layout.setContentsMargins(0, 0, 0, 0)  # Убираем внешние зазоры

        # Категории элементов
       

        # Coords and Decays of all Isotopes
        self.TableOfIsotopes = []

        with open('modelTableOfNuclides/data.csv', 'r') as csvfile:
             # Create a reader object
            csv_reader = csv.reader(csvfile)
  
            # Iterate through the rows in the CSV file
            for row in csv_reader:
                self.TableOfIsotopes.append(row)
        


        self.isotope_buttons = {}
        for symbol, Z, N in self.TableOfIsotopes:
            btn = QPushButton(symbol)
            btn.setCheckable(True)
            btn.setObjectName(self.element_category[symbol])
            btn.clicked.connect(lambda _, s=symbol: self.element_btn_click(s))
            self.layout.addWidget(btn, Z, N)
            self.element_buttons[symbol] = btn

        self.update_button_sizes()

    def element_btn_click(self, symbol):
        for btn in self.element_buttons.values():
            btn.setChecked(False)
        self.element_buttons[symbol].setChecked(True)

    def resizeEvent(self, event):
        self.update_button_sizes()

    def update_button_sizes(self):
        size = min(self.width() // 18, self.height() // 9)
        for btn in self.element_buttons.values():
            btn.setMinimumSize(size, size)
            btn.setMaximumSize(size, size)

    def arrow_drawer(self):
        pass

    def nulides_diapason(self):
        pass


#Class that contains decay modes setting to draw arrows, Burnup Matrix builder, s,r - process mode setting, const-dynamic flux setting, time setting
class Right(QVBoxLayout):

    def __init__(self, parent=None):
        super().__init__()

        self.setAlignment(Qt.AlignTop)
        self.setContentsMargins(20, 10, 20, 20)
        self.setSpacing(10)

        # Основной контейнер для информации
        self.browse_container = QWidget()
        self.browse_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Текст с описанием
        self.browse_text = QLabel("<p style='text-align: center; color: red;'><b>Browse fits format file</b></p>")
        self.browse_text.setAlignment(Qt.AlignCenter)
        self.browse_text.setObjectName("usage_right_text")

        # Кнопка Browse
        self.accept_button = QPushButton("Browse")
        self.accept_button.setObjectName("right_btn_accept")

        # Политика размеров - адаптивная
        self.accept_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Layout для контейнера
        self.container_layout = QVBoxLayout(self.browse_container)
        self.container_layout.setContentsMargins(10, 10, 10, 10)
        self.container_layout.setSpacing(10)
        self.container_layout.setAlignment(Qt.AlignTop)

        # Добавляем текст и кнопку
        self.container_layout.addWidget(self.browse_text, alignment=Qt.AlignHCenter)
        self.container_layout.addWidget(self.accept_button, alignment=Qt.AlignHCenter)

        # Добавляем контейнер в главный Right Layout
        self.addWidget(self.browse_container, alignment=Qt.AlignCenter)

        # Подстраховка - сразу обновить размеры
        self.update_sizes()

    def update_sizes(self):
        """Перерасчет размеров с учетом DPI"""
        if QApplication.primaryScreen():
            dpi = QApplication.primaryScreen().logicalDotsPerInch()
        else:
            dpi = 96  # дефолтное

        scale = dpi / 96.0  # базовое DPI = 96

        # Получаем размеры окна (родителя)
        if self.parentWidget():
            window_width = self.parentWidget().width()
            window_height = self.parentWidget().height()
        else:
            window_width, window_height = (800, 600)

        # Размер текста — пропорционально высоте
        font_size = max(12, int(window_height * 0.03 * scale))
        self.browse_text.setStyleSheet(f"font-size: {font_size}px;")

        # Размер кнопки — пропорционально ширине/высоте
        button_width = int(window_width * 0.5 * scale)
        button_height = int(window_height * 0.2 * scale)

        self.accept_button.setMinimumSize(button_width // 2, button_height // 2)
        self.accept_button.setMaximumSize(button_width, button_height)

    def resizeEvent(self, event):
        self.update_sizes()
        super().resizeEvent(event)

    def burnup_matrix_builder(self):
        pass

    def capture_mode(self):
        pass

    def flux_mode(self):
        pass

    def static_flux(self):
        pass

    def dynamic_flux(self):
        pass

    def time_setting(self):
        pass

    def energy_setting(self):
        pass
