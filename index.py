from PyQt5 import QtWidgets, QtGui
from cryptography.fernet import Fernet

import Desencriptar
import Incriptar

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Encriptador")
        self.setGeometry(300, 300, 700, 600)
        self.setStyleSheet("background-color: #303030;")

        # Título en pantalla
        self.label = QtWidgets.QLabel("Mielsenyolo", self)
        self.label.setGeometry(310, 50, 300, 30)
        self.label.setStyleSheet("color: white; font-size: 18px;")

        # Imagen
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setGeometry(180, 100, 300, 200)

        image_path = "resources/logo.jpg" # Ruta de la imagen que deseas mostrar
        self.show_image(image_path)

        # Boton1
        self.button1 = QtWidgets.QPushButton("Desencriptar", self)
        self.button1.setGeometry(450, 450, 150, 50)
        self.button1.setStyleSheet("background-color: white; color: black;")
        self.button1.clicked.connect(self.open_desencriptar)

        # Boton2
        self.button2 = QtWidgets.QPushButton("Encriptar", self)
        self.button2.setGeometry(100, 450, 150, 50)
        self.button2.setStyleSheet("background-color: white; color: black;")
        self.button2.clicked.connect(self.open_incriptar)

    def open_desencriptar(self):
        self.hide()
        self.desencriptar_interface = Desencriptar.SecondInterface()
        self.desencriptar_interface.closed.connect(self.show)
        self.desencriptar_interface.show()

    def open_incriptar(self):
        self.hide()
        self.incriptar_interface = Incriptar.SecondInterface()
        self.incriptar_interface.closed.connect(self.show)
        self.incriptar_interface.show()

    def show_image(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        self.image_label.setPixmap(pixmap.scaled(300, 200))
 

    def closeEvent(self, event):
      QtWidgets.QApplication.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_() 