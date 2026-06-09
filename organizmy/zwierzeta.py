# organizmy/zwierzeta.py
import random
from .bazowe import Zwierze
from umiejetnosci.calopalenie import Calopalenie

class Wilk(Zwierze):
    def __init__(self, swiat): super().__init__(9, 5, swiat)
    def znak(self): return "W"

class Owca(Zwierze):
    def __init__(self, swiat): super().__init__(4, 4, swiat)
    def znak(self): return "O"

class Lis(Zwierze):
    def __init__(self, swiat): super().__init__(3, 7, swiat)
    def znak(self): return "L"
    def losuj_pole_ruchu(self, zasieg=1):
        sasiednie = self.swiat.pobierz_sasiednie_pola(self.polozenie, zasieg)
        bezpieczne = []
        for p in sasiednie:
            org = self.swiat.pobierz_organizm(p)
            # Dobry węch - nie idzie tam, gdzie wróg silniejszy
            if org is None or org.sila <= self.sila:
                bezpieczne.append(p)
        return random.choice(bezpieczne) if bezpieczne else self.polozenie

class Zolw(Zwierze):
    def __init__(self, swiat): super().__init__(2, 1, swiat)
    def znak(self): return "Z"
    def akcja(self):
        if random.random() > 0.75: # W 75% przypadków nie rusza się
            super().akcja()
    def czy_odbija_atak(self, atakujacy):
        return atakujacy.sila < 5

class Antylopa(Zwierze):
    def __init__(self, swiat): super().__init__(4, 4, swiat)
    def znak(self): return "A"
    def akcja(self):
        # Ruch o 2 pola
        nowe_pole = self.losuj_pole_ruchu(zasieg=2)
        if nowe_pole != self.polozenie:
            self.przemiesc_sie_lub_walcz(nowe_pole)
    def czy_ucieka(self):
        return random.random() < 0.5

class CyberOwca(Zwierze):
    def __init__(self, swiat): super().__init__(10, 4, swiat)
    def znak(self): return "C"
    def czy_odporny_na_barszcz(self): return True
    def akcja(self):
        from .rosliny import BarszczSosnowskiego
        barszcze = [o for o in self.swiat._organizmy if isinstance(o, BarszczSosnowskiego) and o.zyje]
        
        if not barszcze:
            super().akcja() # Zachowuje się jak zwykła owca, jeśli brak celu
            return

        # Logika polowania: szukanie najbliższego
        cel = min(barszcze, key=lambda b: abs(b.polozenie[0] - self.polozenie[0]) + abs(b.polozenie[1] - self.polozenie[1]))
        
        dx = max(-1, min(1, cel.polozenie[0] - self.polozenie[0]))
        dy = max(-1, min(1, cel.polozenie[1] - self.polozenie[1]))
        nowe_pole = (self.polozenie[0] + dx, self.polozenie[1] + dy)
        
        if nowe_pole != self.polozenie:
            self.przemiesc_sie_lub_walcz(nowe_pole)


class Czlowiek(Zwierze):
    def __init__(self, swiat):
        super().__init__(5, 4, swiat)
        self.kierunek_ruchu = None
        self.umiejetnosc = Calopalenie(self)

    def znak(self): return "H"

    def aktywuj_umiejetnosc(self):
        if self.umiejetnosc.aktywuj():
            self.swiat.dodaj_log("Człowiek aktywował Całopalenie!")
        else:
            self.swiat.dodaj_log("Umiejętność ładuje się lub już trwa!")

    def akcja(self):
        self.umiejetnosc.aktualizuj_stan()
        
        if self.kierunek_ruchu:
            nx = self.polozenie[0] + self.kierunek_ruchu[0]
            ny = self.polozenie[1] + self.kierunek_ruchu[1]
            nowe_pole = (nx, ny)
            
            if self.swiat.czy_pole_na_planszy(nowe_pole):
                self.przemiesc_sie_lub_walcz(nowe_pole)
            
            self.kierunek_ruchu = None

        # Po ruchu - rozpatrzenie palenia przestrzeni
        self.umiejetnosc.dzialanie(self.swiat)