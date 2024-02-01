import sys
from PySide6 import QtCore, QtWidgets, QtGui
from scraping import scrape_match_summary, excel_file

def assertURL(pasted_URL: str, response):
    if pasted_URL.startswith("https://egol.fcf.com.br/SISGOL"):
        scrape_match_summary(pasted_URL)
        response.setText('Concluído')
        return pasted_URL
    else:
        response.setText("Inválido, colar link da súmula da FCF")

class SummaryScraper(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
                
        self.setWindowTitle('Leitor de súmulas da FCF')
        self.setWindowIcon(QtGui.QIcon("Figueirense.png"))
        self.instructions = QtWidgets.QLabel(f'Para funcionamento correto:\n- O arquivo {excel_file} precisa estar fechado\n- A base de dados deve estar com o nome: {excel_file}\n- Este programa e o arquivo \"{excel_file}\" devem estar na mesma pasta\n\nColar link da súmula:')
        self.url_input_box = QtWidgets.QLineEdit(self)
        self.confirm_button = QtWidgets.QPushButton(text="Confirmar")
        self.response = QtWidgets.QLabel('')

        self.image_label = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap("Figueirense.png").scaledToHeight(100)
        self.image_label.setPixmap(pixmap)
        # self.image_label.setFixedSize(100,100)
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.instructions)
        self.layout.addWidget(self.url_input_box)
        self.layout.addWidget(self.confirm_button, alignment=QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.response)
        # self.setGeometry(500,200,200,200)

        self.confirm_button.clicked.connect(self.assert_and_scrape)
        self.url_input_box.returnPressed.connect(self.assert_and_scrape)

        self.show()

    @QtCore.Slot()
    def assert_and_scrape(self):
        try:
            assertURL(self.url_input_box.text(),self.response)
            QtCore.QTimer.singleShot(2000, lambda: self.response.setText(""))

        except FileNotFoundError:
            self.response.setText(f'O arquivo não está na mesma pasta ou nome {excel_file} está incorreto.')
            QtCore.QTimer.singleShot(8000, lambda: self.response.setText(""))

        except KeyboardInterrupt:
            self.response.setText('Interrompido')
                       
        except ValueError:
            self.response.setText('Colar um link de súmula da FCF')
            
        except PermissionError:
            self.response.setText(f'Feche o arquivo {excel_file}')
                
        # except ...
            # error for a match not from figueirense
            # self.response.setText('Não é partida do Figueirense')
            
        except Exception:
            self.response.setText('Erro')

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    scrape_app = SummaryScraper()
    scrape_app.resize(700,200)
    # scrape_app.show()

    sys.exit(app.exec())