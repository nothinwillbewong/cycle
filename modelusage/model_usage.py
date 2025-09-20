#Qt________________________________________
from PyQt5 import QtGui, QtCore, QtWidgets#
from PyQt5.QtWidgets import* ##############
from PyQt5.QtCore import* #################
from PyQt5.QtGui import* ##################

#OTHERS____________________________________
from pathlib import Path ##################
from PIL import Image #####################
from enum import Enum #####################
import qrc_resources ######################
from math import* #########################
import numpy as np#########################
import sys#################################
import os #################################
###########################################
#ui-components files:



class model_usage(QObject):

#Initializer:
	def __init__(self):
		super().__init__()
        
		#ui_components:
		self.__left = Left()
		self.__right= Right()

#Get instances Right & Left:
	def getLeftWidget(self):
		return self.__left
		
	def getRightLayout(self):
		return self.__right
	#........................
    



#Document presenter.....................................................................
class Left(QWidget):

#Initializer:
    def __init__(self):
        super().__init__()
        
    #main widget of presenter:
        widget = QGroupBox() ###############
        widget.setObjectName('gbox_usage_left') #
        ####################################

    #main layout of main widget of presenter:
        layout = QHBoxLayout() #############
        layout.addWidget(widget) ###########
        self.setLayout(layout) #############
        self.setContentsMargins(0, 0, 0, 0)
    #End of initializer....................




#to hide from user:
    def hide(self):
        self.setVisible(False)

#to show for user:
    def show(self):
        self.setVisible(True)
#End of Left presenter..................................................................



class Right(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignTop)
        self.setContentsMargins(20, 60, 20, 20)
        self.setSpacing(10)

        # Описание программы
        self.message_label = QLabel()
        self.message_label.setText(
            """
            <p style="text-align: center;"><b>Welcome to FAI-tools!</b></p>
            <p style="text-align: justify;">This software was developed at the</p>
            <p style="text-align: justify;"><b>FESENKOV ASTROPHYSICAL INSTITUTE</b></p>
            <p style="text-align: justify;">
                as part of the project funded by the Science Committee of the Ministry
                of Science and Higher Education of the Republic of Kazakhstan
                (Grant No. AP14869876).
            </p>
            <p style="text-align: justify;">Please review the</p>
            <p style="text-align: justify;">
                <a href='https://fai.kz/ru/about' style="color: #6988E7; text-decoration: none;"
                   onmouseover="this.style.color='#6988E7';"
                   onmouseout="this.style.color='#6988E7';">
                   https://fai.kz
                </a>.
            </p>
            """
        )

        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setWordWrap(True)
        self.message_label.setOpenExternalLinks(True)
        self.message_label.setObjectName("usage_right_label")

        # Делаем текст адаптивным
        self.message_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.message_label.setMinimumHeight(150)

        # Чекбокс соглашения
        self.agreement_checkbox = QCheckBox("I accept the agreement.")
        self.agreement_checkbox.setObjectName("usage_right_checkbox")

        # Кнопка продолжения
        self.accept_button = QPushButton("Continue")
        self.accept_button.setObjectName("right_btn_accept")
        self.accept_button.setEnabled(False)

        # Делаем кнопку адаптивной
        self.accept_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.accept_button.setMinimumHeight(50)

        # Связываем чекбокс с кнопкой
        self.agreement_checkbox.stateChanged.connect(
            lambda state: self.accept_button.setEnabled(state == Qt.Checked)
        )

        # Добавляем элементы в макет
        self.addWidget(self.message_label, alignment=Qt.AlignCenter)
        self.addWidget(self.agreement_checkbox, alignment=Qt.AlignBottom)
        self.addWidget(self.accept_button, alignment=Qt.AlignBottom)

    def resizeEvent(self, event):
        """Обновляет размеры шрифта и элементов при изменении окна"""
        parent = self.parentWidget()
        if parent:
            width = parent.width()
            height = parent.height()

            # Динамический размер шрифта
            font_size = max(12, int(height * 0.03))  # Шрифт - 3% от высоты окна
            self.message_label.setStyleSheet(f"font-size: {font_size}px;")

            # Адаптивный размер кнопки
            btn_width = int(width * 0.3)  # 30% от ширины окна
            btn_height = max(50, int(height * 0.08))  # Минимум 50px, но адаптируется

            self.accept_button.setMinimumSize(btn_width, btn_height)
            self.accept_button.setMaximumSize(btn_width * 1.2, btn_height * 1.2)

        super().resizeEvent(event)








    
