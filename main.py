import os
import sys

import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.zoom = 9
        self.image = QLabel(self)
        self.btn = QPushButton('Схема', self)
        self.resize(25, 250)
        self.btn.move(525, 425)
        self.btn.clicked.connect(self.run)
        self.map = 'map'
        self.map_file = "map.png"
        self.coord_x = 40.588386
        self.coord_y = 55.633778
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.getImage()
        self.initUI()

    def getImage(self):
        map_request = "http://static-maps.yandex.ru/1.x/"
        params = {
            'll': ','.join([str(self.coord_x), str(self.coord_y)]),
            'l': self.map,
            'z': str(self.zoom)
        }
        response = requests.get(map_request, params=params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.update()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.coord_x -= 0.01
            self.getImage()
        if event.key() == Qt.Key_Right:
            self.coord_x += 0.01
            self.getImage()
        if event.key() == Qt.Key_Down:
            self.coord_y -= 0.01
            self.getImage()
        if event.key() == Qt.Key_Up:
            self.coord_y += 0.01
            self.getImage()
        if event.key() == Qt.Key_PageDown:
            if self.zoom != 0:
                self.zoom -= 1
                self.getImage()
        if event.key() == Qt.Key_PageUp:
            if self.zoom != 17:
                self.zoom += 1
                self.getImage()

    def run(self):
        if self.btn.text() == 'Схема':
            self.btn.setText('Спутник')
            self.map = 'sat'
            self.map_file = 'map.jpg'
        elif self.btn.text() == 'Спутник':
            self.btn.setText('Гибрид')
            self.map = 'skl'
            self.map_file = 'map.png'
        elif self.btn.text() == 'Гибрид':
            self.btn.setText('Схема')
            self.map = 'map'
            self.map_file = 'map.png'
        self.getImage()

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())