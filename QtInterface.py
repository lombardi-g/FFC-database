import sys
from PySide6 import QtCore, QtWidgets, QtGui

excel_file = "teste"

class SummaryScraper(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
                
        self.setWindowTitle('Leitor de súmulas da FCF')
        self.setWindowIcon(QtGui.QIcon("Figueirense.png"))
        self.label = QtWidgets.QLabel(f'Para funcionamento correto:\n- A base de dados deve estar com o nome: {excel_file}\n- Este programa e o arquivo \"{excel_file}\" devem estar na mesma pasta\n\nColar link da súmula:')
        self.url_input_box = QtWidgets.QLineEdit(self)
        self.confirm_button = QtWidgets.QPushButton(text="Confirmar")
        self.response = QtWidgets.QLabel('')

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.url_input_box)
        self.layout.addWidget(self.confirm_button, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.response)
        # self.setGeometry(500,200,200,200)

        self.confirm_button.clicked.connect(self.assert_and_scrape)

        self.show()

    @QtCore.Slot()
    def assert_and_scrape(self):
        self.response.setText("test")


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    scrape_app = SummaryScraper()
    scrape_app.resize(500,200)
    # scrape_app.show()

    sys.exit(app.exec())