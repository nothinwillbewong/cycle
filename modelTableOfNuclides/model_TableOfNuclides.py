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

import endfreader as er
###########################################
# ui-components files:

from GUIcomp import *

# сделать размеры адаптивными



class model_TableOfNuclides(QObject):

    # Initializer:
    def __init__(self):
        super().__init__()

        # Создаем правую панель
        self.__right = Right()
        self.__left = Left()
        self.__left.set_reaction_panel(self.__right)
        self.__right.set_left_widget(self.__left)

    # Get instances Right & Left:
    def getLeftWidget(self):
        return self.__left

    def getRightLayout(self):
        return self.__right
    


class Left(QGraphicsView):
    factor = 3

    def __init__(self):
        super().__init__()
        self.setObjectName("foo")
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setMinimumSize(10, 10)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout_widget = QWidget()
        #self.layout_widget.setStyleSheet('background-color: #2c2f33;')
        self.layout_widget.setObjectName("fooo")
        self.layout = QGridLayout(self.layout_widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self._zoom = 0
        self._zoom_step = 1.25
        self.element_buttons = {}

        table = er.Decay()
        self.data = table.get_isotopes()

        self.element_buttons = {}
        self.button_positions = {}

        font = QFont('Arial', 3)

        self.reaction_colors = {
            'beta+': Qt.blue,
            'beta-': Qt.red,
            'alpha': Qt.darkGreen,
            'ec': Qt.cyan,
            'p': Qt.darkYellow,
            'beta+, n': Qt.magenta,
            'beta+, alpha': Qt.darkRed,
            'beta-, alpha': Qt.darkCyan,
            'gamma': Qt.gray,
            'neutron capture': Qt.darkBlue
        }
#############################
        i= 112
        sym = 'Nn'
        A1 = 1

        # Add buttons with proper grid positions
        for symbol, Z, A, decaymode in self.data:
            btn = QPushButton(f"{A}"+symbol)
            btn.setObjectName(decaymode)
            btn.setFixedSize(12, 12)
            btn.setFont(font)
            row = Z + i
            col = A - Z  
            
            self.layout.addWidget(btn, row, col)
            self.element_buttons[(Z, A)] = btn
            self.button_positions[(Z, A)] = (row, col)
            if sym !=symbol and A -A1 < 1:
                i = i -2

            sym = symbol
            A1 = A


        proxy = QGraphicsProxyWidget()
        proxy.setWidget(self.layout_widget)

        self.scene.addItem(proxy)


        self.setRenderHints(self.renderHints() | QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        self.update_arrows()

        self.show()
#######################################


######################################
    def wheelEvent(self, event):
        if event.angleDelta().y() > 0:
            zoom_factor = self._zoom_step
            self._zoom += 1
        else:
            zoom_factor = 1 / self._zoom_step
            self._zoom -= 1

        if self._zoom < -10:
            self._zoom = -10
            return
        elif self._zoom > 20:
            self._zoom = 20
            return

        self.scale(zoom_factor, zoom_factor)
#####################################


    def set_reaction_panel(self, reaction_panel):
        self.reaction_panel = reaction_panel


    def element_btn_click(self, symbol):
        for btn in self.element_buttons.values():
            btn.setChecked(False)
        self.element_buttons[symbol].setChecked(True)

    # def resizeEvent(self, event):
    #     self.update_button_sizes()

    # def update_button_sizes(self):
    #     size = min(self.width() // 300, self.height() // 150)
    #     for btn in self.element_buttons.values():
    #         btn.setMinimumSize(size, size)
    #         btn.setMaximumSize(size, size)


    def decay_result(self):
        if self.decaytype == "beta-":
            self.Z = self.Z + 1
        elif self.decaytype == 'beta+':
            self.Z = self.Z - 1
        elif self.decaytype == 'alpha':
            self.Z = self.Z - 2
            self.A = self.A - 4
        elif self.decaytype == 'ec':
            self.Z = self.Z - 1
        elif self.decaytype == 'beta+, n':
            self.Z = self.Z + 1
            self.A = self.A - 1
        elif self.decaytype == 'beta+, alpha':
            self.Z = self.Z - 3
            self.A = self.A - 4
        elif self.decaytype == 'beta-, alpha':
            self.Z = self.Z - 1
            self.A = self.A - 4
        elif self.decaytype == 'p':
            self.Z = self.Z - 1
            self.A = self.A - 1

    def update_arrows(self):
        # Удалим старые стрелки (все линии и стрелочные наконечники)
        for item in self.scene.items():
            if isinstance(item, (QGraphicsLineItem, QGraphicsPolygonItem, QGraphicsTextItem)):
                self.scene.removeItem(item)

        # Добавим заново только разрешённые стрелки
        if hasattr(self, "reaction_panel"):
            allowed = self.reaction_panel.get_enabled_reactions()
        else:
            allowed = list(self.reaction_colors.keys())

        for symbol, Z, A, decaymode in self.data:
            if decaymode not in allowed:
                continue

            start = (Z, A)
            self.Z, self.A = Z, A
            self.decaytype = decaymode
            self.decay_result()
            end = (self.Z, self.A)

            if start in self.button_positions and end in self.button_positions:
                self.draw_arrow(start, end, decaymode)


    
    def draw_arrow(self, start, end, decaymode):

        if start not in self.button_positions or end not in self.button_positions:
            return

        row1, col1 = self.button_positions[start]
        row2, col2 = self.button_positions[end]

        x1 = col1 * 12 + 6
        y1 = row1 * 12 + 6
        x2 = col2 * 12 + 6
        y2 = row2 * 12 + 6

        line = QGraphicsLineItem(x1, y1, x2, y2)
        line.setPen(QPen(self.reaction_colors[decaymode], 1))
        self.scene.addItem(line)

    def arrow_drawer(self):
        pass

    def nulides_diapason(self):
        pass


#Class that contains decay modes setting to draw arrows, Burnup Matrix builder, s,r - process mode setting, const-dynamic flux setting, time setting
class Right(QVBoxLayout):

    def __init__(self, parent=None):
        super().__init__(parent)


###########
        self.set_label = QLabel('Set Diapason')
        self.set_label.setObjectName('set_label')
        self.set_label.setFixedSize(100,25)



        self.from_box = QComboBox()
        self.from_box.setObjectName('from_box')
        self.from_box.setFixedSize(100,25)

        self.to_box = QComboBox()
        self.to_box.setObjectName('to_box')
        self.to_box.setFixedSize(100,25)
########################

        self.reac_label = QLabel('Reaction Types')
        self.reac_label.setObjectName('react_types')
        self.reac_label.setFixedSize(150,25)

        self.types_cb_widget = QWidget()
        self.types_cb_widget.setObjectName('types_widget')
        self.types_cb_widget.setFixedSize(300,250)

        self.neutron_capture_cb = QCheckBox('neutron capture')
        self.neutron_capture_cb.setObjectName('neutron_cb')
        self.neutron_capture_cb.stateChanged.connect(self.on_checkbox_changed)

        self.beta_plus_cb = QCheckBox('beta+')
        self.beta_plus_cb.setObjectName('betaplus_cb')
        self.beta_plus_cb.stateChanged.connect(self.on_checkbox_changed)

        self.beta_minus_cb = QCheckBox('beta-')
        self.beta_minus_cb.setObjectName('betaminus_cb')
        self.beta_minus_cb.stateChanged.connect(self.on_checkbox_changed)

        self.alpha_cb = QCheckBox('alpha')
        self.alpha_cb.setObjectName('alpha_cb')
        self.alpha_cb.stateChanged.connect(self.on_checkbox_changed)

        self.gamma_cb = QCheckBox('gamma')
        self.gamma_cb.setObjectName('gamma_cb')
        self.gamma_cb.stateChanged.connect(self.on_checkbox_changed)

        self.p_cb = QCheckBox('p')
        self.p_cb.setObjectName('p_cb')
        self.p_cb.stateChanged.connect(self.on_checkbox_changed)

        self.beta_minus_alpha_cb = QCheckBox('beta-, alpha')
        self.beta_minus_alpha_cb.setObjectName('betaminus_alpha_cb')
        self.beta_minus_alpha_cb.stateChanged.connect(self.on_checkbox_changed)

        self.beta_plus_alpha_cb = QCheckBox('beta+, alpha')
        self.beta_plus_alpha_cb.setObjectName('beta_plus_alpha_cb')
        self.beta_plus_alpha_cb.stateChanged.connect(self.on_checkbox_changed)

        self.ec_cb = QCheckBox('EC')
        self.ec_cb.setObjectName('ec_cb')
        self.ec_cb.stateChanged.connect(self.on_checkbox_changed)

        self.types_container = QVBoxLayout(self.types_cb_widget)

        self.types_container.addWidget(self.neutron_capture_cb)
        self.addSpacing(2)
        self.types_container.addWidget(self.beta_plus_cb)
        self.addSpacing(2)
        self.types_container.addWidget(self.beta_minus_cb)
        self.addSpacing(2)
        self.types_container.addWidget(self.alpha_cb)
        self.addSpacing(2)
        self.types_container.addWidget(self.gamma_cb)
        self.addSpacing(2)
        self.types_container.addWidget(self.beta_plus_alpha_cb)
        self.addSpacing(2)
        self.types_container.addWidget(self.beta_minus_alpha_cb)
        self.addSpacing(2)
        self.types_container.addWidget(self.p_cb)
        self.addSpacing(2)
        self.types_container.addWidget(self.ec_cb)
#####################

        self.arrows_cb = QCheckBox('arrows')
        self.arrows_cb.setObjectName('arrows_cb')
######################
        self.flux_state_tab = QTabWidget()
        self.flux_state_tab.setObjectName("flux_state")

        self.flux_static_widget = QWidget()
        self.flux_static_widget.setObjectName('Static')

        self.flux_dynamic_widget = QWidget()
        self.flux_dynamic_widget.setObjectName('Dynamic')

        self.flux_state_tab.addTab(self.flux_static_widget, 'Static')
        self.flux_state_tab.addTab(self.flux_dynamic_widget, 'Dynamic')

        self.static_flux_tab()
        self.dynamic_flux_tab()
#######################

#######################
        self.burnup_pb = QPushButton('Build Burnup Matrix')
        self.burnup_pb.setObjectName('burnup_pb')
        self.burnup_pb.setFixedSize(150,50)
#######################



        self.addWidget(self.set_label)
        self.addSpacing(5)
        self.addWidget(self.from_box)
        self.addSpacing(5)
        self.addWidget(self.to_box)
        self.addSpacing(40)
        self.addWidget(self.reac_label)
        self.addSpacing(5)
        self.addWidget(self.types_cb_widget)
        self.addSpacing(10)
        self.addWidget(self.arrows_cb)
        self.addSpacing(30)
        self.addWidget(self.flux_state_tab)
        self.addSpacing(20)
        self.addWidget(self.burnup_pb, alignment=Qt.AlignCenter)
        self.setAlignment(Qt.AlignTop)

        for cb in [self.beta_plus_cb, self.beta_minus_cb, self.alpha_cb,
           self.neutron_capture_cb, self.gamma_cb]:
            cb.stateChanged.connect(self.on_checkbox_changed)

        



    def static_flux_tab(self):

        self.energy_layout = QHBoxLayout()
        self.flux_layout = QHBoxLayout()
        self.database_layout = QHBoxLayout()

        self.energy_label = QLabel('Energy')
        self.energy_label.setObjectName('energy_label')
        self.flux_label = QLabel('Flux')
        self.flux_label.setObjectName('flux_label')
        self.database_label = QLabel('Database')
        self.database_label.setObjectName('database_label')

        self.energy_box = QComboBox()
        self.energy_box.setObjectName('energy_box')
        self.flux_box = QComboBox()
        self.flux_box.setObjectName('flux_box')
        self.database_box = QComboBox()
        self.database_box.setObjectName('database_box')

        self.energy_layout.addWidget(self.energy_label)
        self.energy_layout.addWidget(self.energy_box)

        self.flux_layout.addWidget(self.flux_label)
        self.flux_layout.addWidget(self.flux_box)

        self.database_layout.addWidget(self.database_label)
        self.database_layout.addWidget(self.database_box)

        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(self.energy_layout)
        self.v_layout.addLayout(self.flux_layout)
        self.v_layout.addLayout(self.database_layout)
        self.flux_static_widget.setLayout(self.v_layout)

    
    def on_checkbox_changed(self):
        if hasattr(self, "left_widget"):
            self.left_widget.update_arrows()

    def get_enabled_reactions(self):
        enabled = []
        if self.beta_plus_cb.isChecked():
            enabled.append("beta+")
        if self.beta_minus_cb.isChecked():
            enabled.append("beta-")
        if self.alpha_cb.isChecked():
            enabled.append("alpha")
        if self.neutron_capture_cb.isChecked():
            enabled.append("neutron capture")
        if self.gamma_cb.isChecked():
            enabled.append("gamma")
        if self.ec_cb.isChecked():
            enabled.append("ec")
        if self.p_cb.isChecked():
            enabled.append("p")
        if self.beta_plus_alpha_cb.isChecked():
            enabled.append("beta+, alpha")
        if self.beta_minus_alpha_cb.isChecked():
            enabled.append("beta-, alpha")

        return enabled
    

    def set_left_widget(self, left_widget):
        self.left_widget = left_widget

    


    
    def dynamic_flux_tab(self):
        pass






    # def burnup_matrix_builder(self):
    #     pass

    # def capture_mode(self):
    #     pass

    # def flux_mode(self):
    #     pass

    # def static_flux(self):
    #     pass

    # def dynamic_flux(self):
    #     pass

    # def time_setting(self):
    #     pass

    # def energy_setting(self):
    #     pass
