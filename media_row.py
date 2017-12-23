import subprocess

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import media_menu

media_menu = media_menu.media_menu

class media_row(QHBoxLayout):
    def __init__(self, media_menu, image_path, title, command):

        super().__init__()

        self.media_menu = media_menu

        self.title = title

        self.visible = True

        self.image = QLabel()
        self.image.setPixmap( QPixmap(image_path) )
        self.image.setMargin(5)
        self.image.mouseReleaseEvent = self.mousePress
        self.image.mouseDoubleClickEvent = self.mousePressDouble
        self.addWidget(self.image)

        self.label = QLabel()
        self.label.setText(title)
        self.label.mouseReleaseEvent = self.mousePress
        self.label.mouseDoubleClickEvent = self.mousePressDouble
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.addWidget(self.label)

        self.command = command

        self.deselect()

    def mousePress(self,QMouseEvent):
        self.select()

    def mousePressDouble(self,QMouseEvent):
        self.run_command()
        QCoreApplication.quit()

    def select(self):
        if media_row.selected != None:
            media_row.selected.deselect()

        self.image.setStyleSheet(self.selected_style)
        self.label.setStyleSheet(self.selected_style)

        media_row.selected = self
        self.media_menu.ensure_row_visible(self)

    def deselect(self):
        self.image.setStyleSheet(self.deselected_style)
        self.label.setStyleSheet(self.deselected_style)

    def hide(self):
        self.label.hide()
        self.image.hide()
        self.visible = False

    def show(self):
        self.label.show()
        self.image.show()
        self.visible = True

    def run_command(self):
        subprocess.Popen(self.command, shell=True)

    selected_style   = "background-color: " + media_menu.color_light + "; color: black; font-size: 16pt; font-weight: bold;"
    deselected_style = "background-color: " + media_menu.color_dark + "; color: white; font-size: 16pt; font-weight: bold;"

    selected = None
