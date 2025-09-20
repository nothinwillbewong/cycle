#Qt5 files:
from PyQt5.QtGui import* ###########################
from PyQt5.QtCore import* ##########################
from PyQt5.QtWidgets import* #######################
from PyQt5.QtGui import QIcon ######################
from PyQt5.QtGui import QScreen ####################
from PyQt5.QtWidgets import QFrame #################
from PyQt5.QtCore import Qt, QPropertyAnimation #### 
from PyQt5.QtCore import QSize, pyqtSignal, QObject#
from PyQt5 import QtGui, QtCore, QtWidgets ######### 
####################################################
from PyQt5.QtWidgets import (
    QWidget, QDockWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QGroupBox, QToolButton, QTextEdit, QLabel
)#########################################################

#system files:
import sys #####
import inspect #
import os 
################

#CLass for animated toolbar buttons:
class AnimatedToolButton(QToolButton):

#Constructor:
    def __init__(self, default_icon, active_icon, text, parent=None):

        #set icon on toolbar buttons:
        super().__init__(parent) ############################
        self.default_icon = default_icon ####################
        self.active_icon = active_icon ######################
        self.setIcon(self.default_icon) #####################
        self.setText(text) ##################################
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon) #
        #####################################################
        
        #setting the button size:
        self.original_geometry = None ##########################
        self.animation = QPropertyAnimation(self, b"geometry") #
        self.is_active = False #################################
        ########################################################
    #End of Constructor#########################################
    
#Active or Not:
    def setActive(self, active):
        #Sets the state of the button (active or not) #################
        self.is_active = active #######################################
        self.setIcon(self.active_icon if active else self.default_icon)
    #End of activity ##################################################

#Hover animation:
    def enterEvent(self, event):

        if not self.original_geometry:
            #Сохраняем изначальную геометрию кнопки:
            self.original_geometry = self.geometry()  
        
        #Увеличить кнопку:
        new_geometry = self.original_geometry.adjusted(-10, -10, 10, 10) ##
        self.animation.setDuration(200) ###################################
        # Текущая геометрия
        self.animation.setStartValue(self.geometry()) ##################### 
        # Увеличенная геометрия
        self.animation.setEndValue(new_geometry) ########################## 
        self.animation.start() ############################################
        super().enterEvent(event) #########################################
        ###################################################################
    #End of enter Event ###################################################

#Leave animation:
    def leaveEvent(self, event):
        # Анимация уменьшения при покидании мыши
        if self.original_geometry: #############
            self.animation.setDuration(200)
            # Текущая геометрия ###############################
            self.animation.setStartValue(self.geometry()) ##### 
            # Возвращаем к изначальной геометрии ##############
            self.animation.setEndValue(self.original_geometry)# 
            self.animation.start() ############################
        super().leaveEvent(event) #############################
#End of CLass AnimatedToolButton ######

#CLass for element buttons:
class MendeleevButton(QToolButton):
    def __init__(self, default_icon, active_icon, text, parent=None):
        super().__init__(parent)
        self.default_icon = default_icon
        self.active_icon = active_icon
        self.setIcon(self.default_icon)
        self.setText(text)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setObjectName("MendeleevBtn")

        self.is_active = False

    def setActive(self, active):
        """Устанавливает состояние кнопки (активное или нет)."""
        self.is_active = active
        self.setIcon(self.active_icon if active else self.default_icon)

    def enterEvent(self, event):
        """При наведении меняем иконку."""
        self.setIcon(self.active_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """При уходе курсора возвращаем стандартную иконку."""
        self.setIcon(self.default_icon)
        super().leaveEvent(event)
#End of CLass ELements Button #########

class TableOfNuclides(QToolButton):
    def __init__(self, default_icon, active_icon, text, parent=None):
        super().__init__(parent)
        self.default_icon = default_icon
        self.active_icon = active_icon
        self.setIcon(self.default_icon)
        self.setText(text)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setObjectName("TONbutton")

        self.is_active = False

    def setActive(self, active):
        """Устанавливает состояние кнопки (активное или нет)."""
        self.is_active = active
        self.setIcon(self.active_icon if active else self.default_icon)

    def enterEvent(self, event):
        """При наведении меняем иконку."""
        self.setIcon(self.active_icon)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """При уходе курсора возвращаем стандартную иконку."""
        self.setIcon(self.default_icon)
        super().leaveEvent(event)


#Main DockWidget on the right side to hold Model's right: 
class QDashboard(QDockWidget):

#Constructor:
    def __init__(self,parent=None):

    #settings dockwidget:
        super().__init__('Dock', parent) #################################
        ##################################################################
        self.setWindowTitle('Tool bar...') ###############################
        self.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        ##################################################################

    #main container Widget is a QGroupbox:
        self.container = QGroupBox()##################
        self.container.setObjectName('dashborder') ##
        #############################################

    #layout for main container: #####################
        self.layout = QVBoxLayout() #################
    #Set layout into container: #####################
        self.container.setLayout(self.layout) #######
    #set container as main widget: ##################
        self.setWidget(self.container) ##############
        #############################################

    #Map of number & w-QWidget 
        self.NumWidgetMap = dict() 
        self.show()
    #End of Constructor##############################

#Close pressed:
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.hide()
    #...............................

#Show:
    def Show(self):
        #self.setVisible(True)
        self.show()
    #..............

#Hide:
    def hide(self):
        pass
        for key in self.NumWidgetMap:
            self.NumWidgetMap[key].hide()
    #....................................
    
#Show Layout:
    def SetLayout(self, num):
        if num in self.NumWidgetMap:
            for key in self.NumWidgetMap:
                self.NumWidgetMap[key].hide()
        else: return
        self.NumWidgetMap[num].show()
    #........................................

#Register Layout:
    def AddLayout(self, num, layout):
        #Проверить layout на сущ в карте! 
        if not num in self.NumWidgetMap:
            self.w = QWidget() #QGroupBox()
            self.w.setLayout(layout)
            self.NumWidgetMap[num] = self.w
            self.layout.addWidget(self.w)
    #........................................

#Resize the Dockwidget:
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.parent() and hasattr(self.parent(), "sync_width"):
            self.parent().sync_width()   
#End of CLass DockWidget ##############

#CLass for holding signals:
class SignalEmitter(QObject):

#Signal to send text to GUI:
    text_written = pyqtSignal(str)
#End of CLass SignalEmitter#######

class GUITerminal(QWidget):

    _instance = None  

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GUITerminal, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        super().__init__(parent)
        if hasattr(self, "_initialized"):
            return  
        
        self._initialized = True  
        self.setObjectName("GUITerminal")  

        # Баннер терминала
        self.terminal_label = QLabel("Terminal")
        self.terminal_label.setObjectName("terminal_label")

        # Кнопка закрытия терминала
        self.close_button = QPushButton()
        self.close_button.setObjectName("close_terminal_button")
        self.close_button.setIcon(QIcon("resources/OR-arrow.png")) 
        self.close_button.setIconSize(QSize(36, 36))
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.hide)

        # Верхняя панель (заголовок + кнопка закрытия)
        top_bar = QHBoxLayout()
        top_bar.addWidget(self.terminal_label)
        top_bar.addStretch()
        top_bar.addWidget(self.close_button)
        top_bar.setContentsMargins(10, 0, 0, 0)

        # Поле для вывода текста терминала
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setObjectName("terminal_text_editor")

        # **Добавляем адаптивный шрифт**
        self.default_font_size = 12
        self.update_font_size()

        # Основной Layout терминала
        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.text_edit)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        self.setLayout(layout)

        # Адаптивность: растягиваемый терминал (по высоте)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Сигналы для обновления текста
        self.emitter = SignalEmitter()
        self.emitter.text_written.connect(self.append_text)

        # Перенаправление `sys.stdout` и `sys.stderr`
        sys.stdout = self
        sys.stderr = self

    def append_text(self, text):
        """Добавляет текст в терминал"""
        self.text_edit.append(text)

    def write(self, text):
        """Выводит текст в терминал"""
        if text.strip():
            formatted_text = f"<<< {text.strip()}"
            self.emitter.text_written.emit(formatted_text)

    def flush(self):
        """Фиктивная функция для совместимости с `sys.stdout` и `sys.stderr`"""
        pass

    def hide(self):
        """Скрытие терминала"""
        self.setVisible(False)

    def show(self):
        """Показ терминала"""
        self.setVisible(True)

    def resizeEvent(self, event):
        """Обновляет размер шрифта при изменении размера окна"""
        self.update_font_size()
        super().resizeEvent(event)

    def update_font_size(self):
        """Пересчитывает размер шрифта в зависимости от размера окна"""
        if self.parent():
            width = self.parent().width()
            height = self.parent().height()

            # Выбираем масштабирование относительно высоты окна (0.02 * высота)
            new_font_size = max(8, int(height * 0.02))

            font = QFont("Consolas", new_font_size)
            self.text_edit.setFont(font)

    def resizeEvent(self, event):
        """Динамическое изменение размера шрифта при изменении окна"""
        new_font_size = max(15, int(self.width() * 0.1))  # Масштабируем шрифт


class GUITerminal(QWidget):

    _instance = None  

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(GUITerminal, cls).__new__(cls)
        return cls._instance

    def __init__(self, parent=None):
        super().__init__(parent)
        if hasattr(self, "_initialized"):
            return  
        self._initialized = True  
        self.setObjectName("GUITerminal")  

        # Заголовок терминала
        self.terminal_label = QLabel("Terminal")
        self.terminal_label.setObjectName("terminal_label")

        # Кнопка закрытия терминала
        self.close_button = QPushButton()
        self.close_button.setObjectName("close_terminal_button")
        self.close_button.setIcon(QIcon("resources/OR-arrow.png")) 
        self.close_button.setIconSize(QSize(36, 36))
        self.close_button.setCursor(Qt.PointingHandCursor)
        self.close_button.clicked.connect(self.hide)

        # Верхняя панель (заголовок + кнопка закрытия)
        top_bar = QHBoxLayout()
        top_bar.addWidget(self.terminal_label)
        top_bar.addStretch()
        top_bar.addWidget(self.close_button)
        top_bar.setContentsMargins(10, 0, 0, 0)

        # Поле для вывода текста терминала
        self.text_edit = QTextEdit()
        self.text_edit.setReadOnly(True)
        self.text_edit.setObjectName("terminal_text_editor")

        # **Устанавливаем адаптивный шрифт**
        self.default_font_size = 12
        self.update_font_size()

        # Основной Layout терминала
        layout = QVBoxLayout()
        layout.addLayout(top_bar)
        layout.addWidget(self.text_edit)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(0)
        self.setLayout(layout)

        # **Адаптивность: растягиваемый терминал**
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Сигналы для обновления текста
        self.emitter = SignalEmitter()
        self.emitter.text_written.connect(self.append_text)

        # Перенаправление `sys.stdout` и `sys.stderr`
        sys.stdout = self
        sys.stderr = self

    def append_text(self, text):
        """Добавляет текст в терминал"""
        self.text_edit.append(text)

    def write(self, text):
        """Выводит текст в терминал"""
        if text.strip():
            formatted_text = f"<<< {text.strip()}"
            self.emitter.text_written.emit(formatted_text)

    def flush(self):
        """Фиктивная функция для совместимости с `sys.stdout` и `sys.stderr`"""
        pass

    def hide(self):
        """Скрытие терминала"""
        self.setVisible(False)

    def show(self):
        """Показ терминала"""
        self.setVisible(True)

    def resizeEvent(self, event):
        """Обновляет размер шрифта и высоту терминала при изменении размера окна"""
        self.setFixedHeight(int(self.parent().height() * 0.2))  # **Терминал занимает 20% окна**
        self.update_font_size()
        super().resizeEvent(event)

    def update_font_size(self):
        """Пересчитывает размер шрифта в зависимости от высоты окна"""
        if self.parent():
            height = self.parent().height()
            new_font_size = max(10, int(height * 0.02))  # **2% от высоты окна**
            font = QFont("Consolas", new_font_size)
            self.text_edit.setFont(font)






