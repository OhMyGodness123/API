import sys
from io import BytesIO
import requests
from PIL import Image
import pprint
import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit

SCREEN_SIZE = [800, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.image = QLabel(self)
        self.map = 'map'
        self.map_file = "map.png"
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.line = QLineEdit(self)
        self.line.move(650, 160)
        self.text = 'парк'
        self.btn = QPushButton('Искать', self)
        self.btn.resize(100, 30)
        self.btn.move(670, 200)
        self.btn.clicked.connect(self.run)
        self.getImage()
        self.initUI()

    def getImage(self):
        print(self.text)
        search_api_server = "https://search-maps.yandex.ru/v1/"
        api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
        address_ll = "37.588392,55.734036"
        search_params = {
            "apikey": api_key,
            "text": self.text,
            "lang": "ru_RU",
            "ll": address_ll,
            "type": "biz"
        }
        response = requests.get(search_api_server, params=search_params)
        if not response:
            print("Ошибка выполнения запроса:")
            print(search_api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
        json_response = response.json()
        organization = json_response['features'][0]
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        point = organization["geometry"]["coordinates"]
        org_point = "{0},{1}".format(point[0], point[1])
        delta = "0.005"
        map_params = {
            "ll": address_ll,
            "spn": ",".join([delta, delta]),
            "l": "map",
            "pt": "{0},pm2dgl".format(org_point)
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        print(response)
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        self.pixmap = QPixmap(self.map_file)
        self.image.setPixmap(self.pixmap)
        self.update()

    def run(self):
        self.text = self.line.text()
        self.line.clear()
        self.getImage()

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Отображение карты')

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
