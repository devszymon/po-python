from organizmy.bazowe import Roslina, Zwierze


class BarszczSosnowskiego(Roslina):
    def __init__(self, swiat):
        super().__init__(10, swiat)

    def znak(self):
        return "b"

    def akcja(self):
        sasiedzi = self.swiat.pobierz_sasiednie_pola(self.polozenie)
        for pole in sasiedzi:
            organizm = self.swiat.pobierz_organizm(pole)
            if isinstance(organizm, Zwierze) and not organizm.czy_odporny_na_barszcz():
                self.swiat.dodaj_log(f"Barszcz spala {organizm.nazwa()}!")
                self.swiat.usun_organizm(organizm)

        super().akcja()

    def wplyw_na_atakujacego(self, atakujacy):
        if not atakujacy.czy_odporny_na_barszcz():
            self.swiat.usun_organizm(atakujacy)
            self.swiat.dodaj_log(f"{atakujacy.nazwa()} ginie od zjedzenia Barszczu!")

