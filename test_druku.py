import os
from PIL import Image
from niimprint import PrinterClient, SerialTransport

# Importujemy funkcję z drugiego pliku
from test_etykiety import generuj_etykiete

# TUTAJ WPISZ SWÓJ PORT
MOJ_PORT = "COM6" 

def drukuj_etykiete(sciezka_obrazu, port_com):
    if not os.path.exists(sciezka_obrazu):
        print(f"[!] Nie znaleziono pliku: {sciezka_obrazu}.")
        return

    try:
        obraz_oryginalny = Image.open(sciezka_obrazu).convert("1")
        print(f"[*] Łączenie z drukarką Niimbot (Port {port_com})...")
        
        transport = SerialTransport(port=port_com)
        drukarka = PrinterClient(transport)
        
        print("[*] Wysyłanie do druku...")
        drukarka.print_image(obraz_oryginalny, density=3)
        print("[+] Gotowe! Etykieta wydrukowana.")
        
    except Exception as e:
        print(f"[!] Błąd podczas komunikacji z drukarką: {e}")
        print("    Upewnij się, że drukarka jest włączona i nie jest połączona z telefonem.")

if __name__ == "__main__":
    print("=======================================")
    print("      RĘCZNY KREATOR ETYKIET")
    print("=======================================")
    
    while True:
        print("\n---------------------------------------")
        # Krok 1: Pytamy o tekst na naklejce (dodana opcja wyjścia)
        tag = input("Podaj TAG sprzętu (np. M-SALUS-15) [lub wpisz 'X', aby wyjść]: ").strip()
        
        # Warunek przerwania pętli i wyjścia z programu
        if tag.upper() == 'X':
            print("Zamykanie kreatora etykiet. Do zobaczenia!")
            break
            
        # Zabezpieczenie przed wpisaniem pustego TAGu
        if not tag:
            print("[!] TAG nie może być pusty. Spróbuj ponownie.")
            continue
        
        # Krok 2: Menu wyboru ikony
        print("\nWybierz ikonę (wpisz numer):")
        print(" 1. Komputer AIO")
        print(" 2. Kasa fiskalna")
        print(" 3. Laptop")
        print(" 4. Monitor")
        print(" 5. Skaner kodów")
        print(" 6. Smartfon")
        print(" 7. Telefon stacjonarny")
        print(" 8. Telewizor (TV)")
        print(" 9. UPS")
        print("10. drukarka")
        print("0. Brak ikony (tylko tekst i QR)")
        
        wybor = input("Twój wybór (1-10): ").strip()
        
        sciezka_ikony = ""
        if wybor == "1": sciezka_ikony = "ikony/aio.png"
        elif wybor == "2": sciezka_ikony = "ikony/kasa.png"
        elif wybor == "3": sciezka_ikony = "ikony/laptop.png"
        elif wybor == "4": sciezka_ikony = "ikony/monitor.png"
        elif wybor == "5": sciezka_ikony = "ikony/skaner.png"
        elif wybor == "6": sciezka_ikony = "ikony/smartfon.png"
        elif wybor == "7": sciezka_ikony = "ikony/telefon_stacjonarny.png"
        elif wybor == "8": sciezka_ikony = "ikony/tv.png"
        elif wybor == "9": sciezka_ikony = "ikony/ups.png"
        elif wybor == "10": sciezka_ikony = "ikony/drukarka.png"
        elif wybor == "0": sciezka_ikony = None
        else:
            print("[!] Niepoprawny wybór ikony. Spróbuj ponownie.")
            continue
        
        # Krok 3: Generowanie obrazka
        nazwa_pliku = "gotowa_etykieta.png"
        generuj_etykiete(tag, sciezka_ikony, nazwa_pliku)
        print(f"\n[+] Wygenerowano podgląd: {nazwa_pliku}")
        
        # Krok 4: Pytanie o wydruk
        czy_drukowac = input("Czy chcesz teraz wydrukować tę naklejkę? (T/N): ").strip().upper()
        if czy_drukowac == 'T':
            drukuj_etykiete(nazwa_pliku, MOJ_PORT)
        else:
            print("[-] Anulowano wydruk. Obraz został zapisany na dysku.")