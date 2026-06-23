# NIIMBOT B3S Label Generator

Aplikacja z graficznym interfejsem użytkownika (GUI) napisanym w **PyQt5**, służąca do generowania i drukowania kodów kreskowych, ikon oraz etykiet identyfikacyjnych (TAG-ów) dla sprzętu IT na drukarce termicznej **NIIMBOT B3S**. Projekt stanowi część systemu automatycznej ewidencji majątku IT (Smart IT Asset Manager).

## Funkcje projektu
- **Własny pasek tytułowy**: Nowoczesny, bezramkowy design okna (Frameless Window) z autorskim stylem i obsługą przeciągania myszą.
- **Dynamiczny podgląd**: Automatyczne generowanie i odświeżanie wyglądu etykiety przed wydrukiem.
- **Wybór ikon sprzętu**: Łatwa kategoryzacja urządzeń (np. Laptop, Monitor, Drukarka, Smartfon itp.) za pomocą menu rozwijanego.
- **Integracja z drukarką**: Bezpośrednie wysyłanie gotowych etykiet do drukarki NIIMBOT B3S.
- **Personalizacja za pomocą QSS**: Cały interfejs został ostylowany przy użyciu zewnętrznego arkusza stylów `style.qss` opartego na ciemnej palecie barw.

## Struktura plików
- `kreator_naklejek_gui.py` - Główny plik aplikacji zawierający logikę interfejsu PyQt5 oraz obsługę zdarzeń.
- `style.qss` - Arkusz stylów CSS/QSS definiujący wygląd okna, pól tekstowych, przycisków i podglądu.
- `kreator_naklejek_gui.bat` - Skrypt wsadowy systemu Windows umożliwiający szybkie uruchamianie aplikacji w tle z poziomu środowiska wirtualnego.
- `test_etykiety.py` - Moduł odpowiedzialny za generowanie obrazu etykiety (PNG) na podstawie TAG-u i ikony.
- `test_druku.py` - Moduł realizujący komunikację z drukarką NIIMBOT i wysyłanie poleceń drukowania.

## Wymagania i instalacja

1. Upewnij się, że masz zainstalowanego Pythona w wersji 3.8 lub nowszej.
2. Sklonuj repozytorium lub pobierz pliki projektu.
3. Utwórz wirtualne środowisko i zainstaluj wymagane pakiety:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Na Windows: .venv\Scripts\activate
   pip install -r requirements.txt
