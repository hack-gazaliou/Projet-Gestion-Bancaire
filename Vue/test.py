# Importation des bibliothèques
import sys
from PySide6.QtWidgets import *


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Définition du titre de la fenêtre
        self.setWindowTitle("Hello!")

        # Ajout des widgets
        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Quel est votre nom ?")
        self.button = QPushButton("Dis-moi bonjour")

        # Création d'une disposition verticale QVBox
        layout = QVBoxLayout()

        # On ajoute les widgets créé à la disposition
        # Le champ edit sera donc au-dessus du bouton
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        # Création d'un widget principal qui va tout contenir
        central_widget = QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)





if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    # Create and show the form
    window = MainWindow()
    window.show()
    # Run the main Qt loop
    sys.exit(app.exec())