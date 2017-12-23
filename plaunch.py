#!/usr/bin/python3

import sys
import subprocess
import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class media_menu(QScrollArea):
    def __init__(self):
        self.app = QApplication(sys.argv)

        super().__init__()

        self.setWindowTitle("plaunch")

        self.last_row = None

        self.setWidgetResizable(True)
        self.frame = QFrame(self)
        self.frame.setLayout(QVBoxLayout())
        self.frame.layout().setSpacing(0)

        self.setWidget(self.frame)

        pal = QPalette()
        pal.setColor( QPalette.Window, QColor(self.color_dark_arr[0], self.color_dark_arr[1], self.color_dark_arr[2]) )
        self.app.setPalette(pal)

        self.add_rows()

        self.frame.layout().addStretch(1)

        self.find_frame = QFrame(self)
        self.find_frame.setLayout(QVBoxLayout())
        self.find_input = FilterInput(self)
        self.find_frame.layout().addWidget(self.find_input)
        self.find_frame.hide()

        self.show()
        sys.exit(self.app.exec_())

    def add_row(self, image_path, title, command):
        row = media_row(self,image_path,title,command)

        if self.last_row != None:
            self.last_row.next_row = row

        row.prev_row = self.last_row
        row.next_row = None
        self.last_row = row
        self.frame.layout().addLayout( row )

    def add_rows(self):
        line_reg = re.compile(r"\ *\"(.*)\"\ *,\ *\"(.*)\"\ *,\ *\"(.*)\"\ *")

        list_file_name = ""

        try:
            list_file_name = sys.argv[1]
        except:
            print("Usage: " + sys.argv[0] + " filename")
            print("File should have lines formatted as: \"image_filename\",\"title\",\"shell_command\"")
            sys.exit()

        with open(list_file_name,'r') as f:
            counter=0
            for line in f:
                counter += 1
                match = line_reg.match(line)

                if not match:
                    print("could not parse line " + str(counter) + " of " + list_file_name)
                    continue

                self.add_row(match[1],match[2],match[3])

    def find_row_by_start_letter(self, letter):
        index = 0
        selected_index = None
        for media_row in self.frame.layout().children():
            index += 1

            if media_row == media_row.selected:
                selected_index = index

            if media_row.selected and media_row.selected.title.lower()[0] == letter:
                if letter == media_row.title.lower()[0] and selected_index != None and index > selected_index:
                    media_row.select()
                    break

                elif media_row.selected.next_row and media_row.selected.next_row.title.lower()[0] == letter:
                    media_row.selected.next_row.select()
                    break

            elif media_row.title.lower()[0] == letter:
                media_row.select()
                break

    def handle_arrows(self,event):
        to_select = None
        if event.key() == Qt.Key_Up:
            if media_row.selected.prev_row:
                to_select = media_row.selected.prev_row

                while to_select and not to_select.visible:
                    to_select = to_select.prev_row

        if event.key() == Qt.Key_Down:
            if media_row.selected.next_row:
                to_select = media_row.selected.next_row

                while to_select and not to_select.visible:
                    to_select = to_select.next_row

        if to_select:
            to_select.select()

    def keyPressEvent(self, event):
        if self.app.keyboardModifiers() == Qt.ControlModifier and event.key() == Qt.Key_F:
            if self.find_frame.isVisible():
                self.find_frame.hide()
            else:
                self.find_frame.show()
                self.find_input.setFocus()
            return

        if self.find_input.hasFocus():
            if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Return:
                self.find_frame.hide()
            return

        elif event.text().lower():
            self.find_row_by_start_letter(event.text().lower()[0])

        if media_row.selected:
            self.handle_arrows(event)

            if event.key() == Qt.Key_Return:
                media_row.selected.run_command()
                QCoreApplication.quit()

    def ensure_row_visible(self, row):
        y = row.image.y()
        h = row.image.height()
        self.ensureVisible(0,y,0,h*2)

    def handle_filtering(self, event, text):
        reg = re.compile(".*" + text + ".*")
        selected_one = False
        for widget in self.frame.layout().children():
            if not isinstance(widget,media_row):
                continue

            if reg.match(widget.title):
                widget.show()
                if not selected_one:
                    widget.select()
                    selected_one = True
            else:
                widget.hide()
                widget.deselect()

    color_dark_arr  = [20,20,20]
    color_light_arr = [220,220,220]
    color_dark      = "rgb(%s,%s,%s)" % (color_dark_arr[0], color_dark_arr[1], color_dark_arr[2])
    color_light     = "rgb(%s,%s,%s)" % (color_light_arr[0], color_light_arr[1], color_light_arr[2])


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

class FilterInput(QLineEdit):
    def __init__(self, media_menu):
        super().__init__()

        self.media_menu = media_menu

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.media_menu.handle_filtering(event, super().text())

if __name__ == "__main__":
    menu = media_menu()
