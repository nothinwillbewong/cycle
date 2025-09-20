# Qt________________________________________
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

# OTHERS____________________________________
from pathlib import Path
from PIL import Image
from enum import Enum
import qrc_resources
from math import *
import numpy as np
import sys
import os
import endf
import endfreader
###########################################
# ui-components files:

from GUIcomp import *

class model_CoreNucleo(QObject):

    def __init__(self, parent = None):
        super().__init__()


        self.__left = Left(self)
        self.__right = Right()


    def getLeftWidget(self):
        return self.__left
    def getRightLayout(self):
        return self.__right

class Left(QWidget):



    def __init__(self, core_model):
        super().__init__()
        self.core_model = core_model
        self.setMinimumSize(100, 100)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.layout = QGridLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.element_buttons = {}

        for symbol, row, col, Z, category in self.get_periodic_table():
            btn = QPushButton(symbol)
            btn.setObjectName(category)
            btn.clicked.connect(lambda _, s=symbol, z=Z: self.fetch_isotope_list(s, z))
            self.layout.addWidget(btn, row, col)
            self.element_buttons[symbol] = btn

        self.update_button_sizes()

    def get_periodic_table(self):
        return [
        ("H", 0, 0, 1, "nonmetal"), ("He", 0, 17, 2, "noble_gas"),
        ("Li", 1, 0, 3, "alkali_metal"), ("Be", 1, 1, 4, "alkaline_earth_metal"),
        ("B", 1, 12, 5, "metalloid"), ("C", 1, 13, 6, "nonmetal"),
        ("N", 1, 14, 7, "nonmetal"), ("O", 1, 15, 8, "nonmetal"),
        ("F", 1, 16, 9, "halogen"), ("Ne", 1, 17, 10, "noble_gas"),
        ("Na", 2, 0, 11, "alkali_metal"), ("Mg", 2, 1, 12, "alkaline_earth_metal"),
        ("Al", 2, 12, 13, "post_transition_metal"), ("Si", 2, 13, 14, "metalloid"),
        ("P", 2, 14, 15, "nonmetal"), ("S", 2, 15, 16, "nonmetal"),
        ("Cl", 2, 16, 17, "halogen"), ("Ar", 2, 17, 18, "noble_gas"),
        ("K", 3, 0, 19, "alkali_metal"), ("Ca", 3, 1, 20, "alkaline_earth_metal"),
        ("Sc", 3, 2, 21, "transition_metal"), ("Ti", 3, 3, 22, "transition_metal"),
        ("V", 3, 4, 23, "transition_metal"), ("Cr", 3, 5, 24, "transition_metal"),
        ("Mn", 3, 6, 25, "transition_metal"), ("Fe", 3, 7, 26, "transition_metal"),
        ("Co", 3, 8, 27, "transition_metal"), ("Ni", 3, 9, 28, "transition_metal"),
        ("Cu", 3, 10, 29, "transition_metal"), ("Zn", 3, 11, 30, "transition_metal"),
        ("Ga", 3, 12, 31, "post_transition_metal"), ("Ge", 3, 13, 32, "metalloid"),
        ("As", 3, 14, 33, "metalloid"), ("Se", 3, 15, 34, "nonmetal"),
        ("Br", 3, 16, 35, "halogen"), ("Kr", 3, 17, 36, "noble_gas"),
        ("Rb", 4, 0, 37, "alkali_metal"), ("Sr", 4, 1, 38, "alkaline_earth_metal"),
        ("Y", 4, 2, 39, "transition_metal"), ("Zr", 4, 3, 40, "transition_metal"),
        ("Nb", 4, 4, 41, "transition_metal"), ("Mo", 4, 5, 42, "transition_metal"),
        ("Tc", 4, 6, 43, "transition_metal"), ("Ru", 4, 7, 44, "transition_metal"),
        ("Rh", 4, 8, 45, "transition_metal"), ("Pd", 4, 9, 46, "transition_metal"),
        ("Ag", 4, 10, 47, "transition_metal"), ("Cd", 4, 11, 48, "transition_metal"),
        ("In", 4, 12, 49, "post_transition_metal"), ("Sn", 4, 13, 50, "post_transition_metal"),
        ("Sb", 4, 14, 51, "metalloid"), ("Te", 4, 15, 52, "metalloid"),
        ("I", 4, 16, 53, "halogen"), ("Xe", 4, 17, 54, "noble_gas"),
        ("Cs", 5, 0, 55, "alkali_metal"), ("Ba", 5, 1, 56, "alkaline_earth_metal"),
        ("La", 7, 3, 57, "lanthanide"),
        ("Hf", 5, 3, 72, "transition_metal"), ("Ta", 5, 4, 73, "transition_metal"),
        ("W", 5, 5, 74, "transition_metal"), ("Re", 5, 6, 75, "transition_metal"),
        ("Os", 5, 7, 76, "transition_metal"), ("Ir", 5, 8, 77, "transition_metal"),
        ("Pt", 5, 9, 78, "transition_metal"), ("Au", 5, 10, 79, "transition_metal"),
        ("Hg", 5, 11, 80, "transition_metal"), ("Tl", 5, 12, 81, "post_transition_metal"),
        ("Pb", 5, 13, 82, "post_transition_metal"), ("Bi", 5, 14, 83, "post_transition_metal"),
        ("Po", 5, 15, 84, "metalloid"), ("At", 5, 16, 85, "halogen"), ("Rn", 5, 17, 86, "noble_gas"),
        ("Fr", 6, 0, 87, "alkali_metal"), ("Ra", 6, 1, 88, "alkaline_earth_metal"),
        ("Ac", 8, 3, 89, "actinide"),
        ("Rf", 6, 3, 104, "transition_metal"), ("Db", 6, 4, 105, "transition_metal"),
        ("Sg", 6, 5, 106, "transition_metal"), ("Bh", 6, 6, 107, "transition_metal"),
        ("Hs", 6, 7, 108, "transition_metal"), ("Mt", 6, 8, 109, "transition_metal"),
        ("Ds", 6, 9, 110, "transition_metal"), ("Rg", 6, 10, 111, "transition_metal"),
        ("Cn", 6, 11, 112, "transition_metal"), ("Nh", 6, 12, 113, "post_transition_metal"),
        ("Fl", 6, 13, 114, "post_transition_metal"), ("Mc", 6, 14, 115, "post_transition_metal"),
        ("Lv", 6, 15, 116, "post_transition_metal"), ("Ts", 6, 16, 117, "halogen"), ("Og", 6, 17, 118, "noble_gas"),
        ("Ce", 7, 4, 58, "lanthanide"), ("Pr", 7, 5, 59, "lanthanide"),
        ("Nd", 7, 6, 60, "lanthanide"), ("Pm", 7, 7, 61, "lanthanide"),
        ("Sm", 7, 8, 62, "lanthanide"), ("Eu", 7, 9, 63, "lanthanide"),
        ("Gd", 7, 10, 64, "lanthanide"), ("Tb", 7, 11, 65, "lanthanide"),
        ("Dy", 7, 12, 66, "lanthanide"), ("Ho", 7, 13, 67, "lanthanide"),
        ("Er", 7, 14, 68, "lanthanide"), ("Tm", 7, 15, 69, "lanthanide"),
        ("Yb", 7, 16, 70, "lanthanide"), ("Lu", 7, 17, 71, "lanthanide"),
        ("Th", 8, 4, 90, "actinide"), ("Pa", 8, 5, 91, "actinide"),
        ("U", 8, 6, 92, "actinide"), ("Np", 8, 7, 93, "actinide"),
        ("Pu", 8, 8, 94, "actinide"),("Am", 8, 9, 95, "actinide"),
        ("Cm", 8, 10, 96, "actinide"),
        ("Bk", 8, 11, 97, "actinide"),
        ("Cf", 8, 12, 98, "actinide"),
        ("Es", 8, 13, 99, "actinide"),
        ("Fm", 8, 14, 100, "actinide"),
        ("Md", 8, 15, 101, "actinide"),
        ("No", 8, 16, 102, "actinide"),
        ("Lr", 8, 17, 103, "actinide"),
    ]


    def fetch_isotope_list(self, symbol, Z):
        try:
            decay_folder = os.path.abspath("ENDF-B-VIII.1/decay-version.VIII.1")
            isotopes = endfreader.endfReader.read_isotopes_from_decay_folder(decay_folder)
            self.core_model.getRightLayout().show_isotope_list(symbol, Z, isotopes)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Couldn't read isotopes: {e}")

    def resizeEvent(self, event):
        self.update_button_sizes()

    def update_button_sizes(self):
        size = min(self.width() // 18, self.height() // 9)
        for btn in self.element_buttons.values():
            btn.setMinimumSize(size, size)
            btn.setMaximumSize(size, size)

    def wheelEvent(self, event):
        zoom_factor = 1.0 # Simple way to control the total amount zoomed  in or out  
        scale_factor = 1.10 # How much to scale into or out of the chart  
        if event.angleDelta().y() >= 120 and zoom_factor < 3.0:  
            zoom_factor *= 1.25  
            self.chart.zoom(scale_factor)  
        elif event.angleDelta().y() <= -120 and zoom_factor > 0.5:  
            zoom_factor *= 0.8  
            self.chart.zoom(1 / scale_factor)


class Right(QVBoxLayout):

    def __init__(self, parent=None):
        super().__init__()

        select_cb = QComboBox()
        select_cb.setFixedSize(100,25)
        select_cb.setObjectName('select_cb')
        
        inf_label = QLabel('Information about isotope')
        inf_label.setFixedSize(150,20)
        inf_label.setObjectName('inf_label')
    

        inf_text = QLineEdit()
        inf_text.setFixedSize(500,700)
        inf_text.setObjectName('inf_text')


        self.addWidget(select_cb)
        self.addSpacing(40)
        self.addWidget(inf_label)
        self.addSpacing(10)
        self.addWidget(inf_text)
        self.setAlignment(Qt.AlignTop)



        



    #     # self.setAlignment(Qt.AlignTop)
    #     # self.setContentsMargins(20, 10, 20, 20)
    #     # self.setSpacing(10)

    #     # # Основной контейнер для информации
    #     # self.browse_container = QWidget()
    #     # self.browse_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    #     # # Текст с описанием
    #     # self.browse_text = QLabel("<p style='text-align: center; color: red;'><b>Browse fits format file</b></p>")
    #     # self.browse_text.setAlignment(Qt.AlignCenter)
    #     # self.browse_text.setObjectName("usage_right_text")

    #     # # Кнопка Browse
    #     # self.accept_button = QPushButton("Browse")
    #     # self.accept_button.setObjectName("right_btn_accept")

    #     # # Политика размеров - адаптивная
    #     # self.accept_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    #     # # Layout для контейнера
    #     # self.container_layout = QVBoxLayout(self.browse_container)
    #     # self.container_layout.setContentsMargins(10, 10, 10, 10)
    #     # self.container_layout.setSpacing(10)
    #     # self.container_layout.setAlignment(Qt.AlignTop)

    #     # # Добавляем текст и кнопку
    #     # self.container_layout.addWidget(self.browse_text, alignment=Qt.AlignHCenter)
    #     # self.container_layout.addWidget(self.accept_button, alignment=Qt.AlignHCenter)

    #     # # Добавляем контейнер в главный Right Layout
    #     # self.addWidget(self.browse_container, alignment=Qt.AlignCenter)

    #     # Подстраховка - сразу обновить размеры
    #     super().__init__()
        
    #     self.label = QLabel("<b>Select an element from the periodic table</b>")
    #     self.label.setAlignment(Qt.AlignCenter)
    #     self.label.setWordWrap(True)
    #     self.label.setStyleSheet("font-size: 18px; font-weight: bold; color: white; background-color")
    #     self.addWidget(self.label)

    #     self.scroll_area = QScrollArea()
    #     self.scroll_area.setWidgetResizable(True)
    #     self.scroll_area.setMaximumHeight(100)
    #     self.scroll_area.setMinimumWidth(100)
    #     self.scroll_area.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #     self.addWidget(self.scroll_area)

    #     self.isotope_buttons_container = QWidget()
    #     self.isotope_buttons_layout = QVBoxLayout(self.isotope_buttons_container)
    #     self.isotope_buttons_layout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    #     self.scroll_area.setWidget(self.isotope_buttons_container)
    #     # self.update_sizes()


    # # def select_isotope_box(self):
    # #     self.select_box = QComboBox('Select isotope')
    # #     self.element_isotopes = el_isotopes(symbol)
    # #     for key in self.element_isotopes:
    # #         self.select_box.addItems(key)
    # #     self.combo.currentIndexChanged.connect(self.get_isotope_data)
        

    # # def fetch_isotope_list(self, symbol, Z):
    # #     decay_folder = os.path.abspath("decay")
    # #     isotopes = endfreader.read_isotopes_from_decay_folder(decay_folder, Z_filter=Z)
    # #     self.core_model.getRightLayout().show_isotope_list(symbol, Z, isotopes)


    # def show_isotope_list(self, symbol, Z, isotopes):
    #     # Очистка старых виджетов
    #     for i in reversed(range(self.isotope_buttons_layout.count())):
    #         widget = self.isotope_buttons_layout.itemAt(i).widget()
    #         if widget:
    #             widget.deleteLater()

    #     # self.label.setText(f"<b>Select an isotope of {symbol}</b>")
    #     # self.label.setAlignment(Qt.AlignTop)

    #     # Создаем выпадающий список
    #     self.combo = QComboBox()   
    #     # self.combo.setGeometry(10,0,100,100) 
    #     self.combo.setStyleSheet("font-size: 20px; padding: 1px, 18px,1px, 3px; background-color: white;")
    #     self.combo.addItem("Select an isotope...")

    #     # Сохраняем соответствие index -> (Z, A, m, filename)
    #     self.combo_data = {}

    #     for i, (iso, filename) in enumerate(isotopes, start=1):
    #         A, m = iso.A, iso.m
    #         label = f"{symbol}-{A}{m if m else ''}"
    #         self.combo.addItem(label)
    #         self.combo_data[i] = (symbol, Z, A, m, filename)

    #     self.combo.currentIndexChanged.connect(self.isotope_selected)
    #     self.isotope_buttons_layout.addWidget(self.combo)

    # def isotope_selected(self, index):
    #     if index == 0:
    #         return  # первая строка — заглушка

    #     symbol, Z, A, m, filename = self.combo_data[index]
    #     self.fetch_isotope_info(symbol, Z, A, m, filename)



    # def create_isotope_callback(self, symbol, Z, A, m, filename):
    #     return lambda: self.fetch_isotope_info(symbol, Z, A, m, filename)

    # def fetch_isotope_info(self, symbol, Z, A, m, filename):
    #     try:
    #         decay_folder = os.path.abspath("ENDF-B-VIII.1/decay-version.VIII.1")
    #         filepath = os.path.join(decay_folder, filename)
    #         mat = endf.Material(filepath)
    #         if (8, 457) in mat.section_data:
    #             decay_data = mat.section_data[(8, 457)]
    #             data = self.analyze_decay_data(decay_data, filename, endfreader.Isotope(symbol, Z, A, m))
    #             self.update_info(symbol, data)
    #         else:
    #             QMessageBox.warning(None, "No Section", "Section (8, 457) not found in file.")
    #     except Exception as e:
    #         QMessageBox.critical(None, "Error", f"Couldn't get isotope data: {e}")

    # def analyze_decay_data(self, decay_data, filename, isotope):
    #     result = {
    #         "A": isotope.A,
    #         "m": isotope.m,
    #         "stable": "modes" not in decay_data or all(mode.get("RTYP") == 0.0 for mode in decay_data.get("modes", [])),
    #         "decay_modes": []
    #     }
    #     if not result["stable"]:
    #         for mode in decay_data.get("modes", []):
    #             rtyp = mode.get("RTYP")
    #             decay_type = {
    #                 0.0: "Gamma radiation",
    #                 1.0: "Beta-minus decay (β⁻)",
    #                 2.0: "Electron capture or Positron decay (β⁺, e.c.)",
    #                 3.0: "Isomeric transition (IT)",
    #                 4.0: "Alpha decay (α)",
    #                 5.0: "Neutron emission",
    #                 6.0: "Spontaneous fission (SF)",
    #                 7.0: "Proton emission",
    #                 10.0: "Unknown decay type"
    #             }.get(rtyp, f"Unknown decay (RTYP={rtyp})")
    #             result["decay_modes"].append({
    #                 "type": decay_type,
    #                 "Q": mode.get("Q", [0.0])[0],
    #                 "half_life": decay_data.get("T1/2", ["Unknown"])[0]
    #             })
    #     return result

    # def update_info(self, symbol, data):
    #     info = f"<h2 style='font-size: 26px; font-weight: bold; color: white;'>{symbol}-{data['A']}{'m' if data['m'] else ''}</h2>"
    #     info += f"<p style='font-size: 20px; color: white;'><b>Stable:</b> {'Yes' if data.get('stable') else 'No'}</p>"
    #     if not data.get("stable"):
    #         info += "<p style='font-size: 20px; white: orange;'><b>Decay Modes:</b></p><ul>"
    #         for mode in data.get("decay_modes", []):
    #             info += f"<li style='font-size: 18px; color: white;'><b>Type:</b> {mode['type']}, <b>Energy:</b> {mode['Q']} keV, <b>Half-life:</b> {mode['half_life']} sec</li>"
    #         info += "</ul>"
    #     self.label.setText(info)
    #     self.label.setWordWrap(True)

        

        




    # def update_sizes(self):
    #     """Перерасчет размеров с учетом DPI"""
    #     if QApplication.primaryScreen():
    #         dpi = QApplication.primaryScreen().logicalDotsPerInch()
    #     else:
    #         dpi = 96  # дефолтное

    #     scale = dpi / 96.0  # базовое DPI = 96

    #     # Получаем размеры окна (родителя)
    #     if self.parentWidget():
    #         window_width = self.parentWidget().width()
    #         window_height = self.parentWidget().height()
    #     else:
    #         window_width, window_height = (800, 600)

    #     # Размер текста — пропорционально высоте
    #     font_size = max(12, int(window_height * 0.03 * scale))
    #     self.browse_text.setStyleSheet(f"font-size: {font_size}px;")

    #     # Размер кнопки — пропорционально ширине/высоте
    #     button_width = int(window_width * 0.5 * scale)
    #     button_height = int(window_height * 0.2 * scale)

    #     self.accept_button.setMinimumSize(button_width // 2, button_height // 2)
    #     self.accept_button.setMaximumSize(button_width, button_height)

    # def resizeEvent(self, event):
    #     self.update_sizes()
    #     super().resizeEvent(event)

    




