import os
from PyQt5 import QtWidgets, QtCore
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import sys
import subprocess


class SecondInterface(QtWidgets.QMainWindow):
    closed = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Desencriptar")
        self.setGeometry(300, 300, 700, 600)
        self.setStyleSheet("background-color: #303030;")

        # Título en pantalla
        self.label = QtWidgets.QLabel("Mielsenyolo", self)
        self.label.setGeometry(310, 50, 300, 30)
        self.label.setStyleSheet("color: white; font-size: 18px;")

        # Título en pantalla
        self.label = QtWidgets.QLabel("Desencriptar archivo", self)
        self.label.setGeometry(270, 280, 300, 30)
        self.label.setStyleSheet("color: white; font-size: 18px;")

        # Boton1
        self.button1 = QtWidgets.QPushButton("Seleccionar archivo encriptado", self)
        self.button1.setGeometry(230, 450, 250, 50)
        self.button1.setStyleSheet("background-color: white; color: black;")
        self.button1.clicked.connect(self.select_encrypted_file)

    def closeEvent(self, event):
        self.closed.emit()
        event.ignore()

    def select_encrypted_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo encriptado")
        if file_path:
            self.decrypt_file(file_path)

    def decrypt_file(self, file_path):
        key_file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de clave")
        if key_file_path:
            with open(key_file_path, 'rb') as key_file:
                key = key_file.read()

            try:
                cipher_suite = Fernet(key)
                with open(file_path, 'rb') as encrypted_file:
                    encrypted_data = encrypted_file.read()

                decrypted_data = cipher_suite.decrypt(encrypted_data)

                save_dir = QFileDialog.getExistingDirectory(self, "Seleccionar directorio de guardado")
                if save_dir:
                    original_extension = os.path.splitext(file_path)[1]  # Obtener la extensión del archivo encriptado
                    original_file_path = os.path.join(save_dir, f"decrypted_file{original_extension}")

                    with open(original_file_path, 'wb') as decrypted_file:
                        decrypted_file.write(decrypted_data)

                    print("Archivo desencriptado guardado:", original_file_path)
                else:
                    print("No se seleccionó un directorio de guardado.")

            except Exception as e:
                QMessageBox.warning(self, "Error", "Error al desencriptar el archivo. Verifique el archivo de clave.")

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