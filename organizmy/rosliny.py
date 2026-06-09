# organizmy/rosliny.py
from .bazowe import Roslina, Zwierze

class Trawa(Roslina):
    def __init__(self, swiat): super().__init__(0, swiat)
    def znak(self): return "t"

class Mlecz(Roslina):
    def __init__(self, swiat): super().__init__(0, swiat)
    def znak(self): return "m"
    def akcja(self):
        # 3 próby zasiewu
        for _ in range(3):
            super().akcja()

class Guarana(Roslina):
    def __init__(self, swiat): super().__init__(0, swiat)
    def znak(self): return "g"
    def wplyw_na_atakujacego(self, atakujacy):
        atakujacy.sila += 3
        self.swiat.dodaj_log(f"{atakujacy.nazwa()} zjada Guaranę, siła wzrasta do {atakujacy.sila}!")

class WilczeJagody(Roslina):
    def __init__(self, swiat): super().__init__(99, swiat)
    def znak(self): return "j"
    def wplyw_na_atakujacego(self, atakujacy):
        self.swiat.usun_organizm(atakujacy)
        self.swiat.dodaj_log(f"{atakujacy.nazwa()} ginie od Wilczych Jagód!")

class BarszczSosnowskiego(Roslina):
    def __init__(self, swiat): super().__init__(10, swiat)
    def znak(self): return "b"
    
    def akcja(self):
        sasiedzi = self.swiat.pobierz_sasiednie_pola(self.polozenie)
        for pole in sasiedzi:
            org = self.swiat.pobierz_organizm(pole)
            # Zabija zwierzęta w sąsiedztwie (wyjątek Cyber Owca, którą chroni polimorfizm)
            if isinstance(org, Zwierze) and not org.czy_odporny_na_barszcz():
                self.swiat.dodaj_log(f"Barszcz spala {org.nazwa()}!")
                self.swiat.usun_organizm(org)
        
        super().akcja() # Rozsiewanie

    def wplyw_na_atakujacego(self, atakujacy):
        if not atakujacy.czy_odporny_na_barszcz():
            self.swiat.usun_organizm(atakujacy)
            self.swiat.dodaj_log(f"{atakujacy.nazwa()} ginie od zjedzenia Barszczu!")