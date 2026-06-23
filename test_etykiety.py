import os
import qrcode
from PIL import Image, ImageDraw, ImageFont

def generuj_etykiete(tag, sciezka_ikony, plik_wyjsciowy="gotowa_etykieta.png"):
    szerokosc, wysokosc = 400, 160
    etykieta = Image.new('RGB', (szerokosc, wysokosc), color='white')
    draw = ImageDraw.Draw(etykieta)
    
    margines_lewy = 25   
    margines_prawy = 30  
    
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(tag)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    
    rozmiar_qr = 120 
    qr_img = qr_img.resize((rozmiar_qr, rozmiar_qr))
    pozycja_y_qr = (wysokosc - rozmiar_qr) // 2
    etykieta.paste(qr_img, (margines_lewy, pozycja_y_qr)) 
    
    obszar_x_start = margines_lewy + rozmiar_qr + 20 
    dostepna_szerokosc = szerokosc - obszar_x_start - margines_prawy

    rozmiar_czcionki = 38 
    
    def pobierz_szerokosc(tekst, czcionka):
        try:
            return draw.textlength(tekst, font=czcionka)
        except AttributeError:
            return draw.textsize(tekst, font=czcionka)[0]

    try:
        font = ImageFont.truetype("arialbd.ttf", rozmiar_czcionki)
    except IOError:
        font = ImageFont.load_default()

    while pobierz_szerokosc(tag, font) > dostepna_szerokosc and rozmiar_czcionki > 10:
        rozmiar_czcionki -= 2
        try:
            font = ImageFont.truetype("arialbd.ttf", rozmiar_czcionki)
        except IOError:
            break

    szerokosc_tekstu = pobierz_szerokosc(tag, font)
    pozycja_x_tekst = obszar_x_start + (dostepna_szerokosc - szerokosc_tekstu) / 2
    pozycja_y_tekst = 20 
    
    draw.text((pozycja_x_tekst, pozycja_y_tekst), tag, font=font, fill="black")
    
    if sciezka_ikony and os.path.exists(sciezka_ikony):
        ikona = Image.open(sciezka_ikony).convert('RGBA')
        rozmiar_ikony = 65 
        ikona = ikona.resize((rozmiar_ikony, rozmiar_ikony))
        
        pozycja_x_ikona = int(obszar_x_start + (dostepna_szerokosc - rozmiar_ikony) / 2)
        pozycja_y_ikona = 75 
        
        etykieta.paste(ikona, (pozycja_x_ikona, pozycja_y_ikona), ikona)
    elif sciezka_ikony:
        print(f" [!] Uwaga: Brak pliku ikony ({sciezka_ikony}). Generuję bez ikony.")

    etykieta.save(plik_wyjsciowy)
    return plik_wyjsciowy