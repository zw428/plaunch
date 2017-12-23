from PyQt5.QtWidgets import *

class filter_input(QLineEdit):
    def __init__(self, media_menu):
        super().__init__()

        self.media_menu = media_menu

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        self.media_menu.handle_filtering(event, super().text())
