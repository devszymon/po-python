# main.py
import sys
import os
from swiat import Swiat
from organizmy.zwierzeta import Wilk, Owca, Lis, Zolw, Antylopa, CyberOwca, Czlowiek
from organizmy.rosliny import Trawa, Mlecz, Guarana, WilczeJagody, BarszczSosnowskiego

def wyczysc_ekran():
    os.system('cls' if os.name == 'nt' else 'clear')

def start_gry():
    swiat = Swiat(20, 20)

    # Inicjalizacja gracza
    gracz = Czlowiek(swiat)
    swiat.dodaj_organizm(gracz, (10, 10))

    # Wypełnianie planszy florą i fauną w losowych miejscach
    klasy_startowe = [
        Wilk, Owca, Lis, Zolw, Antylopa, CyberOwca,
        Trawa, Mlecz, Guarana, WilczeJagody, BarszczSosnowskiego
    ]

    for klasa in klasy_startowe:
        for _ in range(3): # po 3 z każdego rodzaju
            wolne = swiat.znajdz_wolne_sasiednie((10,10), zasieg=10)
            if wolne:
                swiat.dodaj_organizm(klasa(swiat), wolne)

    while True:
        wyczysc_ekran()
        swiat.rysuj_swiat()
        
        print("\n--- ZDARZENIA ---")
        for log in swiat.pobierz_logi_i_wyczysc():
            print(log)

        print("\nSterowanie: W/A/S/D - ruch, P - Całopalenie, Spacja - pomiń, Q - wyjście")
        akcja = input("Podaj akcję: ").strip().lower()

        if akcja == 'q':
            break
        elif akcja == 'w':
            gracz.kierunek_ruchu = (0, -1)
        elif akcja == 's':
            gracz.kierunek_ruchu = (0, 1)
        elif akcja == 'a':
            gracz.kierunek_ruchu = (-1, 0)
        elif akcja == 'd':
            gracz.kierunek_ruchu = (1, 0)
        elif akcja == 'p':
            gracz.aktywuj_umiejetnosc()

        swiat.wykonaj_ture()

if __name__ == "__main__":
    start_gry()