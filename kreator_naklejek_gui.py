from PyQt5.QtCore import QPoint, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QPushButton, QVBoxLayout, QMessageBox, QApplication, QHBoxLayout
import sys

from test_druku import drukuj_etykiete, MOJ_PORT
from test_etykiety import generuj_etykiete

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        # 1. USUNIĘCIE SYSTEMOWEGO PASKA TYTUŁOWEGO
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(500, 400)
        
        # 2. GŁÓWNY UKŁAD OKNA (bez marginesów, żeby pasek dotykał krawędzi)
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 3. TWORZENIE WŁASNEGO PASKA TYTUŁOWEGO
        self.title_bar = QWidget()
        self.title_bar.setFixedHeight(40) # Wysokość paska
        self.title_bar.setStyleSheet("background-color: #11111b; color: #cdd6f4;") # Twój własny kolor!
        
        # Układ dla paska tytułowego (poziomy)
        self.title_layout = QHBoxLayout()
        self.title_layout.setContentsMargins(15, 0, 0, 0)
        
        # Tytuł okna
        self.title_label = QLabel("Kreator naklejek")
        
        # Przycisk minimalizacji
        self.btn_min = QPushButton("-")
        self.btn_min.setFixedSize(40, 40)
        self.btn_min.setStyleSheet("QPushButton { border: none; background: transparent; } QPushButton:hover { background-color: #45475a; }")
        self.btn_min.clicked.connect(self.showMinimized)
        
        # Przycisk zamykania
        self.btn_close = QPushButton("X")
        self.btn_close.setFixedSize(40, 40)
        self.btn_close.setStyleSheet("QPushButton { border: none; background: transparent; } QPushButton:hover { background-color: #f38ba8; color: black; }")
        self.btn_close.clicked.connect(self.close)
        
        # Dodawanie elementów do paska tytułowego
        self.title_layout.addWidget(self.title_label)
        self.title_layout.addStretch() # Wypycha przyciski na prawą stronę
        self.title_layout.addWidget(self.btn_min)
        self.title_layout.addWidget(self.btn_close)
        self.title_bar.setLayout(self.title_layout)
        
        self.pixmap_path = "gotowa_etykieta.png"
        self.podglad = QLabel()
        self.podglad.setObjectName("podglad_etykiety") # <--- DODAJEMY UNIKALNE ID
        self.podglad.setAlignment(Qt.AlignCenter)
        self.update_image()

        self.tag = QLineEdit()
        self.tag.setPlaceholderText("Wpisz TAG sprzętu (np. TEL-15)")
        self.ikona = QComboBox()
        self.ikona.addItems([
            "Brak ikony",
            "Komputer AIO",
            "Kasa fiskalna",
            "Laptop",
            "Monitor",
            "Skaner kodów",
            "Smartfon",
            "Telefon stacjonarny",
            "Telewizor (TV)",
            "Drukarka"
        ])
        self.generuj_button = QPushButton("Generuj etykietę")
        self.drukuj_button = QPushButton("Drukuj etykietę")


        #Layout
        self.content = QVBoxLayout()
        self.content.addWidget(self.podglad)
        self.content.addWidget(self.tag)
        self.content.addWidget(self.ikona)
        self.content.addWidget(self.generuj_button)
        self.content.addWidget(self.drukuj_button)
        self.content.setContentsMargins(40, 20, 40, 20)
        self.content.setSpacing(10)
        self.main_layout.addWidget(self.title_bar)
        self.main_layout.addLayout(self.content)
        self.setLayout(self.main_layout)

        #Połączenie przycisków z funkcjami
        self.ikona.currentTextChanged.connect(self.get_icon_path)
        self.generuj_button.clicked.connect(self.generowanie_etykiety)
        self.drukuj_button.clicked.connect(self.drukowanie_etykiety)

        # Zmienne potrzebne do przesuwania okna
        self.old_pos = self.pos()
    
    # 5. LOGIKA PRZESUWANIA OKNA
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if not self.old_pos.isNull():
            # Obliczamy różnicę w ruchu myszki i przesuwamy okno
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = QPoint()
        

    #Połączenie QComboBox z wyborami ikon
    def get_icon_path(self, ikona_wybrana):
        if ikona_wybrana == "Brak ikony":
            return None
        elif ikona_wybrana == "Komputer AIO":
            return "ikony/aio.png"
        elif ikona_wybrana == "Kasa fiskalna":
            return "ikony/kasa.png"
        elif ikona_wybrana == "Laptop":
            return "ikony/laptop.png"
        elif ikona_wybrana == "Monitor":
            return "ikony/monitor.png"
        elif ikona_wybrana == "Skaner kodów":
            return "ikony/skaner.png"
        elif ikona_wybrana == "Smartfon":
            return "ikony/smartfon.png"
        elif ikona_wybrana == "Telefon stacjonarny":
            return "ikony/telefon_stacjonarny.png"
        elif ikona_wybrana == "Telewizor (TV)":
            return "ikony/tv.png"
        elif ikona_wybrana == "Drukarka":
            return "ikony/drukarka.png"
        else:
            return None
        
    def update_image(self, path=None):
        """Funkcja ładująca obraz na nowo"""
        pixmap = QPixmap(self.pixmap_path)
        
        if not pixmap.isNull():
            # Skalujemy obraz, aby pasował do okna
            scaled_pixmap = pixmap.scaled(300, 120)
            self.podglad.setPixmap(scaled_pixmap)
            print(f"Obraz zaktualizowany: {self.pixmap_path}")
        else:
            QMessageBox.critical(self, "Błąd ładowania obrazu", "Wystąpił błąd podczas ładowania podglądu")
            self.podglad.setText("Błąd ładowania obrazu!")
    
    def generowanie_etykiety(self):
        try:
            generuj_etykiete(self.tag.text(), self.get_icon_path(self.ikona.currentText()))
        except Exception as e:
            QMessageBox.critical(self, "Błąd generowania", f"Wystąpił błąd podczas generowania etykiety: {e}")
        self.update_image()

    def drukowanie_etykiety(self):
        odp = QMessageBox.question(self, "Potwierdzenie druku", "Czy na pewno chcesz wydrukować tę etykietę?", QMessageBox.Yes | QMessageBox.No)
        if odp == QMessageBox.Yes:
            try:
                drukuj_etykiete(self.pixmap_path, MOJ_PORT)
            except Exception as e:
                QMessageBox.critical(self, "Błąd druku", f"Wystąpił błąd podczas drukowania: {e}")
        elif odp == QMessageBox.No:
            return
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    try:
        with open("style.qss", "r") as style_file:
            app.setStyleSheet(style_file.read())
    except FileNotFoundError:
        print("Nie znaleziono pliku style.qss. Aplikacja użyje domyślnego wyglądu.")
    # ------------------------------------
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())