#!/usr/bin/python3

import sys
import subprocess
import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class game_menu(QScrollArea):

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

        pal = QPalette();
        pal.setColor( QPalette.Window, QColor(self.color_dark_arr[0], self.color_dark_arr[1], self.color_dark_arr[2]) );
        self.app.setPalette(pal);

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

        self.frame.layout().addStretch(1)

        self.show()
        sys.exit(self.app.exec_())

    color_dark_arr  = [20,20,20]
    color_light_arr = [220,220,220]

    color_dark   = "rgb(%s,%s,%s)" % (color_dark_arr[0], color_dark_arr[1], color_dark_arr[2])
    color_light  = "rgb(%s,%s,%s)" % (color_light_arr[0], color_light_arr[1], color_light_arr[2])

    def keyPressEvent(self, event):
        if game_row.selected:
            y = game_row.selected.image.y()
            h = game_row.selected.image.height() 

            if event.key() == 16777235: #up
                if game_row.selected.prev_row:
                    game_row.selected.prev_row.select()
                    self.ensureVisible(0,y,0,h*2)

            if event.key() == 16777237: #down
                if game_row.selected.next_row:
                    game_row.selected.next_row.select()
                    self.ensureVisible(0,y+h,0,h*2)


            if event.key() == 16777220: #enter
                game_row.selected.run_command()
                QCoreApplication.quit()

    def add_row(self, image_path, title, command):
        row = game_row(image_path,title,command)

        if self.last_row != None:
            self.last_row.next_row = row

        row.prev_row = self.last_row
        row.next_row = None
        self.last_row = row
        self.frame.layout().addLayout( row )
    

class game_row(QHBoxLayout):

    def __init__(self, image_path, title, command):

        super().__init__()

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
        if game_row.selected != None:
            game_row.selected.deselect()

        self.image.setStyleSheet(self.selected_style)
        self.label.setStyleSheet(self.selected_style)
        
        game_row.selected = self
    
    def deselect(self):
        self.image.setStyleSheet(self.deselected_style)
        self.label.setStyleSheet(self.deselected_style)

    def run_command(self):
        subprocess.Popen(self.command, shell=True)

    selected_style   = "background-color: " + game_menu.color_light + "; color: black; font-size: 16pt; font-weight: bold;"
    deselected_style = "background-color: " + game_menu.color_dark + "; color: white; font-size: 16pt; font-weight: bold;"
    
    selected = None
        

if __name__ == "__main__":

    test = game_menu();
