import sys
import re
import argparse

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import filter_input

class media_menu(QScrollArea):
    def __init__(self):
        self.app = QApplication(sys.argv)

        super().__init__()

        argparser = argparse.ArgumentParser("File should have lines formatted as: \"image_filename\",\"title\",\"shell_command\"")
        argparser.add_argument("-s", "--sort", type=int, nargs="?", const=0, default=1, help="Whether or not to sort entries by name (0 or 1). %(default)s by default.")
        argparser.add_argument("filename")

        args = argparser.parse_args()

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

        self.add_rows(args.filename, args.sort)

        self.frame.layout().addStretch(1)

        self.find_frame = QFrame(self)
        self.find_frame.setLayout(QVBoxLayout())
        self.find_input = filter_input.filter_input(self)
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

    def add_rows(self, filename, sort):
        line_reg = re.compile(r"\ *\"(.*)\"\ *,\ *\"(.*)\"\ *,\ *\"(.*)\"\ *")

        file_lines = []

        with open(filename,'r') as f:
            counter=0
            for line in f:
                counter += 1
                match = line_reg.match(line)

                if not match:
                    print("could not parse line " + str(counter) + " of " + filename)
                    continue

                file_lines.append([match[1], match[2], match[3]])

        if sort:
                file_lines = sorted(file_lines, key=lambda line: line[1])

        for fl in file_lines:
                self.add_row(fl[0], fl[1], fl[2])

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
        selected_one = False
        for widget in self.frame.layout().children():
            if not isinstance(widget,media_row):
                continue

            if text.lower() in widget.title.lower():
                widget.show()
                if not selected_one:
                    widget.select()
                    selected_one = True
            else:
                widget.hide()
                widget.deselect()

        if not selected_one:
                media_row.selected = None

    color_dark_arr  = [20,20,20]
    color_light_arr = [220,220,220]
    color_dark      = "rgb(%s,%s,%s)" % (color_dark_arr[0], color_dark_arr[1], color_dark_arr[2])
    color_light     = "rgb(%s,%s,%s)" % (color_light_arr[0], color_light_arr[1], color_light_arr[2])

import media_row
media_row = media_row.media_row
