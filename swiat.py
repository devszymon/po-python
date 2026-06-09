# swiat.py
import random

class Swiat:
    def __init__(self, szerokosc: int, wysokosc: int):
        self._szerokosc = szerokosc
        self._wysokosc = wysokosc
        self._tura = 0
        self._organizmy = []
        self._plansza = {}
        self._logi = []

    @property
    def szerokosc(self): return self._szerokosc
    
    @property
    def wysokosc(self): return self._wysokosc

    def dodaj_log(self, komunikat: str):
        self._logi.append(komunikat)

    def pobierz_logi_i_wyczysc(self):
        logi = self._logi[:]
        self._logi.clear()
        return logi

    def czy_pole_na_planszy(self, pole: tuple) -> bool:
        x, y = pole
        return 0 <= x < self._szerokosc and 0 <= y < self._wysokosc

    def pobierz_organizm(self, pole: tuple):
        return self._plansza.get(pole)

    def dodaj_organizm(self, organizm, pole: tuple):
        if self.czy_pole_na_planszy(pole) and pole not in self._plansza:
            self._organizmy.append(organizm)
            self._plansza[pole] = organizm
            organizm.polozenie = pole

    def usun_organizm(self, organizm):
        if organizm in self._organizmy:
            organizm.zyje = False
            self._organizmy.remove(organizm)
            if self._plansza.get(organizm.polozenie) == organizm:
                del self._plansza[organizm.polozenie]

    def przesun_organizm(self, organizm, nowe_pole: tuple):
        stare_pole = organizm.polozenie
        if self._plansza.get(stare_pole) == organizm:
            del self._plansza[stare_pole]
        self._plansza[nowe_pole] = organizm
        organizm.polozenie = nowe_pole

    def pobierz_sasiednie_pola(self, pole: tuple, zasieg: int = 1):
        x, y = pole
        pola = []
        for dx in range(-zasieg, zasieg + 1):
            for dy in range(-zasieg, zasieg + 1):
                if dx == 0 and dy == 0:
                    continue
                nowe = (x + dx, y + dy)
                if self.czy_pole_na_planszy(nowe):
                    pola.append(nowe)
        return pola

    def znajdz_wolne_sasiednie(self, pole: tuple, zasieg: int = 1):
        sasiednie = self.pobierz_sasiednie_pola(pole, zasieg)
        wolne = [p for p in sasiednie if p not in self._plansza]
        return random.choice(wolne) if wolne else None

    def wykonaj_ture(self):
        self._tura += 1
        # Sortowanie wedle priorytetów: inicjatywa (malejąco), potem wiek (malejąco)
        self._organizmy.sort(key=lambda o: (o.inicjatywa, o.wiek), reverse=True)
        
        # Iterujemy po kopii, na wypadek gdyby organizmy zginęły w trakcie tury
        for org in self._organizmy[:]:
            if org.zyje and org.wiek > 0:
                org.akcja()
            org.wiek += 1

    def rysuj_swiat(self):
        print(f"--- Tura {self._tura} ---")
        for y in range(self._wysokosc):
            wiersz = ""
            for x in range(self._szerokosc):
                org = self._plansza.get((x, y))
                wiersz += org.znak() if org else "."
            print(wiersz)
        print("-------------")