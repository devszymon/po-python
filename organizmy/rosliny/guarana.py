from organizmy.bazowe import Roslina


class Guarana(Roslina):
    def __init__(self, swiat):
        super().__init__(0, swiat)

    def znak(self):
        return "g"

    def wplyw_na_atakujacego(self, atakujacy):
        atakujacy.sila += 3
        self.swiat.dodaj_log(f"{atakujacy.nazwa()} zjada Guaranę, siła wzrasta do {atakujacy.sila}!")

