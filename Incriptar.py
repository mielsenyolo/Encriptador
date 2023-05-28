import os
from PyQt5 import QtWidgets, QtCore
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import sys
import subprocess


class SecondInterface(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()
    encrypt_completed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Encriptar")
        self.setGeometry(300, 300, 700, 600)
        self.setStyleSheet("background-color: #303030;")

        # Título en pantalla
        self.label = QtWidgets.QLabel("Mielsenyolo", self)
        self.label.setGeometry(310, 50, 300, 30)
        self.label.setStyleSheet("color: white; font-size: 18px;")

        # Título en pantalla
        self.label = QtWidgets.QLabel("Encriptar archivo", self)
        self.label.setGeometry(300, 270, 300, 30)
        self.label.setStyleSheet("color: white; font-size: 18px;")

        # Boton1
        self.button1 = QtWidgets.QPushButton("Seleccionar archivo para encriptar", self)
        self.button1.setGeometry(230, 450, 250, 50)
        self.button1.setStyleSheet("background-color: white; color: black;")
        self.button1.clicked.connect(self.select_file_to_encrypt)

    def closeEvent(self, event):
        self.closed.emit()
        event.ignore()

    def select_file_to_encrypt(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo para encriptar")
        if file_path:
            self.encrypt_file(file_path)

    def encrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            file_data = file.read()

        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_data = cipher_suite.encrypt(file_data)

        save_dir = QFileDialog.getExistingDirectory(self, "Seleccionar directorio de guardado")
        if save_dir:
            original_name = os.path.basename(file_path)
            original_extension = os.path.splitext(file_path)[1]  # Obtener la extensión del archivo original
            save_location = os.path.join(save_dir, f"{original_name}{original_extension}")

            with open(save_location, 'wb') as encrypted_file:
                encrypted_file.write(encrypted_data)

            key_file_path = save_location + '.key.txt'
            with open(key_file_path, 'w') as key_file:
                key_file.write(key.decode())

            msg_box = QMessageBox()
            msg_box.setStyleSheet("QLabel{background-color: white;}")
            msg_box.setText("Guardado Exitoso")
            msg_box.setInformativeText(f"Archivo encriptado guardado en: {save_location}\n"
                                       f"Archivo de clave guardado en: {key_file_path}")
            msg_box.exec_()

            self.encrypt_completed.emit()

            # Cerrar la aplicación actual y abrir index.py nuevamente
            QtWidgets.QApplication.quit()
            subprocess.Popen(["python", "index.py"])

    def closeEvent(self, event):
        QtWidgets.QApplication.quit()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SecondInterface()
    window.show()
    sys.exit(app.exec_())