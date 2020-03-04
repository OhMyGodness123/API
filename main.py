import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.zoom = 9
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        params = {
            'll': '40.588386,55.633778',
            'z': str(self.zoom),
            'l': 'map'
        }
        response = requests.get(map_request, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.add_pix()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')
        self.add_pix()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            if self.zoom != 0:
                self.zoom -= 1
                self.getImage()
        if event.key() == Qt.Key_PageUp:
            if self.zoom != 17:
                self.zoom += 1
                self.getImage()

    def add_pix(self):
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.update()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
