# 'pip install PySide6' tarvitaan 
import sys
import random
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene, QMenu
from PySide6.QtGui import QPainter, QPen, QBrush, QFont
from PySide6.QtCore import Qt, QTimer

# vakiot
SOLUN_KOKO = 20
RUUDUKON_LEVEYS = 20
RUUDUKON_KORKEUS = 15

class Matopeli(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene(self))
        self.setRenderHint(QPainter.Antialiasing)
        self.setSceneRect(0, 0, SOLUN_KOKO * RUUDUKON_LEVEYS, SOLUN_KOKO * RUUDUKON_KORKEUS)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.paivita_peli)
        
        self.kaynnista_peli()

    def keyPressEvent(self, event):
        nappain = event.key()
        if nappain in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            # päivitetään suunta vain jos se ei ole vastakkainen valitulle suunnalle
            if nappain == Qt.Key_Left and self.suunta != Qt.Key_Right:
                self.suunta = nappain
            elif nappain == Qt.Key_Right and self.suunta != Qt.Key_Left:
                self.suunta = nappain
            elif nappain == Qt.Key_Up and self.suunta != Qt.Key_Down:
                self.suunta = nappain
            elif nappain == Qt.Key_Down and self.suunta != Qt.Key_Up:
                self.suunta = nappain

    def paivita_peli(self):
        paa_x, paa_y = self.mato[0]

        if self.suunta == Qt.Key_Left:
            uusi_paa = (paa_x - 1, paa_y)
        elif self.suunta == Qt.Key_Right:
            uusi_paa = (paa_x + 1, paa_y)
        elif self.suunta == Qt.Key_Up:
            uusi_paa = (paa_x, paa_y - 1)
        elif self.suunta == Qt.Key_Down:
            uusi_paa = (paa_x, paa_y + 1)

        self.mato.insert(0, uusi_paa)
        
        self.mato.pop()

        self.piirra_peli()

    def piirra_peli(self):
        self.scene().clear()

        for osa in self.mato:
            x, y = osa
            self.scene().addRect(x * SOLUN_KOKO, y * SOLUN_KOKO, SOLUN_KOKO, SOLUN_KOKO, QPen(Qt.black), QBrush(Qt.black))
        
    def kaynnista_peli(self):
        self.suunta = Qt.Key_Right
        self.mato = [(5, 5), (5, 6), (5, 7)]
        self.timer.start(300)

def main():
    sovellus = QApplication(sys.argv)
    peli = Matopeli()
    peli.show()
    sys.exit(sovellus.exec())

if __name__ == "__main__":
    main()